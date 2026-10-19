# flex-html-lexer

## Overview

A lightweight HTML lexical analyzer implemented in C using Flex. The project demonstrates lexical analysis through regular expressions, pattern matching, and start conditions.

## Features

- DOCTYPE declaration recognition
- HTML comment detection
- Opening, closing, and self-closing tag recognition
- Attribute name recognition
- Double-quoted, single-quoted, and unquoted attribute values
- Boolean attribute recognition

## Technologies

- **Flex:** Lexical analyzer generation
- **C:** Token recognition actions
- **Python unittest:** Automated testing

## Building and Running

Requirements: Flex, GCC, and Python 3.

Generate the C source and compile the analyzer:

```powershell
flex -o lex.yy.c html.l
gcc lex.yy.c -o html.exe
```

Run the analyzer interactively:

```powershell
.\html.exe
```

Alternatively, process an HTML file:

```powershell
Get-Content .\example.html -Raw | .\html.exe
```

## Testing

Run the test suite from the project root:

```powershell
python -m unittest discover -s tests -v
```

The tests cover DOCTYPE declarations, comments, tags, and attribute variations. The suite generates `test_report.json`, containing each test's input, expected output fragments, actual output, and result.

All current test cases pass.

## Limitations

This project recognizes a subset of HTML constructs and is not a complete HTML parser or validator. Text content is not explicitly classified, tag nesting is not validated, and malformed HTML is not comprehensively handled.