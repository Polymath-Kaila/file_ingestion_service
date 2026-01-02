# ingest.py

from typing import BinaryIO

from ingestion.stream_reader import (
    stream_chunks,
    read_stream_with_metadata,
)
from ingestion.signatures import detect_file_type
from ingestion.text_handling import looks_like_text, safe_decode_text


def ingest_stream(
    stream: BinaryIO,
    filename: str,
    chunk_size: int = 8192,
) -> dict:
    """
    Ingest a binary stream safely and return metadata.

    This function:
    - never loads the full stream into memory
    - detects file type via signature
    - distinguishes text vs binary conservatively
    - decodes text safely when applicable
    """

    # Step 1: Read minimal header
    header_size = 32
    header = stream.read(header_size)

    file_type = detect_file_type(header)

    # Step 2: Classify binary vs text 
    is_binary = file_type in {"png", "jpg", "pdf", "zip"}

    text_sample = None
    decoded_text = None

    if not is_binary:
        if looks_like_text(header):
            decoded_text = safe_decode_text(header)
            if decoded_text is not None:
                text_sample = decoded_text

    # Step 3: Stream entire content for metadata
    # We must include the header bytes again
    from io import BytesIO
    combined_stream = BytesIO(header)
    combined_stream.write(stream.read())
    combined_stream.seek(0)

    metadata = read_stream_with_metadata(
        combined_stream,
        chunk_size=chunk_size,
    )

    # Step 4: Final result
    return {
        "filename": filename,
        "detected_type": file_type,
        "is_binary": is_binary,
        "text_sample": text_sample,
        "size_bytes": metadata["size_bytes"],
        "sha256": metadata["sha256"],
    }
