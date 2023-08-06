from pedal.cait.cait_api import parse_program
from pedal.core.commands import gently
from pedal.core.report import MAIN_REPORT
from pedal.sandbox import compatibility
import ast

from pedal.toolkit.signatures import type_check, parse_type, normalize_type, parse_type_value, test_type_equality

DELTA = 0.001


def all_documented():
    """

    Returns:

    """
    ast = parse_program()
    defs = ast.find_all('FunctionDef') + ast.find_all("ClassDef")
    for a_def in defs:
        if a_def.name == "__init__":
            continue
        if (a_def.body and
                (a_def.body[0].ast_name != "Expr" or
                 a_def.body[0].value.ast_name != "Str")):
            if a_def.ast_name == 'FunctionDef':
                gently("You have an undocumented function: " + a_def.name)
            else:
                gently("You have an undocumented class: " + a_def.name)
            return False
    return True


def get_arg_name(node):
    """

    Args:
        node:

    Returns:

    """
    name = node.id
    if name is None:
        return node.arg
    else:
        return name


def match_function(name, root=None):
    """

    Args:
        name:
        root:

    Returns:

    """
    if root is None:
        ast = parse_program()
    else:
        ast = root
    defs = ast.find_all('FunctionDef')
    for a_def in defs:
        if a_def._name == name:
            return a_def
    return None


def match_signature_muted(name, length, *parameters):
    """

    Args:
        name:
        length:
        *parameters:

    Returns:

    """
    ast = parse_program()
    defs = ast.find_all('FunctionDef')
    for a_def in defs:
        if a_def._name == name:
            found_length = len(a_def.args.args)
            if found_length != length:
                return None
            elif parameters:
                for parameter, arg in zip(parameters, a_def.args.args):
                    arg_name = get_arg_name(arg)
                    if arg_name != parameter:
                        return None
                else:
                    return a_def
            else:
                return a_def
    return None


def find_def_by_name(name, root=None):
    """

    Args:
        name:
        root:

    Returns:

    """
    if root is None:
        root = parse_program()
    defs = root.find_all('FunctionDef')
    for a_def in defs:
        if a_def._name == name:
            return a_def
    return None


def match_parameters(name, *types, returns=None, root=None):
    """

    Args:
        name:
        *types:
        returns:
        root:

    Returns:

    """
    defn = find_def_by_name(name, root)
    if defn:
        for expected, actual in zip(types, defn.args.args):
            if actual.annotation:
                expected = parse_type_value(expected, True)
                actual_type = parse_type(actual.annotation)
                if not test_type_equality(expected, actual_type):
                    gently("Error in definition of function `{}` parameter `{}`. Expected `{}`, "
                             "instead found `{}`.".format(name, actual.arg, expected, actual_type),
                             label="wrong_parameter_type", title="Wrong Parameter Type")
                    return None
        else:
            if returns is not None:
                if not isinstance(returns, str):
                    returns = returns.__name__
                if defn.returns:
                    actual_type = parse_type(defn.returns)
                    if not type_check(returns, actual_type):
                        gently("Error in definition of function `{}` return type. Expected `{}`, "
                                 "instead found {}.".format(name, returns, actual_type),
                                 label="wrong_return_type")
                        return None
                else:
                    gently("Error in definition of function `{}` return type. Expected `{}`, "
                             "but there was no return type specified.".format(name, returns),
                             label="missing_return_type")
                    return None
            return defn


def match_signature(name, length, *parameters):
    """

    Args:
        name:
        length:
        *parameters:

    Returns:

    """
    ast = parse_program()
    defs = ast.find_all('FunctionDef')
    for a_def in defs:
        if a_def._name == name:
            found_length = len(a_def.args.args)
            if found_length < length:
                gently("The function named <code>{}</code> has fewer parameters ({}) "
                         "than expected ({}). ".format(name, found_length, length), label="insuff_args")
            elif found_length > length:
                gently("The function named <code>{}</code> has more parameters ({}) "
                         "than expected ({}). ".format(name, found_length, length), label="excess_args")
            elif parameters:
                for parameter, arg in zip(parameters, a_def.args.args):
                    arg_name = get_arg_name(arg)
                    if arg_name != parameter:
                        gently("Error in definition of <code>{}</code>. Expected a parameter named {}, "
                                 "instead found {}.".format(name, parameter, arg_name), label="name_missing")
                        return None
                else:
                    return a_def
            else:
                return a_def
    else:
        gently("No function named <code>{name}</code> was found.".format(name=name),
                 label="missing_func", title="Missing Function", fields={'name': name})
    return None


