# ui/app.py

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse

from ingestion.ingest import ingest_stream

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
      <head><title>Secure File Ingestion</title></head>
      <body>
        <h1>Secure Streaming File Ingestion</h1>
        <form action="/upload" method="post" enctype="multipart/form-data">
          <input type="file" name="file" required />
          <button type="submit">Upload</button>
        </form>
      </body>
    </html>
    """


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    result = ingest_stream(file.file, file.filename)
    return result
