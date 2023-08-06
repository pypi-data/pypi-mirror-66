from sys import version_info

try:  # python 3.2+
    from functools import lru_cache
except ImportError:
    from functools32 import lru_cache

try:  # python 3.3+
    from inspect import signature, Parameter
except ImportError:
    from funcsigs import signature, Parameter

from inspect import getmodule
from makefun import wraps, add_signature_parameters, with_signature

import pytest
from pytest_steps.steps_common import create_pytest_param_str_id, get_fixture_or_param_value, get_pytest_node_hash_id


class StepsDataHolder:
    """
    An object that is passed along the various steps of your tests.
    You can put intermediate results in here, and find them in the following steps.

    Note: you can use `vars(results)` to see the available results.
    """
    pass


STEP_SUCCESS_FIELD = "__test_step_successful_for__"


def get_parametrize_decorator(steps, steps_data_holder_name, test_step_argname):
    """
    Subroutine of `pytest_steps` used to perform the test function parametrization when test step mode is 'parametrize'.
    See `pytest_steps` for details.

    :param steps:
    :param steps_data_holder_name:
    :param test_step_argname:
    :return:
    """
    def steps_decorator(test_func):
        """
        The generated test function decorator.

        It is equivalent to @mark.parametrize('case_data', cases) where cases is a tuple containing a CaseDataGetter for
        all case generator functions

        :param test_func:
        :return:
        """

        # Step ids
        step_ids = [create_pytest_param_str_id(f) for f in steps]

        # Depending on the presence of steps_data_holder_name in signature, create a cached fixture for steps data
        s = signature(test_func)
        if steps_data_holder_name in s.parameters:
            # the user wishes to share results across test steps. Create a cached fixture
            @lru_cache(maxsize=None)
            def get_results_holder(**kwargs):
                """
                A factory for the StepsDataHolder objects. Since it uses @lru_cache, the same StepsDataHolder will be
                returned when the keyword arguments are the same.

                :param kwargs:
                :return:
                """
                return StepsDataHolder()  # TODO use Munch or MaxiMunch from `mixture` project, when publicly available?

            def results(request):
                """
                The fixture for the StepsDataHolder.

                It is function-scoped (so oit is called for each step of each param combination)
                but it implements an intelligent cache so that the same StepsDataHolder object is returned across all
                test steps belonging to the same param combination.

                :param request:
                :return:
                """
                # Get a good unique identifier of the test.
                # The id should be different everytime anything changes, except when the test step changes
                # Note: when the id was using not only param values but also fixture values we had to discard
                # steps_data_holder_name and 'request'. But that's not the case anymore,simply discard "test step" param
                test_id = get_pytest_node_hash_id(request.node, params_to_ignore={test_step_argname})

                # Get or create the cached Result holder for this combination of parameters
                return get_results_holder(id=test_id)

            # Create a fixture with custom name : this seems to work also for old pytest versions
            results.__name__ = steps_data_holder_name
            results = pytest.fixture(results)

            # Add the fixture dynamically: we have to add it to the function holder module as explained in
            # https://github.com/pytest-dev/pytest/issues/2424
            module = getmodule(test_func)
            if steps_data_holder_name not in dir(module):
                setattr(module, steps_data_holder_name, results)
            else:
                raise ValueError("The {} fixture already exists in module {}: please specify a different "
                                 "`steps_data_holder_name` in `@test_steps`".format(steps_data_holder_name, module))

        # Parametrize the function with the test steps
        parametrizer = pytest.mark.parametrize(test_step_argname, steps, ids=step_ids)

        # We will expose a new signature with additional 'request' arguments if needed
        orig_sig = signature(test_func)
        func_needs_request = 'request' in orig_sig.parameters
        if not func_needs_request:
            # add request parameter last, as first may be 'self'
            new_sig = add_signature_parameters(orig_sig, last=Parameter('request',
                                                                        kind=Parameter.POSITIONAL_OR_KEYWORD))
        else:
            new_sig = orig_sig

        # Finally, if there are some steps that are marked as having a dependency,
        use_dependency = any(hasattr(step, DEPENDS_ON_FIELD) for step in steps)
        if not use_dependency:
            # no dependencies: no need to do complex things
            # Create a light function wrapper that will allow for manual execution
            @wraps(test_func, new_sig=new_sig)
            def wrapped_test_function(*args, **kwargs):
                request = kwargs['request'] if func_needs_request else kwargs.pop('request')
                if request is None:
                    # manual call (maybe for pre-loading?), ability to execute several steps
                    _execute_manually(test_func, s, test_step_argname, step_ids, steps, args, kwargs)
                else:
                    return test_func(*args, **kwargs)
        else:
            # Create a test function wrapper that will replace the test steps with monitored ones before injecting them
            @wraps(test_func, new_sig=new_sig)
            def wrapped_test_function(*args, **kwargs):
                """Executes the current step only if its dependencies are correct, and registers its execution result"""
                request = kwargs['request'] if func_needs_request else kwargs.pop('request')
                if request is None:
                    # manual call (maybe for pre-loading?), no dependency management, ability to execute several steps
                    _execute_manually(test_func, s, test_step_argname, step_ids, steps, args, kwargs)
                else:
                    # (a) retrieve the "current step" function
                    current_step_fun = get_fixture_or_param_value(request, test_step_argname)

                    # Get the unique id that is shared between the steps of the same execution
                    # Note: when the id was using not only param values but also fixture values we had to discard
                    # steps_data_holder_name and 'request'. But that's not the case anymore, simply discard "test step"
                    test_id_without_steps = get_pytest_node_hash_id(request.node, params_to_ignore={test_step_argname})

                    # Make sure that it has a field to store its execution success
                    if not hasattr(current_step_fun, STEP_SUCCESS_FIELD):
                        # this is a dict where the key is the `test_id_without_steps` and the value is a boolean
                        setattr(current_step_fun, STEP_SUCCESS_FIELD, dict())

                    # (b) skip or fail it if needed
                    dependencies, should_fail = getattr(current_step_fun, DEPENDS_ON_FIELD, ([], False))
                    # -- check that dependencies have all run (execution order is correct)
                    if not all(hasattr(step, STEP_SUCCESS_FIELD) for step in dependencies):
                        raise ValueError("Test step {} depends on another step that has not yet been executed. In "
                                         "current version the steps execution order is manual, make sure it is correct."
                                         "".format(current_step_fun.__name__))
                    # -- check that dependencies all ran with success
                    deps_successess = {step: getattr(step, STEP_SUCCESS_FIELD).get(test_id_without_steps, False)
                                       for step in dependencies}
                    failed_deps = [d.__name__ for d, res in deps_successess.items() if res is False]
                    if not all(deps_successess.values()):
                        msg = "This test step depends on other steps, and the following have failed: %s" % failed_deps
                        if should_fail:
                            pytest.fail(msg)
                        else:
                            pytest.skip(msg)

                    # (c) execute the test function for this step
                    res = test_func(*args, **kwargs)

                    # (d) declare execution as a success
                    getattr(current_step_fun, STEP_SUCCESS_FIELD)[test_id_without_steps] = True

                    return res

        # With this hack we will be ordered correctly by pytest https://github.com/pytest-dev/pytest/issues/4429
        wrapped_test_function.place_as = test_func

        # finally apply parametrizer
        wrapped_parametrized_test_function = parametrizer(wrapped_test_function)
        return wrapped_parametrized_test_function

    return steps_decorator


