# Set up a base build container and use to install pip dependencies
FROM python:3.10-slim-bullseye as base
FROM base as builder
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt gunicorn --no-warn-script-location

# Copy over pip dependencies from base
FROM base
COPY --from=builder /install /usr/local

# Set up /app as our runtime directory
RUN mkdir /app
WORKDIR /app

# Run as non-root user
RUN useradd -M gunicorn
USER gunicorn

# Add everything except what is in .dockerignore
COPY ./ .

# Run gunicorn as a production-suitable app server
EXPOSE 7777
CMD gunicorn --workers 4 --bind 0.0.0.0:7777 challenge.wsgi --keep-alive 5 --log-level info --access-logfile -
