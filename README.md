# flex-html-lexer

## Overview

This project is a lexical analyzer built using **Flex** that identifies and classifies basic HTML structures.

The goal is to understand how lexical analysis works by applying regular expressions and pattern matching to HTML source code. The analyzer recognizes common HTML constructs, including tags, attributes, comments, document type declarations, and text content.

This project is developed as part of a university assignment to practice lexical analyzer design and implementation.

## Project Requirements

The analyzer is expected to recognize the following HTML components:

- **DOCTYPE declaration:** Identifies the HTML document type declaration.
- **HTML comments:** Detects comments enclosed between `<!--` and `-->`.
- **Text content:** Identifies ordinary text outside HTML tags and comments.
- **Attribute names:** Recognizes attribute names such as `class`, `id`, `src`, and `href`.
- **Attribute values:** Recognizes attribute values, including single-quoted, double-quoted, and potentially unquoted values.
- **Tag names:** Identifies HTML tag names such as `html`, `body`, `div`, and `p`.
- **Opening tags:** Recognizes opening tags such as `<div>` and `<p>`.
- **Closing tags:** Recognizes closing tags such as `</div>` and `</p>`.
- **Self-closing tags:** Identifies tags ending with `/>`, such as `<img />`.

## Example HTML Input

The following example contains all the main constructs the analyzer is expected to recognize.

```html
<!DOCTYPE html>

<!-- This is an HTML comment -->

<html lang="en">
    <body>
        <h1 class="title">Hello World</h1>

        <a href="https://example.com" target='_blank'>
            Visit Example
        </a>

        <img src="photo.png" alt="Photo" />
    </body>
</html>
```

## Analysis of the Example

### 1. DOCTYPE Declaration

```html
<!DOCTYPE html>
```

**Expected recognition:** DOCTYPE declaration.

The analyzer should identify this construct as a document type declaration rather than an ordinary HTML tag or text content.

### 2. HTML Comment

```html
<!-- This is an HTML comment -->
```

**Expected recognition:** HTML comment.

HTML comments begin with `<!--` and end with `-->`. The analyzer should recognize the entire comment as one construct.

Content inside a comment should not be interpreted as actual HTML tags. For example, `<div>` inside a comment should not be reported as an opening tag.

### 3. Opening Tag

```html
<body>
```

**Expected recognition:**
- Opening tag
- Tag name: `body`

An opening tag begins with `<`, contains a tag name, and ends with `>`.

Other examples include `<html>`, `<div>`, and `<p>`.

### 4. Closing Tag

```html
</body>
```

**Expected recognition:**
- Closing tag
- Tag name: `body`

A closing tag begins with `</` and ends with `>`. It indicates the end of an HTML element.

The analyzer should distinguish closing tags from opening tags even though both contain tag names.

### 5. Tag Name

```html
<h1>
```

**Expected recognition:** Tag name: `h1`.

A tag name identifies the type of HTML element. Other examples include `html`, `body`, `div`, `p`, `a`, and `img`.

The tag name should be distinguished from the attributes that may follow it.

### 6. Attribute Names and Values

```html
<h1 class="title">
```

**Expected recognition:**
- Opening tag
- Tag name: `h1`
- Attribute name: `class`
- Attribute value: `title`

Attributes provide additional information about an HTML element. An attribute generally consists of a name, an equals sign, and a value.

The following example demonstrates multiple attributes and different quoting styles:

```html
<a href="https://example.com" target='_blank'>
```

Expected components:

| Component | Value |
|---|---|
| Tag name | `a` |
| Attribute name | `href` |
| Attribute value | `https://example.com` |
| Attribute name | `target` |
| Attribute value | `_blank` |

The analyzer should distinguish attribute names from their values. It should also account for both single and double quotation marks.

### 7. Text Content

```html
<h1>Hello World</h1>
```

**Expected recognition:**
- Opening tag: `<h1>`
- Tag name: `h1`
- Text content: `Hello World`
- Closing tag: `</h1>`
- Tag name: `h1`

Text content is the ordinary text between HTML constructs. It should not be confused with tag names, attribute names, attribute values, or comments.

### 8. Self-Closing Tag

```html
<img src="photo.png" alt="Photo" />
```

**Expected recognition:**
- Self-closing tag
- Tag name: `img`
- Attribute name: `src`
- Attribute value: `photo.png`
- Attribute name: `alt`
- Attribute value: `Photo`

A self-closing tag ends with `/>`. Unlike an ordinary opening tag, it does not require a separate closing tag in this notation.

The analyzer should recognize the entire construct as a self-closing tag while still identifying its tag name and attributes.

## Implementation Approach

The analyzer is implemented using Flex, which generates lexical analyzers from regular-expression rules and associated actions.

The general implementation process is:

1. Define regular expressions for the required HTML constructs.
2. Associate each pattern with an action that identifies or reports the matched construct.
3. Handle overlapping patterns carefully, considering Flex's longest-match rule and rule priority.
4. Distinguish the contents of tags from ordinary text.
5. Test the analyzer using progressively more complex HTML examples.
6. Refine the rules to handle whitespace, quotation marks, comments, and other relevant edge cases.

Depending on the implementation, Flex start conditions can be used to distinguish contexts such as ordinary text, tag contents, and attribute values.

## Scope and Limitations

This project focuses on recognizing basic HTML lexical structures. It is not intended to implement a complete HTML parser or validate every aspect of the HTML specification.

Recognizing opening and closing tags does not, by itself, guarantee that elements are correctly nested. Full structural validation would require additional logic, such as maintaining a stack of open elements.

The supported HTML subset and handling of malformed input may be refined during development.

## Technologies

- **Flex:** Lexical analyzer generation.
- **C:** Implementation of token recognition actions.
- **Regular expressions:** Definition of lexical patterns.

## Building and Running

Build and execution instructions will be added once the implementation and its compilation workflow are established.

## Learning Objectives

This project provides practical experience with:

- Lexical analysis and token recognition.
- Regular expressions and pattern matching.
- Flex rules, actions, and start conditions.
- Rule priority and overlapping matches.
- Separating lexical recognition from structural validation.