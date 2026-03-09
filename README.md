# Fertility Count REST Service

This small Python package exposes a REST API that calculates token "fertility" (tokens per word)
using a Hugging Face tokenizer.

## Setup

```bash
python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Running

Start the server with Uvicorn from the service directory:

```bash
cd c:\Users\mym\Projects\python\fertility_count
uvicorn main:app --reload
```

**Important:** the working directory must be the folder itself.  The
module `fertility_count.py` is not part of a package, so invoking
`uvicorn fertility_count.main:app` from the parent directory will fail
with an import error.

The service listens on `http://127.0.0.1:8000` by default.

> **Note:** the first time the tokenizer is loaded you'll see
> a bunch of download messages and warnings about PyTorch or
> symlinks. These are normal and don't affect functionality
> – only the tokenizer is used, not the full model.

## Endpoints

- `GET /health` – returns `{ "status": "ok" }`.
- `GET /fertility` – computes words, tokens, fertility and returns a `token_list`.
  Use either the `text` query parameter for inline text or `files` for a
  comma-separated list of absolute file paths whose contents should be
  analyzed (files are read as UTF-8 with a Windows-1251 fallback).

  Tokens are produced by decoding each token id, so they may include leading
  spaces (`" Об"`), newlines or punctuation.  This makes the list easier to
  inspect compared to the raw byte‑level strings produced by the tokenizer.

- `GET /most-expensive-identifiers` – scans supplied text and/or local files
  for CamelCase identifiers and returns the top 50 sorted by tokenizer cost.
  Use the `text` query parameter for inline content and `files` for a
  comma-separated list of absolute file paths that the service can read.

Example:

```bash
curl "http://127.0.0.1:8000/fertility?text=Hello%20world"
```