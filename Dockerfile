FROM python:3.10.8-slim-buster

WORKDIR .

COPY app ./app/
COPY .secrets.toml settings.toml ./
COPY poetry.lock pyproject.toml ./

RUN pip3 install --no-cache-dir --root-user-action=ignore --upgrade pip \
 && pip3 install --no-cache-dir --root-user-action=ignore setuptools \
 && pip3 install --no-cache-dir --root-user-action=ignore poetry

RUN poetry install --only main --no-root --no-interaction --no-ansi

EXPOSE 5050
ENTRYPOINT ["poetry", "run", "python", "-m", "app"]