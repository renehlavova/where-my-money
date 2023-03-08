# Let's use TomasVotava's Slim Python Dockerfile - it's built daily and it already contains poetry
FROM registry.gitlab.com/bizztreat/python-poetry:3.10-slim

WORKDIR /code

ADD . .

ENV POETRY_VIRTUALENVS_CREATE=0

RUN poetry install

CMD ["poe", "-q", "run"]
