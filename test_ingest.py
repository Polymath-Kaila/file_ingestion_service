from ingestion.ingest import ingest_stream

def test_file(path: str):
    with open(path, "rb") as f:
        result = ingest_stream(f, path)
    print(f"\n=== {path} ===")
    for k, v in result.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    test_file("test_files/hello.txt")
    test_file("test_files/image.png")
