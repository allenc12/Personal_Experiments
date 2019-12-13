#!/usr/bin/env python3
from pycparser import c_parser, c_ast
import argparse, re, os, sys


class NormeError(Exception):
    """Base class for exceptions in this module"""

    pass


class InputError(NormeError):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class InvalidFileError(NormeError):
    """Exception raised for invalid files passed as input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class TransitionError(NormeError):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message


class Norme:
    """Class encapsulating the Norminette style checker.

    Attributes:
        filename -- input filename, defaults to 'butts.c'
    """

    def __init__(self, filename="butts.c"):
        ch = filename[filename.rindex(".") + 1 :]
        if ch != "c" and ch != "h":
            raise InvalidFileError(f"!(ch({ch}) =~ r'[ch]'", "Invalid file extension")
        self._filename = filename
        self._lines = None
        self._function_count = 0
        self._variable_count = 0
        self._error_count = 0
        try:
            with open(filename, "r") as fr:
                self._lines = [l for l in fr.readlines()]
        except Exception as ex:
            print(f"class Norme: Unexpected Exception: {ex}")
            return None
        self._checks = None

    def printError(self, lineno=1, column=0, msg="unexpected error"):
        sys.stderr.write(f"{self._filename}:{lineno}:{column}: Error - {msg}\n")

    def CheckTypePrefixName(self):
        if len(self._lines) < 1:
            return 0
        reg = re.compile(
            r"^typedef(\s[\w\s()\*,]+?){1,}\s+?((t_)?\w+?(\[\d*?\])?);$", re.RegexFlag.M
        )
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None and fnd.group(2)[:2] != "t_":
                self.printError(
                    ii,
                    ln.index(fnd.group(2)),
                    f"typedef '{fnd.group(2)}' must begin with 't_'",
                )
                ret += 1
            ii += 1
        return ret

    def CheckOneInstructionPerLine(self):
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r'^(([^\'"\n]*;){2,})$', re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(
                    ii,
                    fnd.regs[1][1] - 1,
                    "multiple basic C operations on a single line",
                )
                ret += 1
            ii += 1
        return ret

    def CheckPreprocessorIndentation(self):
        if len(self._lines) < 1:
            return 0
        reg = re.compile(
            r"^(#(\s*?)((if|elif|ifndef|define|include|error|undef|warning|include_next|ident|undef|pragma|push|pop|line|else|endif)((\s+?)[^#]*?)?))$",
            re.RegexFlag.M,
        )
        inc = re.compile(
            r"^(#(\s*?)((if|elif|ifdef|ifndef|else)((\s+?)[^#]*?)?))$", re.RegexFlag.M
        )
        dec = re.compile(r"^(#(\s*?)((endif)((\s+?)[^#]*?)?))$", re.RegexFlag.M)
        ii = 1
        ret = 0
        indent = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if inc.search(ln) is not None:
                indent += 1
            if dec.search(ln) is not None:
                indent -= 1
            if fnd is not None:
                chk = len(fnd.group(2))
                if inc.search(ln) is not None:
                    chk += 1
                if chk != indent:
                    self.printError(
                        ii, 1, f"expected {indent} spaces, found {len(fnd.group(2))}"
                    )
                    ret += 1
            ii += 1
        return ret

    def CheckIncludesBeforeFirstInstruction(self):
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r'^#\s*?include [<"][\w/]+?[>"]$', re.RegexFlag.M)
        first_inc = 0
        first_loc = 0
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                first_inc = ii
            elif re.search(r"^\s*?\w+?", ln) is not None:
                first_loc = ii
            if first_inc != 0 and first_loc != 0 and not first_inc < first_loc:
                self.printError(ii, 1, f"includes must come first")
                ret += 1
            ii += 1
        return ret

    def CheckForbiddenSourceHeader(self):
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r'^#\s*?include [<"][\.\w/]+\.c[>"]$', re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(
                    ii, ln.index('"'), "including C source files is forbidden"
                )
                ret += 1
            ii += 1
        return ret

    def CheckColumnLength(self):
        if len(self._lines) < 1:
            return 0
        ii = 1
        ret = 0
        for ln in self._lines:
            if len(ln.expandtabs(4)) > 81:
                self.printError(ii, 81, "line greater than 80 columns")
                ret += 1
            ii += 1
        return ret

    def CheckTopCommentHeader(self):
        if len(self._lines) < 1:
            return 0
        lines = self._lines[0:13]
        ret = 0
        if re.match(r"^/\* \*{74} \*/$", lines[0], re.RegexFlag.M) is None:
            ret += 1
            self.printError(1, 1, "Invalid header")
        if re.match(r"^/\* {76}\*/$", lines[1], re.RegexFlag.M) is None:
            ret += 1
            self.printError(2, 1, "Invalid header")
        if re.match(r"^/\* {56}::: {6}:{8}   \*/$", lines[2], re.RegexFlag.M) is None:
            ret += 1
            self.printError(3, 1, "Invalid header")
        if (
            re.match(
                r"^/\*   (\w+\.[ch]) {,51}:\+: {6}:\+:    :\+:   \*/$",
                lines[3],
                re.RegexFlag.M,
            )
            is None
        ):
            ret += 1
            self.printError(4, 1, "Invalid header")
        if (
            re.match(r"^/\* {52}\+:\+ \+:\+ {9}\+:\+ {5}\*/$", lines[4], re.RegexFlag.M)
            is None
        ):
            ret += 1
            self.printError(5, 1, "Invalid header")
        if (
            re.match(
                r"^/\*   By: \w+? <\w+@\w+(\.\w+?)+?> {,40}\+#\+  \+:\+ {7}\+#\+ {8}\*/$",
                lines[5],
                re.RegexFlag.M,
            )
            is None
        ):
            print(lines[5])
            ret += 1
            self.printError(6, 1, "Invalid header")
        if (
            re.match(
                r"^/\* {48}\+#\+#\+#\+#\+#\+   \+#\+ {11}\*/$", lines[6], re.RegexFlag.M
            )
            is None
        ):
            ret += 1
            self.printError(7, 1, "Invalid header")
        if (
            re.match(
                r"^/\*   Created: \d{4}/\d\d/\d\d \d\d:\d\d:\d\d by \w+? {,18}#\+#    #\+# {13}\*/$",
                lines[7],
                re.RegexFlag.M,
            )
            is None
        ):
            ret += 1
            self.printError(8, 1, "Invalid header")
        if (
            re.match(
                r"^/\*   Updated: \d{4}/\d\d/\d\d \d\d:\d\d:\d\d by \w+? {,17}###   ########.fr {7}\*/$",
                lines[8],
                re.RegexFlag.M,
            )
            is None
        ):
            ret += 1
            self.printError(9, 1, "Invalid header")
        if re.match(r"^/\* {76}\*/$", lines[9], re.RegexFlag.M) is None:
            ret += 1
            self.printError(10, 1, "Invalid header")
        if re.match(r"^/\* \*{74} \*/$", lines[10], re.RegexFlag.M) is None:
            ret += 1
            self.printError(11, 1, "Invalid header")
        if lines[11] != "\n":
            ret += 1
            self.printError(12, 1, "Header must be followed by an empty line")
        if lines[12] == "\n":
            ret += 1
            self.printError(13, 1, "Header must be followed by a single empty line")
        return ret

    def CheckDoubleInclusion(self):
        if len(self._lines) < 1 or self._filename[-1] != "h":
            return 0
        ret = 0
        define = self._filename
        if "/" in define:
            define = define[define.rindex("/")+1]
        define = define.upper().replace(".", "_")
        lines = self._lines[12:]
        if lines[0] != "#ifndef "+define+"\n":
            self.printError(14, 1, "Include guard must be of the form 'FILENAME_H'")
            ret += 1
        if lines[1] != "# define "+define+"\n":
            self.printError(15, 1, "Include guard must be of the form 'FILENAME_H'")
            ret += 1
        if lines[-1] != "#endif\n":
            self.printError(len(self._lines)-1, 1, "Missing include guard '#endif'")
            ret += 1
        return ret

    def CheckInclude(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r'^#\s*?include [<"]\w+\.c[>"]$', re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            inc = reg.search(ln)
            if inc is not None:
                self.printError(
                    ii, ln.index('"'), "including C source files is forbidden"
                )
                ret += 1
            ii += 1
        return ret

    def CheckTernaryOperator(self):  # Checks for spaces around conditional operators
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, fnd.regs[1][1] - 1, "CheckTernaryOperator")
                ret += 1
            ii += 1
        return ret

    def CheckBlock(self):  # checks for newlines before blocks. i.e. '{}'
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckForbiddenKeyword(self):  # checks for presence of forbidden keywords
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckKeywordSpacing(self):  # checks for spacing after return, while, break, continue,
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckAlignement(self):  #
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckMultipleSpaces(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckNamedParameters(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckReturnParentheses(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckIndentationMultiline(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckCommentsFormat(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckIndentationInsideFunction(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckOperatorSpacing(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckMultipleEmptyLines(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckDefine(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckUnaryOperator(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckBracketSpacing(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckFilename(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckParametersNumber(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckControlStructure(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckMultipleAssignation(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckFunctionSpacing(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckFunctionNumber(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckNestedTernary(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckBeginningOfLine(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckDeclarationCount(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckNumberOfLine(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckCase(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckTypeDeclarationSpacing(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckCallSpacing(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckDeclarationPlacement(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckSeparationChar(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckElseIf(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckNoArgFunction(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckGlobalTypePrefixName(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckEmptyLine(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckVla(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckCppComment(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckSpaceBetweenFunctions(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckArgumentSpacing(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckEndOfLine(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckNumberOfVariables(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckComma(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckParentSpacing(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckCommentsPlacement(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckDeclarationInstanciation(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def CheckIndentationOutsideFunction(self):
        if len(self._lines) < 1 or 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "TODO")
                ret = 1
            ii += 1
        return ret

    def runChecks(self):
        self._checks = [
            self.CheckInclude,
            self.CheckTypePrefixName,
            self.CheckOneInstructionPerLine,
            self.CheckTernaryOperator,
            self.CheckPreprocessorIndentation,
            self.CheckIncludesBeforeFirstInstruction,
            self.CheckForbiddenSourceHeader,
            self.CheckColumnLength,
            self.CheckBlock,
            self.CheckForbiddenKeyword,
            self.CheckKeywordSpacing,
            self.CheckAlignement,
            self.CheckMultipleSpaces,
            self.CheckNamedParameters,
            self.CheckReturnParentheses,
            self.CheckIndentationMultiline,
            self.CheckCommentsFormat,
            self.CheckIndentationInsideFunction,
            self.CheckOperatorSpacing,
            self.CheckMultipleEmptyLines,
            self.CheckDefine,
            self.CheckUnaryOperator,
            self.CheckBracketSpacing,
            self.CheckFilename,
            self.CheckParametersNumber,
            self.CheckControlStructure,
            self.CheckMultipleAssignation,
            self.CheckFunctionSpacing,
            self.CheckFunctionNumber,
            self.CheckNestedTernary,
            self.CheckBeginningOfLine,
            self.CheckDeclarationCount,
            self.CheckNumberOfLine,
            self.CheckCase,
            self.CheckDoubleInclusion,
            self.CheckTypeDeclarationSpacing,
            self.CheckCallSpacing,
            self.CheckDeclarationPlacement,
            self.CheckSeparationChar,
            self.CheckTopCommentHeader,
            self.CheckElseIf,
            self.CheckNoArgFunction,
            self.CheckGlobalTypePrefixName,
            self.CheckEmptyLine,
            self.CheckVla,
            self.CheckCppComment,
            self.CheckSpaceBetweenFunctions,
            self.CheckArgumentSpacing,
            self.CheckEndOfLine,
            self.CheckNumberOfVariables,
            self.CheckComma,
            self.CheckParentSpacing,
            self.CheckCommentsPlacement,
            self.CheckDeclarationInstanciation,
            self.CheckIndentationOutsideFunction,
        ]
        total_errors = 0
        print(f"\033[1mNorme: {self._filename}\033[0m")
        for fn in self._checks:
            total_errors += fn()
        return total_errors


def main(argv):
    argc = len(argv)
    if argc > 1:
        lst = argv[1:]
    else:
        lst = ["bep.c"]
    for fn in lst:
        np = Norme(fn)
        np.runChecks()


if __name__ == "__main__":
    main(sys.argv)
