FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY . .
ENV PORT=8000
EXPOSE ${PORT}
CMD uv run uvicorn main:app --host 0.0.0.0 --port $PORT
