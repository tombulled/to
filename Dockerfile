FROM python:3.8

WORKDIR /app

COPY pyproject.toml pyproject.toml
COPY to to
COPY assets assets

# Temporarily the ./icons directory is included for favicons.
# In the future this will be handled differently.
COPY icons icons

RUN pip install .
RUN pip install uvicorn

USER 1001

CMD ["python", "-m", "uvicorn", "to:app", "--host", "0.0.0.0", "--port", "8080"]