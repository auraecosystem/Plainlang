import unittest

from plainlang.lexer import LexError, tokenize
from plainlang.parser import ParseError, parse
from plainlang.runtime import PlainlangRuntimeError, execute


class LexerTests(unittest.TestCase):
    def test_tokenizes_keywords_numbers_and_strings(self):
        kinds = [token.kind for token in tokenize('let answer = 42\\nprint("ok")')]
        self.assertEqual(kinds, ["IDENT", "IDENT", "OP", "NUMBER", "NEWLINE", "IDENT", "PUNCT", "STRING", "PUNCT", "EOF"])

    def test_reports_unexpected_characters(self):
        with self.assertRaises(LexError):
            tokenize("let x = @")


class ParserTests(unittest.TestCase):
    def test_parses_function_and_call(self):
        program = parse("function add(a, b) { return a + b }\\nlet x = add(2, 3)")
        self.assertEqual(len(program.statements), 2)

    def test_rejects_invalid_syntax(self):
        with self.assertRaises(ParseError):
            parse("let = 3")


class RuntimeTests(unittest.TestCase):
    def test_arithmetic_and_variables(self):
        output = []
        execute("let total = (2 + 3) * 4\\nprint(total)", output=lambda *v: output.append(" ".join(map(str, v))))
        self.assertEqual(output, ["20"])

    def test_function_return(self):
        output = []
        execute('function greet(name) { return "Hello, " + name }\\nprint(greet("Plainlang"))', output=lambda *v: output.append(" ".join(map(str, v))))
        self.assertEqual(output, ["Hello, Plainlang"])

    def test_boolean_comparison(self):
        output = []
        execute("print(5 >= 3)\\nprint(2 == 4)", output=lambda *v: output.append(v[0]))
        self.assertEqual(output, [True, False])

    def test_undefined_name_is_rejected_at_runtime(self):
        with self.assertRaises(PlainlangRuntimeError):
            execute("print(missing)")

    def test_division_by_zero_is_reported(self):
        with self.assertRaises(PlainlangRuntimeError):
            execute("print(4 / 0)")

    def test_function_arity_is_checked(self):
        with self.assertRaises(PlainlangRuntimeError):
            execute("function one(x) { return x }\\none()")


if __name__ == "__main__":
    unittest.main()
