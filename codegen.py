import argparse 
import os 
import re 
import sys  
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq 

from datetime import datetime

load_dotenv()

SYSTEM_PROMPT = """
You are an expert Python code generator.

Convert the user's programming task into correct, readable,
working Python code.

Rules:
1. Return ONLY valid Python source code.
2. Do not include explanations, introductions, or conclusions.
3. Do not use Markdown or Markdown code fences.
4. Include necessary imports.
5. Use clear function and variable names.
6. Handle common edge cases.
7. Add concise Python comments only when useful.
8. Make the code self-contained and easy to run.
9. Do not claim that code was tested unless it was.
"""



def clean_code(response: str) -> str:
    """Remove Markdown code fences from an LLM response."""
    response = response.strip()

    response = re.sub(
        r"\A```(?:python|py)?[ \t]*\r?\n?",
        "",
        response,
        flags=re.IGNORECASE,
    )

    response = re.sub(
        r"\r?\n?```[ \t]*\Z",
        "",
        response,
    )

    return response.strip()


def generate_code(task: str) -> str:
    """Generate Python code using the Groq API."""
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your .env file."
        )

    model = os.getenv(
        "GROQ_MODEL","openai/gpt-oss-120b",
    )

    client = Groq(api_key=api_key)

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ],
        temperature=0.2,
    )

    response = completion.choices[0].message.content or ""
    code = clean_code(response)

    if not code:
        raise ValueError("The model returned empty code.")

    return code


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Python code from a plain-English task."
    )

    parser.add_argument(
        "task",
        nargs="+",
        help="Programming task to convert into Python code",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="generated_code.py",
        help="Output Python file (default: generated_code.py)",
    )

    args = parser.parse_args()
    task = " ".join(args.task).strip()

    try:
        code = generate_code(task)

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if  output_path.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path=output_path.with_name(f"{output_path.stem}_{timestamp}{output_path.suffix}")

        output_path.write_text(code + "\n", encoding="utf-8")

        print("\n--- Generated Python code ---\n")
        print(code)
        print(f"\nSaved to: {output_path.resolve()}")

        return 0

    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
