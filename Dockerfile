FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md /app/
COPY src /app/src
COPY corpus /app/corpus
RUN pip install --no-cache-dir -e ".[api]"
ENV VERDICT_CORPUS=/app/corpus/dineflow
EXPOSE 8000
CMD ["uvicorn", "verdict_desk.api:app", "--host", "0.0.0.0", "--port", "8000"]
