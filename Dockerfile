# Use the official Python image as the base image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /app/

# Install dependencies using pipenv
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code to the container
COPY . /app/

# Expose the port that your application runs on
EXPOSE 8000

# Run the Django application
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
