# Secure Streaming File Ingestion Service

A backend-grade file ingestion pipeline that:  

- handles files as byte streams
- validates file types using signatures
- safely distinguishes text vs binary
- streams data without loading it into memory
- applies correct Unicode handling

Built in pure Python for correctness and performance.
