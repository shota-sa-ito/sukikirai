FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye
ENV POETRY_HOME=/opt/poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$PATH:/opt/poetry/bin
RUN poetry config virtualenvs.in-project true
#COPY pyproject.toml .
#COPY poetry.lock .
#RUN poetry config virtualenvs.in-project true \
#    && poetry install
