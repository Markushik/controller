FROM python:3.10.8-slim-buster

WORKDIR .

COPY app ./app
COPY .secrets.toml settings.toml ./
COPY poetry.lock pyproject.toml ./

RUN pip3 install --no-cache-dir --upgrade pip \
 && pip3 install --no-cache-dir poetry

RUN poetry install --no-interaction --no-dev

EXPOSE 5050
ENTRYPOINT ["poetry", "run", "python", "-m", "app"]