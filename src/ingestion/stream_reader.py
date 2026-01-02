import hashlib
from typing import BinaryIO, Iterator
from ingestion.signatures import detect_file_type


def stream_chunk(
        stream:BinaryIO,
        chunk_size:int = 8192,
    ) -> Iterator[bytes]:  
    """
    yield chunks of bytes from a binary stream.
    
    - does Not load full stream inot memory
    - stops cleanly at end of stream/file (EOF)
    """

    while True:
        chunk = stream.read(chunk_size)
        if not chunk:
            break
        yield chunk


def read_stream_with_metadata(
    stream: BinaryIO,
    chunk_size: int = 8192,
) -> dict:
    """
    Read a binary stream safely while computing metadata.

    Returns:
        {
            "size_bytes": int,
            "sha256": str
        }
    """
    hasher = hashlib.sha256()
    total_size = 0

    for chunk in stream_chunk(stream, chunk_size):
        total_size += len(chunk)
        hasher.update(chunk)

    return {
        "size_bytes": total_size,
        "sha256": hasher.hexdigest(),
    }

def stream_with_signature(
    stream: BinaryIO,
    header_size: int = 16,
    chunk_size: int = 8192,
):
    """
    Stream data while detecting file signature.

    Yields:
        (file_type, chunk)
    """
    header = stream.read(header_size)
    mv = memoryview(header)

    if mv.startswith(b"\x89PNG"):
        filetype = "png"
    else:
        return

    file_type = detect_file_type(header)

    # Yield header first
    if header:
        yield file_type, header

    # Yield the rest of the stream
    for chunk in stream_chunk(stream, chunk_size):
        yield file_type, chunk


