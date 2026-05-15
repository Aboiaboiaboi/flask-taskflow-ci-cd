# Multi-stage build: builder installs deps, runtime copies only what's needed
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
RUN useradd --no-create-home --shell /bin/false appuser
USER appuser
COPY --chown=appuser:appuser . .
EXPOSE 5000
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "app:app"]