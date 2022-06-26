# Set up a base build container and use to install pip dependencies
FROM python:3.10-slim-bullseye as base
FROM base as builder

RUN pip install --user pipenv

# Tell pipenv to create venv in the current directory
ENV PIPENV_VENV_IN_PROJECT=1
ADD Pipfile.lock Pipfile /usr/src/
WORKDIR /usr/src
RUN /root/.local/bin/pipenv sync

# Copy over pip dependencies from base
FROM base
RUN mkdir -v /usr/src/.venv
COPY --from=builder /usr/src/.venv/ /usr/src/.venv/

# Set up /usr/src as our runtime directory
WORKDIR /usr/src/

# Run as non-root user
RUN useradd -M gunicorn
USER gunicorn

# Add everything except what is in .dockerignore
COPY ./ .

# Run gunicorn as a production-suitable app server
EXPOSE 7777
CMD ./.venv/bin/python -m gunicorn --workers 4 --bind 0.0.0.0:7777 challenge.wsgi --keep-alive 5 --log-level info --access-logfile -
