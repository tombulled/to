FROM python:3.8

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY to to
COPY config.yaml config.yaml

RUN pip install .
RUN pip install uvicorn

USER 1001

CMD ["python", "-m", "uvicorn", "to:app", "--host", "0.0.0.0", "--port", "8080"]