FROM python:3.10.10-bullseye

ENV PYTHONPATH="${PYTHONPATH}:/app"

WORKDIR /app

RUN set +x \
    && apt update \
    && apt upgrade -y \
    && apt install -y build-essential gcc curl jq vim \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - \
    && cd /usr/bin \
    && ln -s /etc/poetry/bin/poetry \
    && ln -s /app/script/entrypoint.sh \
    && poetry config virtualenvs.create false \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
RUN sed "s/\r//g" /app/script/pre_form_entrypoint.sh > /app/script/entrypoint.sh \
    && chmod +x /app/script/*
RUN poetry install -n

ENTRYPOINT ["entrypoint.sh"]



