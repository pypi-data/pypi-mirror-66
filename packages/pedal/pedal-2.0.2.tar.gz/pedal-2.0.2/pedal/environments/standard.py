"""
A simple environment for quickly running Pedal code.

Parameter Order
    Files
    MainFile
    MainCode
    User
    Assignment
    Course
    Execution
    InstructorFile

Get submission (Main Code, Main Filename, Other Code, Other Settings) from
    as argument
        main_code, main_file
        files = {'answer.py': code}

    sys.args
        filename
        parameter
    global variable
    filename

Provide Output
    STDOUT
    Global variable
    Filename
    Returned result


"""

import sys

from pedal.assertions import resolve_all
from pedal.core.commands import contextualize_report
from pedal.core.submission import Submission
from pedal.source import verify
from pedal.cait import parse_program
from pedal.sandbox import run
from pedal.tifa import tifa_analysis
from pedal.resolvers import simple


def parse_argv():
    if len(sys.argv) == 2:
        main_file = sys.argv[1]
        with open(main_file) as main_file_handle:
            main_code = main_file_handle.read()
        return sys.argv[0], {main_file: main_code}, main_file, main_code, None, None, None, None
    #elif len(sys.argv) == 3:
    else:
        return sys.argv
    # TODO: Finish handling arguments intelligently


def setup_pedal(files=None, main_file='answer.py', main_code=None,
                user=None, assignment=None, course=None, execution=None,
                instructor_file='on_run.py', skip_tifa=False, set_success=True):
    if files is None and main_code is None:
        instructor_file, files, main_file, main_code, user, assignment, course, execution = parse_argv()
    elif files is None:
        files = {main_file: main_code}
    elif main_code is None:
        main_code = files[main_file]
    contextualize_report(Submission(files, main_file, main_code, user, assignment, course, execution,
                                    instructor_file))
    verify()
    ast = parse_program()
    if not skip_tifa:
        tifa = tifa_analysis()
    student = run(threaded=True, raise_exceptions=True)
    student.report_exceptions_mode = True

    def print_resolve(*args, **kwargs):
        resolve_all(set_successful=set_success, no_phases_is_success=True)
        result = simple.resolve(*args, **kwargs)
        #print("Feedback Label:", result.label)
        print("Title:", result.title)
        print("Label:", result.label)
        print("Score:", result.score)
        print("Message:", result.message)
        return result

    return ast, student, print_resolve
