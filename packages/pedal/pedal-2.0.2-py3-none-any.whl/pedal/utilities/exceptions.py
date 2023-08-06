import traceback
import os

BuiltinKeyError = KeyError


class KeyError(BuiltinKeyError):
    """
    A version of KeyError that replaces the built-in with one small
    modification: when printing an explanatory message, the message is not
    rendered as a tuple. Because that's stupid and the fact that it made it
    into CPython is just rude.

    See Also:
        https://github.com/python/cpython/blob/master/Objects/exceptions.c#L1556
    """
    __module__ = "builtins"

    def __init__(self, original, message):
        for field in ['__cause__', '__traceback__', '__context__']:
            if hasattr(original, field):
                setattr(self, field, getattr(original, field))
            else:
                setattr(self, field, None)
        self.message = message

    def __str__(self):
        return self.message


def add_context_to_error(e, message):
    """

    Args:
        e:
        message:

    Returns:

    """
    if isinstance(e, BuiltinKeyError):
        new_args = repr(e.args[0]) + message
        e = KeyError(e, new_args)
        e.args = tuple([new_args])
    elif isinstance(e, OSError):
        # TODO: Investigate OSError, since they have so many args.
        #       Might be weird.
        e.args = tuple([e.args[0] + message])
        return e
    elif hasattr(e, 'args') and e.args:
        e.args = tuple([e.args[0] + message])
    return e


class ExpandedTraceback:
    """
    Class for reformatting tracebacks to have more pertinent information.
    """

    def __init__(self, exception, exc_info, full_traceback,
                 instructor_filename, line_offset, student_filename,
                 original_code_lines):
        """
        Args:
            exception (Exception): The exception that was raised.
            exc_info (ExcInfo): The result of sys.exc_info() when the exception
                was raised.
            full_traceback (bool): Whether or not to provide the full traceback
                or just the parts relevant to students.
            instructor_filename (str): The name of the instructor file, which
                can be used to avoid reporting instructor code in the
                traceback.
        """
        self.line_offset = line_offset
        self.exception = exception
        self.exc_info = exc_info
        self.full_traceback = full_traceback
        self.instructor_filename = instructor_filename
        self.student_filename = student_filename
        self.line_number = traceback.extract_tb(exc_info[2])[-1][1]
        self.original_code_lines = original_code_lines

    @staticmethod
    def _clean_traceback_line(line):
        return line.replace(', in <module>', '', 1)

    def format_exception(self, preamble=""):
        """

        Args:
            preamble:

        Returns:

        """
        if not self.exception:
            return ""
        if isinstance(self.exception, TimeoutError):
            return str(self.exception)
        cl, exc, tb = self.exc_info
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next
        length = self._count_relevant_tb_levels(tb)
        tb_e = traceback.TracebackException(cl, self.exception, tb, limit=length,
                                            capture_locals=False)
        # print(list(), file=x)
        for frame in tb_e.stack:
            if frame.filename == os.path.basename(self.student_filename):
                frame.lineno += self.line_offset
            if frame.lineno - 1 < len(self.original_code_lines):
                frame._line = self.original_code_lines[frame.lineno - 1]
            else:
                frame._line = "*line missing*"
        lines = [self._clean_traceback_line(line)
                 for line in tb_e.format()]
        lines[0] = "Traceback:\n"
        return preamble + ''.join(lines)

    def _count_relevant_tb_levels(self, tb):
        length = 0
        while tb and not self._is_relevant_tb_level(tb):
            length += 1
            tb = tb.tb_next
        return length

    def _is_relevant_tb_level(self, tb):
        """
        Determines if the give part of the traceback is relevant to the user.

        Returns:
            boolean: True means it is NOT relevant
        """
        # Are in verbose mode?
        if self.full_traceback:
            return False
        filename, a_, b_, _ = traceback.extract_tb(tb, limit=1)[0]
        # Is the error in the student file?
        if filename == self.student_filename:
            return False
        # Is the error in the instructor file?
        if filename == self.instructor_filename:
            return True
        # Is the error in this test directory?
        current_directory = os.path.dirname(os.path.realpath(__file__))
        if filename.startswith(current_directory):
            return True
        # Is the error related to a file in the parent directory?
        # parent_directory = os.path.dirname(current_directory)
        # TODO: Currently we don't refer to this?
        # Is the error in a local file?
        if filename.startswith('.'):
            return False
        # Is the error in an absolute path?
        if not os.path.isabs(filename):
            return False
        # Okay, it's not a student related file
        return True
