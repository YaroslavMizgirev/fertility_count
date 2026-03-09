"""Module for fertility calculation.

Contains helper to compute token fertility using a shared tokenizer.
"""

from transformers import AutoTokenizer
from typing import Dict

# initialize tokenizer once at import time
_tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-14B")


def compute_fertility(text: str) -> Dict[str, float]:
    """Calculate words, tokens and fertility for the given text.

    Args:
        text: input string to analyze.

    Returns:
        A dictionary with keys ``words``, ``tokens`` and ``fertility``.
    """
    words = text.split()
    token_ids = _tokenizer.encode(text)
    count_words = len(words)
    count_tokens = len(token_ids)
    fertility = count_tokens / count_words if count_words else 0.0

    # convert numeric ids to vocabulary tokens (strings)
    # instead of trying to massage the raw token strings, simply ask
    # the tokenizer to decode each id back to text.  This handles
    # non‑latin1 characters and spacing markers correctly.
    token_list = []
    for tid in token_ids:
        # decode returns a string; it may include leading spaces
        tok = _tokenizer.decode([tid])
        token_list.append(tok)

    return {
        "words": count_words,
        "tokens": count_tokens,
        "fertility": round(fertility, 2),
        "token_list": token_list,
    }


def analyze_identifiers_from_texts(texts: list[str]) -> list[tuple[str, int]]:
    """Scan provided texts for CamelCase identifiers and return the top-50 by token cost.

    This mirrors the example in the user's recent snippet: load texts, extract
    identifiers matching the regex, then compute the number of tokens each
    identifier encodes to.
    """
    import re
    from collections import Counter

    word_cost = Counter()
    for text in texts:
        identifiers = re.findall(r"[А-ЯA-Z][а-яa-z]+(?:[А-ЯA-Z][а-яa-z]+)+", text)
        for ident in identifiers:
            tokens = _tokenizer.encode(ident, add_special_tokens=False)
            word_cost[ident] = len(tokens)
    return word_cost.most_common(50)


def analyze_identifiers_from_files(file_paths: list[str]) -> list[tuple[str, int]]:
    """Read each absolute path (utf-8 or win-1251) and analyse its contents."""
    texts = []
    for path in file_paths:
        try:
            with open(path, encoding="utf-8") as f:
                texts.append(f.read())
        except UnicodeDecodeError:
            with open(path, encoding="windows-1251") as f:
                texts.append(f.read())
    return analyze_identifiers_from_texts(texts)


if __name__ == "__main__":
    # simple CLI fallback for quick tests
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate token fertility for some text."
    )
    parser.add_argument("text", help="Text to analyze (enclose in quotes).")
    args = parser.parse_args()
    result = compute_fertility(args.text)
    print(f"Слов: {result['words']}")
    print(f"Токенов: {result['tokens']}")
    print(f"Fertility: {result['fertility']:.2f}")