TEST_TABLE_HEADER = "<table class='blockpy-feedback-unit table table-sm table-bordered table-hover'>"
TEST_TABLE_OUTPUT = TEST_TABLE_HEADER+(
    "<tr class='table-active'><th></th><th>Arguments</th><th>Expected</th><th>Actual</th></tr>"
)
TEST_TABLE_UNITS = TEST_TABLE_HEADER+(
    "<tr class='table-active'><th></th><th>Arguments</th><th>Returned</th><th>Expected</th></tr>"
)
GREEN_CHECK = "<td class='green-check-mark'>&#10004;</td>"
RED_X = "<td>&#10060;</td>"


def output_test(name, *tests):
    """

    Args:
        name:
        *tests:

    Returns:

    """
    student = compatibility.get_student_data()
    if name in student.data:
        the_function = student.data[name]
        if callable(the_function):
            result = TEST_TABLE_OUTPUT
            success = True
            success_count = 0
            for test in tests:
                inp = test[:-1]
                inputs = ', '.join(["<code>{}</code>".format(repr(i)) for i in inp])
                out = test[-1]
                tip = ""
                if isinstance(out, tuple):
                    tip = out[1]
                    out = out[0]
                message = "<td><code>{}</code></td>" + ("<td><pre>{}</pre></td>" * 2)
                test_out = compatibility.capture_output(the_function, *inp)
                if isinstance(out, str):
                    if len(test_out) < 1:
                        message = message.format(inputs, repr(out), "<i>No output</i>", tip)
                        message = "<tr class=''>" + RED_X + message + "</tr>"
                        if tip:
                            message += "<tr class='table-info'><td colspan=4>" + tip + "</td></tr>"
                        success = False
                    elif len(test_out) > 1:
                        message = message.format(inputs, "\n".join(out), "<i>Too many outputs</i>", tip)
                        message = "<tr class=''>" + RED_X + message + "</tr>"
                        if tip:
                            message += "<tr class='info'><td colspan=4>" + tip + "</td></tr>"
                        success = False
                    elif out not in test_out:
                        message = message.format(inputs, "\n".join(out), "\n".join(test_out), tip)
                        message = "<tr class=''>" + RED_X + message + "</tr>"
                        if tip:
                            message += "<tr class='table-info'><td colspan=4>" + tip + "</td></tr>"
                        success = False
                    else:
                        message = message.format(inputs, "\n".join(out), "\n".join(test_out), tip)
                        message = "<tr class=''>" + GREEN_CHECK + message + "</tr>"
                        success_count += 1
                elif out != test_out:
                    if len(test_out) < 1:
                        message = message.format(inputs, "\n".join(out), "<i>No output</i>", tip)
                    else:
                        message = message.format(inputs, "\n".join(out), "\n".join(test_out), tip)
                    message = "<tr class=''>" + RED_X + message + "</tr>"
                    if tip:
                        message += "<tr class='table-info'><td colspan=4>" + tip + "</td></tr>"
                    success = False
                else:
                    message = message.format(inputs, "\n".join(out), "\n".join(test_out), tip)
                    message = "<tr class=''>" + GREEN_CHECK + message + "</tr>"
                    success_count += 1
                result += message
            if success:
                return the_function
            else:
                result = ("I ran your function <code>{}</code> on some new arguments, and it gave the wrong output "
                          "{}/{} times.".format(name, len(tests) - success_count, len(tests)) + result)
                gently(result + "</table>", label="wrong_output")
                return None
        else:
            gently("You defined {}, but did not define it as a function.".format(name), label="not_func_def")
            return None
    else:
        gently("The function <code>{}</code> was not defined.".format(name), label="no_func_def")
        return None


def unit_test(name, *tests):
    """
    Show a table
    :param name:
    :param tests:
    :return:
    """
    student = compatibility.get_student_data()
    if name in student.data:
        the_function = student.data[name]
        if callable(the_function):
            result = TEST_TABLE_UNITS
            success = True
            success_count = 0
            for test in tests:
                inp = test[:-1]
                inputs = ', '.join(["<code>{}</code>".format(repr(i)) for i in inp])
                out = test[-1]
                tip = ""
                if isinstance(out, tuple):
                    tip = out[1]
                    out = out[0]
                message = ("<td><code>{}</code></td>" * 3)
                ran = True
                try:
                    test_out = the_function(*inp)
                except Exception as e:
                    message = message.format(inputs, str(e), repr(out))
                    message = "<tr class=''>" + RED_X + message + "</tr>"
                    success = False
                    ran = False
                if not ran:
                    result += message
                    continue
                message = message.format(inputs, repr(test_out), repr(out))
                if (isinstance(out, float) and
                        isinstance(test_out, (float, int)) and
                        abs(out - test_out) < DELTA):
                    message = "<tr class=''>" + GREEN_CHECK + message + "</tr>"
                    success_count += 1
                elif out != test_out:
                    # gently(message)
                    message = "<tr class=''>" + RED_X + message + "</tr>"
                    if tip:
                        message += "<tr class='table-info'><td colspan=4>" + tip + "</td></tr>"
                    success = False
                else:
                    message = "<tr class=''>" + GREEN_CHECK + message + "</tr>"
                    success_count += 1
                result += message
            if success:
                return the_function
            else:
                result = "I ran your function <code>{}</code> on some new arguments, " \
                         "and it failed {}/{} tests.".format(name, len(tests) - success_count, len(tests)) + result
                gently(result + "</table>", label="tests_failed")
                return None
        else:
            gently("You defined {}, but did not define it as a function.".format(name))
            return None
    else:
        gently("The function <code>{}</code> was not defined.".format(name))
        return None


