from fastapi import FastAPI, Query
# the service logic lives in fertility_count.py, which is a module in the
# same directory.  Import it directly; this avoids issues with package
# namespaces when the directory also contains __init__.py.
from fertility_count import compute_fertility, analyze_identifiers_from_texts, analyze_identifiers_from_files

app = FastAPI(
    title="Fertility Service",
    description="Simple REST API that computes token fertility for supplied text.",
)


@app.get("/health")
def health():
    """Health check endpoint. Returns 200 OK if service is running."""
    return {"status": "ok"}


from fastapi import UploadFile, File, HTTPException
import io


@app.get("/fertility")
def fertility(
    text: str | None = Query(None, description="Text to analyze"),
    files: str | None = Query(
        None,
        description="Comma-separated absolute paths of files whose contents should be analyzed.",
    ),
):
    """Compute fertility for provided text or files (via GET).

    Exactly the same functionality as the previous POST variant, but uses
    file paths instead of uploaded content.  At least one of ``text`` or
    ``files`` must be supplied.  If both are given, files take precedence.
    """
    if text is None and files is None:
        raise HTTPException(status_code=400, detail="Provide 'text' or 'files' query parameter")

    if files is not None:
        paths = [p.strip() for p in files.split(",") if p.strip()]
        responses = []
        for path in paths:
            try:
                with open(path, encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(path, encoding="windows-1251") as f:
                    content = f.read()
            fertility_result = compute_fertility(content)
            responses.append({"path": path, "result": fertility_result})
        return {"files": responses}

    # fallback to simple text
    result = compute_fertility(text) # type: ignore
    return result


# new endpoint for analyzing identifiers
@app.get("/most-expensive-identifiers")
def most_expensive_identifiers(
    text: str | None = Query(None, description="Raw text to scan"),
    files: str | None = Query(
        None,
        description=(
            """Comma-separated list of absolute file paths whose contents should be scanned.
            Files are read as UTF-8, falling back to Windows-1251 if necessary.
            """
        ),
    ),
):
    """Return the 50 CamelCase identifiers with highest token cost.

    At least one of ``text`` or ``files`` must be provided.
    """
    if text is None and files is None:
        raise HTTPException(status_code=400, detail="Provide either 'text' or 'files'")

    results = []
    if text is not None:
        results = analyze_identifiers_from_texts([text])
    if files is not None:
        paths = [p.strip() for p in files.split(",") if p.strip()]
        results = analyze_identifiers_from_files(paths)

    return {"identifiers": [{"text": w, "tokens": c} for w, c in results]}


# to run via ``uvicorn main:app --reload``
