FROM python:3.10.8-slim as dependencies-builder
# python:
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
# poetry:
ENV POETRY_VERSION '1.2.2'
ENV POETRY_VIRTUALENVS_CREATE false

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    # psycopg-2 build dependencies
    libpq-dev \
    build-essential \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry==$POETRY_VERSION
COPY pyproject.toml ./
RUN poetry export --with prod --without-hashes --no-interaction \
    --no-ansi -f requirements.txt -o requirements.txt
RUN pip install --disable-pip-version-check --prefix=/dependencies --no-cache-dir \
    --force-reinstall -r requirements.txt

FROM dependencies-builder as runtime

ENV APP_DIR /app
RUN mkdir $APP_DIR
RUN mkdir $APP_DIR/staticfiles
WORKDIR $APP_DIR

# copying copliled libs to folder where python expects them to be
COPY --from=dependencies-builder /dependencies /usr/local
COPY . .

RUN rm pyproject.toml

RUN adduser --system --group --no-create-home app_user
RUN chown -R app_user:app_user $APP_DIR
RUN chmod -R 500 $APP_DIR

USER app_user

CMD ["./docker-entrypoint.sh"]