class _LineVisitor(ast.NodeVisitor):
    """
    NodeVisitor subclass that visits every statement of a program and tracks
    their line numbers in a list.
    
    Attributes:
        lines (list[int]): The list of lines that were visited.
    """

    def __init__(self):
        self.lines = []

    def _track_lines(self, node):
        self.lines.append(node.lineno)
        self.generic_visit(node)

    visit_FunctionDef = _track_lines
    visit_AsyncFunctionDef = _track_lines
    visit_ClassDef = _track_lines
    visit_Return = _track_lines
    visit_Delete = _track_lines
    visit_Assign = _track_lines
    visit_AugAssign = _track_lines
    visit_AnnAssign = _track_lines
    visit_For = _track_lines
    visit_AsyncFor = _track_lines
    visit_While = _track_lines
    visit_If = _track_lines
    visit_With = _track_lines
    visit_AsyncWith = _track_lines
    visit_Raise = _track_lines
    visit_Try = _track_lines
    visit_Assert = _track_lines
    visit_Import = _track_lines
    visit_ImportFrom = _track_lines
    visit_Global = _track_lines
    visit_Nonlocal = _track_lines
    visit_Expr = _track_lines
    visit_Pass = _track_lines
    visit_Continue = _track_lines
    visit_Break = _track_lines


def check_coverage(report=None):
    """
    Checks that all the statements in the program have been executed.
    This function only works when a tracer_style has been set in the sandbox,
    or you are using an environment that automatically traces calls (e.g.,
    BlockPy).
    
    TODO: Make compatible with tracer_style='coverage'
    
    Args:
        report (Report): The Report to draw source code from; if not given,
            defaults to MAIN_REPORT.
    Returns:
        bool or set[int]: If the source file was not parsed, None is returned.
            If there were fewer lines traced in execution than are found in
            the AST, then the set of unexecuted lines are returned. Otherwise,
            False is returned.
    """
    if report is None:
        report = MAIN_REPORT
    if not report['source']['success']:
        return None, 0
    lines_executed = set(compatibility.trace_lines())
    if -1 in lines_executed:
        lines_executed.remove(-1)
    student_ast = report['source']['ast']
    visitor = _LineVisitor()
    visitor.visit(student_ast)
    lines_in_code = set(visitor.lines)
    if lines_executed < lines_in_code:
        return lines_in_code - lines_executed, len(lines_executed)/len(lines_in_code)
    else:
        return False, 1


def ensure_coverage(percentage=.5, destructive=False, report=None):
    """
    Provides some feedback if the students' code has coverage below the
    given percentage.
    Note that this avoids destroying the current sandbox instance stored on the
    report, if there is one present.
    
    Args:
        report:
        percentage:
        destructive (bool): Whether or not to remove the sandbox.
    """
    if report is None:
        report = MAIN_REPORT
    student_code = report['source']['code']
    unexecuted_lines, percent_covered = check_coverage(report)
    if unexecuted_lines:
        if percent_covered <= percentage:
            gently("Your code coverage is not adequate. You must cover at least half your code to receive feedback.")
            return False
    return True


def ensure_cisc108_tests(test_count, report=None):
    """

    TODO: This should be moved out of pedal, or generalized for environments.

    Args:
        test_count:
        report:

    Returns:

    """
    student = compatibility.get_student_data()
    if 'assert_equal' not in student.data:
        gently("You have not imported assert_equal from the cisc108 module.")
        return False
    assert_equal = student.data['assert_equal']
    if not hasattr(assert_equal, 'student_tests'):
        gently("The assert_equal function has been modified. Do not let it be overwritten!",
               label="Assertion Function Corrupted")
        return False
    student_tests = assert_equal.student_tests
    if student_tests.tests == 0:
        gently("You are not unit testing the result.", label="No Student Unit Tests")
        return False
    elif student_tests.tests < test_count:
        gently("You have not written enough unit tests.", label="Not Enough Student Unit Tests")
        return False
    elif student_tests.failures > 0:
        gently("Your unit tests are not passing.", label="Student Unit Tests Failing")
        return False
    return True
