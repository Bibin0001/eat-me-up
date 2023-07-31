# Use the official Python image as the base image

FROM python:3.9-alpine

# Set environment variables for Python and buffering

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory inside the container

WORKDIR /app

# Install system dependencies required for PostgreSQL (if you use it as your database)
# For other databases, the required dependencies may differ.

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev

# Install project dependencies

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files into the container

COPY . /app/

# Collect static files

RUN python manage.py collectstatic --noinput

# Apply migrations

RUN python manage.py migrate

# Expose the port on which the Gunicorn server will run (adjust as needed)

EXPOSE 8000

# Set the command to run the Gunicorn server

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]

