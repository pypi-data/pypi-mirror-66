try:  # python 3.3+
    from inspect import signature
except ImportError:
    from funcsigs import signature

try:
    from typing import Union, Callable, Any
except ImportError:
    pass

from distutils.version import LooseVersion
from warnings import warn

from six import string_types
import pytest


# Create a symbol that will work to create a fixture containing 'yield', whatever the pytest version
# Note: if more prevision is needed, use    if LooseVersion(pytest.__version__) < LooseVersion('3.0.0')
if int(pytest.__version__.split('.', 1)[0]) < 3:
    yield_fixture = pytest.yield_fixture
else:
    yield_fixture = pytest.fixture


def remove_duplicates(lst):
    dset = set()
    # relies on the fact that dset.add() always returns None.
    return [item for item in lst
            if item not in dset and not dset.add(item)]


def is_fixture(fixture_fun  # type: Any
               ):
    """
    Returns True if the provided function is a fixture

    :param fixture_fun:
    :return:
    """
    try:
        # noinspection PyStatementEffect
        fixture_fun._pytestfixturefunction
        return True
    except AttributeError:
        # not a fixture ?
        return False


def assert_is_fixture(fixture_fun  # type: Any
                      ):
    """
    Raises a ValueError if the provided fixture function is not a fixture.

    :param fixture_fun:
    :return:
    """
    if not is_fixture(fixture_fun):
        raise ValueError("The provided fixture function does not seem to be a fixture: %s. Did you properly decorate "
                         "it ?" % fixture_fun)


def get_fixture_name(fixture_fun  # type: Union[str, Callable]
                     ):
    """
    Internal utility to retrieve the fixture name corresponding to the given fixture function.
    Indeed there is currently no pytest API to do this.

    Note: this function can receive a string, in which case it is directly returned.

    :param fixture_fun:
    :return:
    """
    if isinstance(fixture_fun, string_types):
        return fixture_fun
    assert_is_fixture(fixture_fun)
    try:  # pytest 3
        custom_fixture_name = fixture_fun._pytestfixturefunction.name
    except AttributeError:
        try:  # pytest 2
            custom_fixture_name = fixture_fun.func_name
        except AttributeError:
            custom_fixture_name = None

    if custom_fixture_name is not None:
        # there is a custom fixture name
        return custom_fixture_name
    else:
        obj__name = getattr(fixture_fun, '__name__', None)
        if obj__name is not None:
            # a function, probably
            return obj__name
        else:
            # a callable object probably
            return str(fixture_fun)


def get_fixture_scope(fixture_fun):
    """
    Internal utility to retrieve the fixture scope corresponding to the given fixture function .
    Indeed there is currently no pytest API to do this.

    :param fixture_fun:
    :return:
    """
    assert_is_fixture(fixture_fun)
    return fixture_fun._pytestfixturefunction.scope
    # except AttributeError:
    #     # pytest 2
    #     return fixture_fun.func_scope


def get_param_argnames_as_list(argnames):
    """
    pytest parametrize accepts both coma-separated names and list/tuples.
    This function makes sure that we always return a list
    :param argnames:
    :return:
    """
    if isinstance(argnames, string_types):
        argnames = argnames.replace(' ', '').split(',')
    return list(argnames)


# ------------ container for the mark information that we grab from the fixtures (`@fixture_plus`)
class _ParametrizationMark:
    """
    Represents the information required by `@fixture_plus` to work.
    """
    __slots__ = "param_names", "param_values", "param_ids"

    def __init__(self, mark):
        bound = get_parametrize_signature().bind(*mark.args, **mark.kwargs)
        try:
            remaining_kwargs = bound.arguments['kwargs']
        except KeyError:
            pass
        else:
            if len(remaining_kwargs) > 0:
                warn("parametrize kwargs not taken into account: %s. Please report it at"
                     " https://github.com/smarie/python-pytest-cases/issues" % remaining_kwargs)
        self.param_names = get_param_argnames_as_list(bound.arguments['argnames'])
        self.param_values = bound.arguments['argvalues']
        try:
            bound.apply_defaults()
            self.param_ids = bound.arguments['ids']
        except AttributeError:
            # can happen if signature is from funcsigs so we have to apply ourselves
            self.param_ids = bound.arguments.get('ids', None)


