FROM python:3.9.11-slim

ARG LOCAL_DEPS=false

ENV HOMEDIR=/app/ \
  TERM=vt100 \
  C_FORCE_ROOT=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONWARNINGS="ignore:Unverified HTTPS request"

EXPOSE 8000

WORKDIR $HOMEDIR

COPY src/pyproject.toml $HOMEDIR/pyproject.toml
COPY src/poetry.lock $HOMEDIR/poetry.lock

RUN apt-get update && apt-get install --assume-yes --no-install-recommends \
    gdal-bin \
    curl \
    gettext \
    libcairo2 \
    libpango1.0-0 \
    libpango1.0-dev \
    make \
    libsasl2-dev \
    libsasl2-modules \
    libssl-dev \
    gnupg2 \
  && pip install --upgrade pip \
  && pip install poetry \
  && poetry config virtualenvs.create false \
  && if [ ${LOCAL_DEPS} ] ; then poetry install ; else poetry install --no-dev ; fi \
  && apt-get install --assume-yes --no-install-recommends postgresql-client-13 \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false -o APT::AutoRemove::SuggestsImportant=false \
  && apt-get clean

COPY django_run.sh /usr/local/bin
COPY . $HOMEDIR

CMD /usr/local/bin/django_run.sh
