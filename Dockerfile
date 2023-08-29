# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install pipenv and dependencies
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code to the container
COPY . /app/

# Specify the command to run when the container starts
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "MuslimLife.wsgi:application"]
