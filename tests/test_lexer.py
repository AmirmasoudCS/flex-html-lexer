
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
SOURCE_FILE = PROJECT_DIR / "html.l"

FLEX = (
    os.environ.get("FLEX")
    or shutil.which("flex")
    or r"C:\msys64\usr\bin\flex.exe"
)

GCC = os.environ.get("CC") or shutil.which("gcc")


class TestHTMLLexer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not SOURCE_FILE.exists():
            raise FileNotFoundError(
                f"Lexer source not found: {SOURCE_FILE}"
            )

        if not Path(FLEX).exists() and not shutil.which(FLEX):
            raise RuntimeError(
                "Flex was not found. Install Flex or set the FLEX "
                "environment variable to its executable path."
            )

        if not GCC:
            raise RuntimeError(
                "GCC was not found. Make sure GCC is available on PATH."
            )

        cls.build_dir = tempfile.TemporaryDirectory()
        build_path = Path(cls.build_dir.name)

        cls.scanner_file = build_path / "lex.yy.c"
        cls.executable = build_path / (
            "html.exe" if os.name == "nt" else "html"
        )

        subprocess.run(
            [
                FLEX,
                "-o",
                str(cls.scanner_file),
                str(SOURCE_FILE),
            ],
            cwd=build_path,
            check=True,
            capture_output=True,
            text=True,
        )

        subprocess.run(
            [
                GCC,
                str(cls.scanner_file),
                "-o",
                str(cls.executable),
            ],
            cwd=build_path,
            check=True,
            capture_output=True,
            text=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.build_dir.cleanup()

    def run_lexer(self, html):
        result = subprocess.run(
            [str(self.executable)],
            input=html,
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        return result.stdout

    def test_doctype(self):
        output = self.run_lexer("<!DOCTYPE html>")

        self.assertIn("DOCTYPE", output)

    def test_complex_doctype(self):
        html = (
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '
            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        )

        output = self.run_lexer(html)

        self.assertIn("DOCTYPE", output)

    def test_comment(self):
        output = self.run_lexer("<!-- Hello, world! -->")

        self.assertIn("COMMENT", output)

    def test_tags_inside_comment_are_ignored(self):
        html = "<!-- <div>hidden</div> -->"

        output = self.run_lexer(html)

        self.assertIn("COMMENT", output)
        self.assertNotIn("OPENING", output)
        self.assertNotIn("CLOSING", output)

    def test_multiline_comment(self):
        html = (
            "<!-- First line\n"
            "<div>Still inside the comment</div>\n"
            "Last line -->"
        )

        output = self.run_lexer(html)

        self.assertIn("COMMENT", output)
        self.assertNotIn("OPENING", output)
        self.assertNotIn("CLOSING", output)

    def test_opening_tag(self):
        output = self.run_lexer("<div>")

        self.assertIn("OPENING div TAG", output)

    def test_single_character_tag_name(self):
        output = self.run_lexer("<p>")

        self.assertIn("OPENING p TAG", output)

    def test_closing_tag(self):
        output = self.run_lexer("</div>")

        self.assertIn("CLOSING </div> TAG", output)

    def test_self_closing_tag(self):
        output = self.run_lexer("<img />")

        self.assertIn("SELF CLOSING img TAG", output)

    def test_double_quoted_attribute(self):
        output = self.run_lexer('<div class="container">')

        self.assertIn("ATTRIBUTE NAME", output)
        self.assertIn('ATTRIBUTE VALUE "container"', output)
        self.assertIn("OPENING div TAG", output)

    def test_single_quoted_attribute(self):
        output = self.run_lexer("<div id='header'>")

        self.assertIn("ATTRIBUTE NAME", output)
        self.assertIn("ATTRIBUTE VALUE 'header'", output)
        self.assertIn("OPENING div TAG", output)

    def test_unquoted_attribute(self):
        output = self.run_lexer("<img width=300>")

        self.assertIn("ATTRIBUTE NAME", output)
        self.assertIn("ATTRIBUTE VALUE 300", output)
        self.assertIn("OPENING img TAG", output)

    def test_boolean_attribute(self):
        output = self.run_lexer("<input disabled>")

        self.assertIn("BOOLEAN ATTRIBUTE", output)
        self.assertIn("disabled", output)
        self.assertIn("OPENING input TAG", output)

    def test_multiple_attributes(self):
        html = (
            '<div class="main-container" '
            "id='header' data-id=123 disabled>"
        )

        output = self.run_lexer(html)

        self.assertIn("ATTRIBUTE VALUE \"main-container\"", output)
        self.assertIn("ATTRIBUTE VALUE 'header'", output)
        self.assertIn("ATTRIBUTE VALUE 123", output)
        self.assertIn("BOOLEAN ATTRIBUTE", output)
        self.assertIn("OPENING div TAG", output)

    def test_attribute_value_with_punctuation(self):
        html = '<a href="https://example.com/page-1.html">'

        output = self.run_lexer(html)

        self.assertIn(
            'ATTRIBUTE VALUE "https://example.com/page-1.html"',
            output,
        )

    def test_self_closing_tag_with_attribute(self):
        output = self.run_lexer('<img src="photo.png" />')

        self.assertIn('ATTRIBUTE VALUE "photo.png"', output)
        self.assertIn("SELF CLOSING img TAG", output)

    def test_multiple_tags(self):
        html = "<div></div><p></p>"

        output = self.run_lexer(html)

        self.assertIn("OPENING div TAG", output)
        self.assertIn("CLOSING </div> TAG", output)
        self.assertIn("OPENING p TAG", output)
        self.assertIn("CLOSING </p> TAG", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
