import re
import sys
import pytest


def test_header_comments():
    """Students should have a docstring with author, date, and description"""
    with open("cond_practice.py", encoding="utf-8") as f:
        kids_code = f.read()

    # Check that a module-level docstring exists
    docstring_match = re.search(r'^\s*"""(.*?)"""', kids_code, re.DOTALL)
    assert docstring_match is not None, "You must include a header docstring using triple quotes (\"\"\")"

    docstring = docstring_match.group(1)

    # Check for author field with a non-empty value
    author_match = re.search(r'author\s*:\s*(.+)', docstring, re.IGNORECASE)
    assert author_match is not None, "Your header must include an 'author:' field"
    assert author_match.group(1).strip() != "", "Your 'author:' field must not be empty"

    # Check for date field with a non-empty value
    date_match = re.search(r'date\s*:\s*(.+)', docstring, re.IGNORECASE)
    assert date_match is not None, "Your header must include a 'date:' field"
    assert date_match.group(1).strip() != "", "Your 'date:' field must not be empty"

    # Check that there's at least one line that isn't just author/date (a description)
    lines = [line.strip() for line in docstring.strip().splitlines()]
    description_lines = [
        line for line in lines
        if line
        and not re.match(r'author\s*:', line, re.IGNORECASE)
        and not re.match(r'date\s*:', line, re.IGNORECASE)
    ]
    assert len(description_lines) >= 1, "Your header must include a short description of the program"


@pytest.mark.parametrize(
    "a,b,c",
    [
        ("1", "5", "10"),
        ("1", "10", "5"),
        ("5", "1", "10"),
        ("5", "10", "1"),
        ("10", "1", "5"),
        ("10", "5", "1"),
    ],
)
def test_orderings(a, b, c, capsys, monkeypatch):
    """No matter what order, student should output sorted numbers"""
    inputs = [c, b, a]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop())
    __import__("cond_practice")
    captured = capsys.readouterr()

    assert "1 5 10" in captured.out
    del sys.modules["cond_practice"]