# -------- tools to get the parametrization mark whatever the pytest version
class _LegacyMark:
    __slots__ = "args", "kwargs"

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


# ---------------- working on pytest nodes (e.g. Function)

def is_function_node(node):
    try:
        node.function
        return True
    except AttributeError:
        return False


def get_parametrization_markers(fnode):
    """
    Returns the parametrization marks on a pytest Function node.
    :param fnode:
    :return:
    """
    if LooseVersion(pytest.__version__) >= LooseVersion('3.4.0'):
        return list(fnode.iter_markers(name="parametrize"))
    else:
        return list(fnode.parametrize)


def get_param_names(fnode):
    """
    Returns a list of parameter names for the given pytest Function node.
    parameterization marks containing several names are split

    :param parentnode:
    :return:
    """
    p_markers = get_parametrization_markers(fnode)
    param_names = []
    for paramz_mark in p_markers:
        param_names += get_param_argnames_as_list(paramz_mark.args[0])
    return param_names


# ---------------- working on functions
def get_pytest_marks_on_function(f):
    """
    Utility to return *ALL* pytest marks (not only parametrization) applied on a function

    :param f:
    :return:
    """
    try:
        return f.pytestmark
    except AttributeError:
        try:
            # old pytest < 3: marks are set as fields on the function object
            # but they do not have a particulat type, their type is 'instance'...
            return [v for v in vars(f).values() if str(v).startswith("<MarkInfo '")]
        except AttributeError:
            return []


def get_pytest_parametrize_marks(f):
    """
    Returns the @pytest.mark.parametrize marks associated with a function (and only those)

    :param f:
    :return: a tuple containing all 'parametrize' marks
    """
    # pytest > 3.2.0
    marks = getattr(f, 'pytestmark', None)
    if marks is not None:
        return tuple(_ParametrizationMark(m) for m in marks if m.name == 'parametrize')
    else:
        # older versions
        mark_info = getattr(f, 'parametrize', None)
        if mark_info is not None:
            # mark_info.args contains a list of (name, values)
            if len(mark_info.args) % 2 != 0:
                raise ValueError("internal pytest compatibility error - please report")
            nb_parameters = len(mark_info.args) // 2
            if nb_parameters > 1 and len(mark_info.kwargs) > 0:
                raise ValueError("Unfortunately with this old pytest version it is not possible to have several "
                                 "parametrization decorators")
            res = []
            for i in range(nb_parameters):
                param_name, param_values = mark_info.args[2*i:2*(i+1)]
                res.append(_ParametrizationMark(_LegacyMark(param_name, param_values, **mark_info.kwargs)))
            return tuple(res)
        else:
            return ()


def _pytest_mark_parametrize(argnames, argvalues, ids=None, indirect=False, scope=None, **kwargs):
    """ Fake method to have a reference signature of pytest.mark.parametrize"""
    pass


def get_parametrize_signature():
    """

    :return: a reference signature representing
    """
    return signature(_pytest_mark_parametrize)


# ---------- test ids utils ---------
def get_test_ids_from_param_values(param_names,
                                   param_values,
                                   ):
    """
    Replicates pytest behaviour to generate the ids when there are several parameters in a single `parametrize`

    :param param_names:
    :param param_values:
    :return: a list of param ids
    """
    nb_params = len(param_names)
    if nb_params == 0:
        raise ValueError("empty list provided")
    elif nb_params == 1:
        paramids = list(str(v) for v in param_values)
    else:
        paramids = []
        for vv in param_values:
            if len(vv) != nb_params:
                raise ValueError("Inconsistent lenghts for parameter names and values: '%s' and '%s'"
                                 "" % (param_names, vv))
            paramids.append('-'.join([str(v) for v in vv]))
    return paramids


