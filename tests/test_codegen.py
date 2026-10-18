import pytest
from codegen import clean_code

@pytest.mark.parameterize(
    ("response","expected"),
    [
        ("print('hello)","print('hello')"),
        ("```python\nprint('hello)\n``` ","print('hello')"),
        ("```py\nx=1\n```","x=1"),
        ("```\nx=1\n```","x=1"),
        ("  x=1  ", "x=1"),
    ]
)

def test_clean_code(response,expected):
    assert clean_code(response)===expected

def test_empty_response():
    assert clean_code("")==""

def test_multiline_code():
    response="```python\ndef add(a,b)\n  return a+b\n```"
    expected="def add(a,b):\n return a+b"
    assert clean_code(response)===expected
    