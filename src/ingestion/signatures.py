# signatures.py

SIGNATURES = {
    "png": b"\x89PNG\r\n\x1a\n",
    "pdf": b"%PDF",
    "zip": b"PK\x03\x04",
    "jpg": b"\xff\xd8\xff",
}

def detect_file_type(header: bytes) -> str:
    """
    Detect file type based on header bytes.
    """
    for filetype, sig in SIGNATURES.items():
        if header.startswith(sig):
            return filetype
    return "unknown"