def _execute_manually(test_func, s, test_step_argname, all_step_ids, all_steps, args, kwargs):
    """
    Internal utility method to execute all steps of a test function manually

    :param test_func:
    :param s:
    :param test_step_argname:
    :param all_step_ids:
    :param all_steps:
    :param args:
    :param kwargs:
    :return:
    """
    bound = s.bind(*args, **kwargs)
    steps_to_run = bound.arguments[test_step_argname]
    if steps_to_run is None:
        # print("@test_steps - decorated function '%s' is being called manually. The `%s` parameter is "
        #       "set to None so all steps will be executed in order" % (f, test_step_argname))
        steps_to_run = all_steps
    else:
        # print("@test_steps - decorated function '%s' is being called manually. The `%s` parameter is "
        #       "set to %s so only these steps will be executed in order."
        #       "" % (f, test_step_argname, steps_to_run))
        if not isinstance(steps_to_run, (list, tuple)):
            steps_to_run = [steps_to_run]
    # execute specified steps
    for step in steps_to_run:
        try:
            # if step is in step_ids, replace it with the step object
            idx = all_step_ids.index(step)
            step = all_steps[idx]
        except ValueError:
            pass

        # set the step
        bound.arguments[test_step_argname] = step

        # execute
        test_func(*bound.args, **bound.kwargs)

    return


DEPENDS_ON_FIELD = '__depends_on__'
_FAIL_INSTEAD_OF_SKIP_DEFAULT = False


# Python 3+: load the 'more explicit api' for `test_steps`
if version_info >= (3, 0):
    new_sig = """(*steps,
                  fail_instead_of_skip: bool = _FAIL_INSTEAD_OF_SKIP_DEFAULT)"""
else:
    new_sig = None


@with_signature(new_sig)
def depends_on(*steps, **kwargs):
    """
    Decorates a test step object so as to automatically mark it as skipped (default) or failed if the dependency
    has not succeeded.

    :param steps: a list of test steps that this step depends on. They can be anything, but typically they are non-test
        (not prefixed with 'test') functions.
    :param fail_instead_of_skip: if set to True, the test will be marked as failed instead of skipped when the
        dependencies have not succeeded.
    :return:
    """
    # python 2 compatibility: no keyword arguments can follow an *args.
    fail_instead_of_skip = kwargs.pop('fail_instead_of_skip', _FAIL_INSTEAD_OF_SKIP_DEFAULT)
    if len(kwargs) > 0:
        raise ValueError("Invalid argument(s): " + str(kwargs.keys()))

    def depends_on_decorator(step_func):
        """
        The generated test function decorator.

        :param step_func:
        :return:
        """
        if not callable(step_func):
            raise TypeError("@depends_on can only be used on test steps that are callables")

        # Remember the dependencies so that @test_steps knows
        setattr(step_func, DEPENDS_ON_FIELD, (steps, fail_instead_of_skip))

        return step_func

    return depends_on_decorator
