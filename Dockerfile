# Use an official Python 3.11 runtime as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install pipenv and dependencies
RUN pip install pipenv

# Specify Python 3.11 explicitly for creating the virtual environment
RUN pipenv --python /usr/local/bin/python3.11 install --deploy --ignore-pipfile

# Copy the rest of the application code to the container
COPY . /app/

# Specify the command to run when the container starts
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "MuslimLife.wsgi:application"]
