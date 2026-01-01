import hashlib
from typing import BinaryIO, Iterator

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