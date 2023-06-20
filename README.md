# to
Bookmark search API

## Installation
```sh
pip3 install .
```

## Development
The development server can be started by executing:
```sh
uvicorn to:app --port 8080 --reload
```

## Containerisation
### Build
```sh
docker build . -t to
```

### Run
```sh
docker run -p 8080:8080 -it to
```