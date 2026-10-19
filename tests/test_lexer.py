
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parents[1]
LEXER_FILE = PROJECT_DIR / "html.l"
REPORT_FILE = PROJECT_DIR / "test_report.json"


def find_executable(env_name, executable_name, fallback=None):
    """Find an executable using an environment variable or PATH."""
    configured_path = os.environ.get(env_name)

    if configured_path:
        return configured_path

    path = shutil.which(executable_name)
    if path:
        return path

    if fallback and Path(fallback).exists():
        return fallback

    raise FileNotFoundError(
        f"Could not find {executable_name}. "
        f"Add it to PATH or set the {env_name} environment variable."
    )


class LexerTests(unittest.TestCase):
    results = []
    temp_dir = None
    lexer_executable = None

    @classmethod
    def setUpClass(cls):
        """Compile the Flex lexer once before running the tests."""
        if not LEXER_FILE.exists():
            raise FileNotFoundError(f"Lexer source not found: {LEXER_FILE}")

        flex = find_executable(
            "FLEX",
            "flex",
            r"C:\msys64\usr\bin\flex.exe",
        )
        gcc = find_executable("CC", "gcc")

        cls.temp_dir = tempfile.TemporaryDirectory()
        build_dir = Path(cls.temp_dir.name)

        generated_c = build_dir / "lex.yy.c"
        cls.lexer_executable = build_dir / "html.exe"

        subprocess.run(
            [flex, "-o", str(generated_c), str(LEXER_FILE)],
            check=True,
            capture_output=True,
            text=True,
        )

        subprocess.run(
            [gcc, str(generated_c), "-o", str(cls.lexer_executable)],
            check=True,
            capture_output=True,
            text=True,
        )

    @classmethod
    def tearDownClass(cls):
        """Save the test results after the suite finishes."""
        REPORT_FILE.write_text(
            json.dumps(cls.results, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

        print(f"\nTest report saved to: {REPORT_FILE}")

        if cls.temp_dir:
            cls.temp_dir.cleanup()

    def check_lexer(self, input_text, expected_fragments):
        """Run the lexer, record its output, and check the expectations."""
        process = subprocess.run(
            [str(self.lexer_executable)],
            input=input_text,
            capture_output=True,
            text=True,
            timeout=10,
        )

        generated_output = process.stdout
        errors = []

        if process.returncode != 0:
            errors.append(
                f"Lexer exited with return code {process.returncode}"
            )

        if process.stderr.strip():
            errors.append(f"Standard error: {process.stderr.strip()}")

        missing = [
            fragment
            for fragment in expected_fragments
            if fragment not in generated_output
        ]

        if missing:
            errors.append(
                "Missing expected output fragments: "
                + repr(missing)
            )

        passed = not errors

        self.results.append({
            "test_name": self.id().split(".")[-1],
            "input": input_text,
            "expected_output": expected_fragments,
            "generated_output": generated_output,
            "result": "PASS" if passed else "FAIL",
            "error": "; ".join(errors) if errors else None,
        })

        self.assertTrue(
            passed,
            "\n".join(errors)
            + f"\nActual output:\n{generated_output}",
        )

    def test_doctype(self):
        self.check_lexer(
            "<!DOCTYPE html>",
            ["DOCTYPE"],
        )

    def test_complex_doctype(self):
        self.check_lexer(
            '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" '
            '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
            ["DOCTYPE"],
        )

    def test_comment(self):
        self.check_lexer(
            "<!-- a comment -->",
            ["COMMENT"],
        )

    def test_multiline_comment(self):
        self.check_lexer(
            "<!-- first line\nsecond line -->",
            ["COMMENT"],
        )

    def test_tags_inside_comment_are_ignored(self):
        self.check_lexer(
            "<!-- <div>hidden</div> -->",
            ["COMMENT"],
        )

        output = self.results[-1]["generated_output"]
        self.assertNotIn("OPENING div TAG", output)
        self.assertNotIn("CLOSING </div> TAG", output)

    def test_opening_tag(self):
        self.check_lexer(
            "<div>",
            ["OPENING div TAG"],
        )

    def test_one_letter_tag(self):
        self.check_lexer(
            "<p>",
            ["OPENING p TAG"],
        )

    def test_closing_tag(self):
        self.check_lexer(
            "</div>",
            ["CLOSING </div> TAG"],
        )

    def test_self_closing_tag(self):
        self.check_lexer(
            "<img/>",
            ["SELF CLOSING img TAG"],
        )

    def test_double_quoted_attribute(self):
        self.check_lexer(
            '<div class="container">',
            ["ATTRIBUTE NAME", 'ATTRIBUTE VALUE "container"',
             "OPENING div TAG"],
        )

    def test_single_quoted_attribute(self):
        self.check_lexer(
            "<div class='container'>",
            ["ATTRIBUTE NAME", "ATTRIBUTE VALUE 'container'",
             "OPENING div TAG"],
        )

    def test_unquoted_attribute(self):
        self.check_lexer(
            "<div id=main>",
            ["ATTRIBUTE NAME", "ATTRIBUTE VALUE main",
             "OPENING div TAG"],
        )

    def test_boolean_attribute(self):
        self.check_lexer(
            "<input disabled>",
            ["BOOLEAN ATTRIBUTE", "OPENING input TAG"],
        )

    def test_multiple_attributes(self):
        self.check_lexer(
            '<div id="main" class="box">',
            ["ATTRIBUTE NAME", 'ATTRIBUTE VALUE "main"',
             'ATTRIBUTE VALUE "box"', "OPENING div TAG"],
        )

    def test_punctuation_in_attribute_value(self):
        self.check_lexer(
            '<a href="https://example.com/page?id=1">',
            ['ATTRIBUTE VALUE "https://example.com/page?id=1"',
             "OPENING a TAG"],
        )

    def test_self_closing_tag_with_attribute(self):
        self.check_lexer(
            '<img src="photo.png"/>',
            ['ATTRIBUTE VALUE "photo.png"',
             "SELF CLOSING img TAG"],
        )

    def test_multiple_tags(self):
        self.check_lexer(
            "<html><body></body></html>",
            [
                "OPENING html TAG",
                "OPENING body TAG",
                "CLOSING </body> TAG",
                "CLOSING </html> TAG",
            ],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
