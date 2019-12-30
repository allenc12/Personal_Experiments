#!/usr/bin/env python3

try:
    import typing
    import argparse
    import re
    import os
    import sys

    from pprint import pprint
    # from pycparser import c_parser, c_ast
except ModuleNotFoundError as ex:
    print(f"Error: {ex}")
    exit(1)


class NormeError(Exception):
    """Base class for exceptions in this module"""

    pass


class NormeWarning(NormeError):
    """Exception raised for non-fatal errors.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, lineno: int, column: int, expression: str, message: str):
        self.lineno = lineno
        self.column = column
        self.expression = expression
        self.message = message


class InvalidFileError(NormeError):
    """Exception raised for invalid files passed as input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression: str, message: str):
        self.expression = expression
        self.message = message


class NormeClient:
    """Class encapsulating the online and offline Norminette style checkers.

    Attributes:
        offline -- hue
    """
    def __init__(self, offline: bool = False):
        self.offline = offline


class Norme:
    """Class encapsulating the offline Norminette style checker.

    Attributes:
        filename -- input filename
        lines -- contents of the input file
    """

    def __init__(self, istty: bool = False):
        self._istty = istty
        self._filename = None
        self._lines = None
        self._function_count = 0
        self._variable_count = 0
        self._error_count = 0
        self._offline = 0
        self._checks = [
            self.CheckTopCommentHeader,
            self.CheckTypePrefixName,
            self.CheckOneInstructionPerLine,
            self.CheckPreprocessorIndentation,
            self.CheckIncludesBeforeFirstInstruction,
            self.CheckForbiddenSourceHeader,
            self.CheckColumnLength,
            self.CheckDoubleInclusion,
            self.CheckInclude,
            self.CheckTernaryOperator,
            # self.CheckBlock,
            # self.CheckForbiddenKeyword,
            # self.CheckKeywordSpacing,
            # self.CheckAlignment,
            # self.CheckMultipleSpaces,
            # self.CheckNamedParameters,
            # self.CheckReturnParentheses,
            # self.CheckIndentationMultiline,
            # self.CheckCommentsFormat,
            # self.CheckIndentationInsideFunction,
            # self.CheckOperatorSpacing,
            # self.CheckMultipleEmptyLines,
            # self.CheckDefine,
            # self.CheckUnaryOperator,
            # self.CheckBracketSpacing,
            # self.CheckFilename,
            # self.CheckParametersNumber,
            # self.CheckControlStructure,
            # self.CheckMultipleAssignation,
            # self.CheckFunctionSpacing,
            # self.CheckFunctionNumber,
            # self.CheckNestedTernary,
            # self.CheckBeginningOfLine,
            # self.CheckDeclarationCount,
            # self.CheckNumberOfLine,
            # self.CheckCase,
            # self.CheckTypeDeclarationSpacing,
            # self.CheckCallSpacing,
            # self.CheckDeclarationPlacement,
            # self.CheckSeparationChar,
            # self.CheckElseIf,
            # self.CheckNoArgFunction,
            # self.CheckGlobalTypePrefixName,
            # self.CheckEmptyLine,
            # self.CheckVla,
            # self.CheckCppComment,
            # self.CheckSpaceBetweenFunctions,
            # self.CheckArgumentSpacing,
            # self.CheckEndOfLine,
            # self.CheckNumberOfVariables,
            # self.CheckComma,
            # self.CheckParentSpacing,
            # self.CheckCommentsPlacement,
            # self.CheckDeclarationInstanciation,
            # self.CheckIndentationOutsideFunction,
        ]

    def printError(self, lineno: int = 1, column: int = 0, msg: str = "unexpected error"):
        if lineno is not None and column is not None:
            if self._istty:
                sys.stderr.write(f"{self._filename}:{lineno}:{column}: \033[1;91mError\033[0m - {msg}\n")
            else:
                sys.stderr.write(f"{self._filename}:{lineno}:{column}: Error - {msg}\n")
        else:
            if self._istty:
                sys.stderr.write(f"{self._filename}: \033[1;91mError\033[0m - {msg}\n")
            else:
                sys.stderr.write(f"{self._filename}: Error - {msg}\n")

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
        if len(self._lines) < 1:
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

    def CheckTernaryOperator(self):
        """Checks for spaces around conditional operators"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"[ \t]([^'\"\r\n\t\f\v ]+?([\?:])[^'\"\r\n\t\f\v ]+?)", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, fnd.regs[1][1] - 1, f"Missing space around '{fnd.group(2)}'")
                ret += 1
            ii += 1
        return ret

    def CheckBlock(self):
        """checks for newlines before blocks. i.e. '{}'"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckBlock")
                ret = 1
            ii += 1
        return ret

    def CheckForbiddenKeyword(self):
        """checks for presence of forbidden keywords"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"(for|switch|do)", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckForbiddenKeyword")
                ret = 1
            ii += 1
        return ret

    def CheckKeywordSpacing(self):
        """checks for spacing after return, while, break, continue,"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckKeywordSpacing")
                ret = 1
            ii += 1
        return ret

    def CheckAlignment(self):
        """Controls global and local scope alignment
        Global scope: function definitions and global variables are separate
        union definitions, typedef struct definitions must be aligned, see bup.h
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckAlignment")
                ret = 1
            ii += 1
        return ret

    def CheckMultipleSpaces(self):
        """Checks for multiple spaces when there should be one or tabs"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckMultipleSpaces")
                ret = 1
            ii += 1
        return ret

    def CheckNamedParameters(self):
        """Checks for unnamed parameters in function declarations in headers"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckNamedParameters")
                ret = 1
            ii += 1
        return ret

    def CheckReturnParentheses(self):
        """Checks that return statements are surrounded by parenthesis"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckReturnParentheses")
                ret = 1
            ii += 1
        return ret

    def CheckCommentsFormat(self):
        """Ensures comments are formatted correctly"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckCommentsFormat")
                ret = 1
            ii += 1
        return ret

    def CheckIndentationInsideFunction(self):
        """Checks for bad indentation inside of a function"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckIndentationInsideFunction")
                ret = 1
            ii += 1
        return ret

    def CheckOperatorSpacing(self):
        """Checks for single spaces surrounding binary operators"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckOperatorSpacing")
                ret = 1
            ii += 1
        return ret

    def CheckMultipleEmptyLines(self):
        """Checks for multiple empty lines"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckMultipleEmptyLines")
                ret = 1
            ii += 1
        return ret

    def CheckDefine(self):
        """chEcKs FoR deFIneS tHAt aRE COnsTant VAlUeS AnD dON't TAkE ARguMEnTs
        see test.c for multiple examples of nON-cONstAnT dEFiNeS
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckDefine")
                ret = 1
            ii += 1
        return ret

    def CheckUnaryOperator(self):
        """Checks for spaces around ! ~ - + * & . -> sizeof (int)
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckUnaryOperator")
                ret = 1
            ii += 1
        return ret

    def CheckBracketSpacing(self):
        """Checks for spaces around []
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckBracketSpacing")
                ret = 1
            ii += 1
        return ret

    def CheckFilename(self):
        """Checks that filename is unix_case
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckFilename")
                ret = 1
            ii += 1
        return ret

    def CheckParametersNumber(self):
        """Checks that no function has more than 4 parameters
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckParametersNumber")
                ret = 1
            ii += 1
        return ret

    def CheckMultipleAssignation(self):
        """Checks for the presence of multiple = operators.
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckMultipleAssignation")
                ret = 1
            ii += 1
        return ret

    def CheckFunctionSpacing(self):
        """Checks for: int cmp (int a, int b)
        however:
        int cmp\n\t(\n\t\tint a,\n\tint b\n)
        is valid
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckFunctionSpacing")
                ret = 1
            ii += 1
        return ret

    def CheckFunctionNumber(self):
        """Check for a maximum of 5 functions in a .c source file
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckFunctionNumber")
                ret = 1
            ii += 1
        return ret

    def CheckNestedTernary(self):
        """Check for nested conditional operators
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckNestedTernary")
                ret = 1
            ii += 1
        return ret

    def CheckBeginningOfLine(self):
        """Checks that lines only begin with \t or no whitespace
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckBeginningOfLine")
                ret = 1
            ii += 1
        return ret

    def CheckNumberOfLine(self):
        """Checks that functions are 25 lines or fewer
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckNumberOfLine")
                ret = 1
            ii += 1
        return ret

    def CheckCase(self):
        """Identifiers must be in unix_case
        not: `g_Flag' `_block' `__hasdf' `traverseList'
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckCase")
                ret = 1
            ii += 1
        return ret

    def CheckTypeDeclarationSpacing(self):
        """Checks that typedef is followed by one space, and the original type is
        followed by exclusively tabs up to the new type name.
        `typedef uint64_t\t\tt_u64;'
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckTypeDeclarationSpacing")
                ret = 1
            ii += 1
        return ret

    def CheckCallSpacing(self):
        """Checks that function calls have no spaces between the function name
        and parentheses `puts("str");', not `puts ("str")'
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckCallSpacing")
                ret = 1
            ii += 1
        return ret

    def CheckDeclarationPlacement(self):
        """Check that function variable declarations are at the beginning of the
        function body.
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckDeclarationPlacement")
                ret = 1
            ii += 1
        return ret

    def CheckSeparationChar(self):
        """Checks for spaces around commas
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckSeparationChar")
                ret = 1
            ii += 1
        return ret

    def CheckElseIf(self):
        """Checks that an else followed by an if is on the same line
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckElseIf")
                ret = 1
            ii += 1
        return ret

    def CheckNoArgFunction(self):
        """Checks that a function definition which takes no arguments is
        declared as `function(void)'
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckNoArgFunction")
                ret = 1
            ii += 1
        return ret

    def CheckGlobalTypePrefixName(self):
        """Checks that any global variable is declared with a name prefixed by
        `g_'
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckGlobalTypePrefixName")
                ret = 1
            ii += 1
        return ret

    def CheckEmptyLine(self):
        """Checks for single empty lines
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckEmptyLine")
                ret = 1
            ii += 1
        return ret

    def CheckVla(self):
        """Checks for variable length arrays
        Note: In the official norminette, this rule seems to be non-functional
        and fails to detect basic variable length arrays
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckVla")
                ret = 1
            ii += 1
        return ret

    def CheckCppComment(self):
        """Checks for C++ style comments
        // comment
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckCppComment")
                ret = 1
            ii += 1
        return ret

    def CheckSpaceBetweenFunctions(self):
        """Checks that only one empty line separates each function definition
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckSpaceBetweenFunctions")
                ret = 1
            ii += 1
        return ret

    def CheckArgumentSpacing(self):
        """Checks that arguments are separated by `, '
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckArgumentSpacing")
                ret = 1
            ii += 1
        return ret

    def CheckEndOfLine(self):
        """Checks for trailing whitespace
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckEndOfLine")
                ret = 1
            ii += 1
        return ret

    def CheckNumberOfVariables(self):
        """Checks that each function declares no more than 5 variables
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckNumberOfVariables")
                ret = 1
            ii += 1
        return ret

    def CheckComma(self):
        """Checks for usage of comma operator outside of function call/definitons, and compound literals
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckComma")
                ret = 1
            ii += 1
        return ret

    def CheckParentSpacing(self):
        """Checks for spacing around parentheses
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckParentSpacing")
                ret = 1
            ii += 1
        return ret

    def CheckCommentsPlacement(self):
        """Checks that comments are not inside of functions
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckCommentsPlacement")
                ret = 1
            ii += 1
        return ret

    def CheckDeclarationInstanciation(self):
        """Checks that non-static non-const variables are not declared and instantiated on the same line.
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckDeclarationInstaciation")
                ret = 1
            ii += 1
        return ret

    def CheckControlStructure(self):
        """Checks for newlines following control flow keywords:
        `if (flag) return (0);' will throw an error
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckControlStructure")
                ret = 1
            ii += 1
        return ret

    def CheckIndentationMultiline(self):
        """TODO: figure out what this checks for"""
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckIndentationMultiline")
                ret = 1
            ii += 1
        return ret

    def CheckDeclarationCount(self):
        """TODO: Still a mystery as to what declarations this counts
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckDeclarationCount")
                ret = 1
            ii += 1
        return ret

    def CheckIndentationOutsideFunction(self):
        """TODO: what the hell would one indent outside of a function?
        """
        if len(self._lines) < 1:
            return 0
        reg = re.compile(r"", re.RegexFlag.M)
        ii = 1
        ret = 0
        for ln in self._lines:
            fnd = reg.search(ln)
            if fnd is not None:
                self.printError(ii, 1, "CheckIndentationOutsideFunction")
                ret = 1
            ii += 1
        return ret

    def isValidFile(self, filename: str):
        ret = 1
        if filename is None:
            self.printError(lineno=None, column=None, msg="Invalid file")
            ret = 0
        elif not os.path.isfile(filename):
            self.printError(lineno=None, column=None, msg="Invalid file type")
            ret = 0
        elif re.match(r"\.[ch]$", filename, re.RegexFlag.M) is None:
            self.printError(lineno=None, column=None, msg="Invalid file extension")
            ret = 0
        return ret

    def checkFile(self, filename: str):
        self.isValidFile(filename)
        lines = open(filename).read().splitlines(keepends=True)
        if len(lines) < 12:
            self.printError(msg="Missing 42 header")
        else:
            if self.CheckTopCommentHeader():
                return 1
        lineno = 0
        for ln in lines[12:]:
            lineno += 1
        return 0

    def runChecks(self, opts):
        if len(self._lines) < 1:
            raise InvalidFileError("len(self._lines) < 1", "Empty file")
        total_errors = 0
        for fn in self._checks:
            if fn.__name__ not in opts.rules:
                total_errors += fn()
        return total_errors

    def checkFiles(self, opts):
        total_errors = 0
        for f in opts.files:
            if not self.isValidFile(f):
                continue
            self._filename = f
            if self._istty:
                print(f"\033[1;97mNorme: {self._filename}\033[0m\r", end="")
            else:
                print(f"Norme: {self._filename}")
            try:
                self._lines = open(self._filename).readlines()
                total_errors += self.runChecks(opts)
            except NormeError as ex:
                print(f"class Norme Error: {ex}")
            except Exception as ex:
                print(f"class Norme: Unexpected Exception: {ex}")
                raise
        return total_errors


def lst_append(lst: typing.List, *args):
    for arg in args:
        lst.append(arg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog=sys.argv[0], description="42SV style checker and enforcer")
    parser.add_argument("-v", "--version", help="Print version", action="version", version="Local version: 0.1.2")
    parser.add_argument("-l", "--local", help="Use offline local client", action="store_true")
    parser.add_argument("-c", "--nocolor", help="Disable color output", action="store_true")
    parser.add_argument("-d", "--debug", help="Enable debug output", action="store_true")
    parser.add_argument("-R", "--rules", help="Rules to disable, separated by commas")
    parser.add_argument("files", nargs="*", help="files and/or paths to process", metavar="FILES")
    parser.print_usage()

    args = parser.parse_args()
    istty = None
    if not args.nocolor:
        istty = os.isatty(sys.stdin.fileno())
    if len(args.files) < 1:
        print("Norme: no files specified, searching current directory recursively...")
        args.files = os.listdir(os.getcwd())
    else:
        lst = []
        for f in args.files:
            if os.path.isdir(f):
                lst_append(lst, *os.listdir(f))
            else:
                lst.append(f)
        args.files = lst

    np = Norme(istty=istty)
    np.checkFiles(args)
