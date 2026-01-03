def looks_like_text(sample: bytes) -> bool:
    """
    Heuristic check to see if a byte sample looks like text.
    """
    # Null bytes are a strong binary signal
    if b"\x00" in sample:
        return False

    # Count non-printable control bytes
    non_printable = sum(
        1 for b in sample
        if b < 9 or (13 < b < 32)
    )

    # If too many control bytes, treat as binary
    return non_printable / max(len(sample), 1) < 0.3

def safe_decode_text(data: bytes):
    """  
    Decode bytes into text safely, handling BOM

    """
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return None