# ---- ParameterSet api ---
def extract_parameterset_info(pnames, pmark):
    """

    :param pnames: the names in this parameterset
    :param pmark: the parametrization mark (a _ParametrizationMark)
    :return:
    """
    _pids = []
    _pmarks = []
    _pvalues = []
    for v in pmark.param_values:
        if is_marked_parameter_value(v):
            # --id
            id = get_marked_parameter_id(v)
            _pids.append(id)
            # --marks
            marks = get_marked_parameter_marks(v)
            _pmarks.append(marks)  # note: there might be several
            # --value(a tuple if this is a tuple parameter)
            vals = get_marked_parameter_values(v)
            if len(vals) != len(pnames):
                raise ValueError("Internal error - unsupported pytest parametrization+mark combination. Please "
                                 "report this issue")
            if len(vals) == 1:
                _pvalues.append(vals[0])
            else:
                _pvalues.append(vals)
        else:
            _pids.append(None)
            _pmarks.append(None)
            _pvalues.append(v)

    return _pids, _pmarks, _pvalues


try:  # pytest 3.x+
    from _pytest.mark import ParameterSet
    def is_marked_parameter_value(v):
        return isinstance(v, ParameterSet)

    def get_marked_parameter_marks(v):
        return v.marks

    def get_marked_parameter_values(v):
        return v.values

    def get_marked_parameter_id(v):
        return v.id

except ImportError:  # pytest 2.x
    from _pytest.mark import MarkDecorator

    def is_marked_parameter_value(v):
        return isinstance(v, MarkDecorator)

    def get_marked_parameter_marks(v):
        return [v]

    def get_marked_parameter_values(v):
        return v.args[1:]

    def get_marked_parameter_id(v):
        return v.kwargs.get('id', None)


# ---- tools to reapply marks on test parameter values, whatever the pytest version ----

# Compatibility for the way we put marks on single parameters in the list passed to @pytest.mark.parametrize
# see https://docs.pytest.org/en/3.3.0/skipping.html?highlight=mark%20parametrize#skip-xfail-with-parametrize

try:
    # check if pytest.param exists
    _ = pytest.param
except AttributeError:
    # if not this is how it was done
    # see e.g. https://docs.pytest.org/en/2.9.2/skipping.html?highlight=mark%20parameter#skip-xfail-with-parametrize
    def make_marked_parameter_value(c, marks):
        if len(marks) > 1:
            raise ValueError("Multiple marks on parameters not supported for old versions of pytest")
        else:
            # get a decorator for each of the markinfo
            marks_mod = transform_marks_into_decorators(marks)

            # decorate
            return marks_mod[0](c)
else:
    # Otherwise pytest.param exists, it is easier
    def make_marked_parameter_value(c, marks):
        # get a decorator for each of the markinfo
        marks_mod = transform_marks_into_decorators(marks)

        # decorate
        return pytest.param(c, marks=marks_mod)


def transform_marks_into_decorators(marks):
    """
    Transforms the provided marks (MarkInfo) obtained from marked cases, into MarkDecorator so that they can
    be re-applied to generated pytest parameters in the global @pytest.mark.parametrize.

    :param marks:
    :return:
    """
    marks_mod = []
    try:
        for m in marks:
            md = pytest.mark.MarkDecorator()

            if LooseVersion(pytest.__version__) >= LooseVersion('3.0.0'):
                if isinstance(m, type(md)):
                    # already a decorator, we can use it
                    marks_mod.append(m)
                else:
                    md.mark = m
                    marks_mod.append(md)
            else:
                # always recreate one, type comparison does not work (all generic stuff)
                md.name = m.name
                # md.markname = m.name
                md.args = m.args
                md.kwargs = m.kwargs

                # markinfodecorator = getattr(pytest.mark, markinfo.name)
                # markinfodecorator(*markinfo.args)

                marks_mod.append(md)

    except Exception as e:
        warn("Caught exception while trying to mark case: [%s] %s" % (type(e), e))
    return marks_mod


def get_pytest_nodeid(metafunc):
    try:
        return metafunc.definition.nodeid
    except AttributeError:
        return "unknown"


try:
    from _pytest.fixtures import scopes as pt_scopes
except ImportError:
    # pytest 2
    from _pytest.python import scopes as pt_scopes


def get_pytest_scopenum(scope_str):
    return pt_scopes.index(scope_str)


def get_pytest_function_scopenum():
    return pt_scopes.index("function")
