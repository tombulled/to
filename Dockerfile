FROM python:3.8

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY to to
COPY config.example.yaml config.yaml

RUN mkdir icons

RUN pip install .
RUN pip install uvicorn

USER 1001

ENV PORT 8080

EXPOSE ${PORT}

CMD python -m uvicorn to:app --host 0.0.0.0 --port ${PORT}