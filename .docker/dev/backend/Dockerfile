#FROM tiangolo/uvicorn-gunicorn:latest
#FROM --platform=linux/amd64 python:3.11.3
FROM python:3.11.3

# Set up Python behaviour
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/home/app
ENV APP_HOME=/home/app/backend
ENV VIRTUAL_ENV=/opt/venv

# Install system dependencies
RUN apt-get update -y \
  && apt-get install -y netcat gcc postgresql vim

# Create folders
RUN mkdir $HOME
RUN mkdir $APP_HOME

# Set the working directory
WORKDIR $APP_HOME

# Copy all files
COPY ./ ./

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r src/requirements/dev.txt


# Execute entrypoint.sh
RUN ["chmod", "+x", "/home/app/backend/.docker/dev/backend/entrypoint.sh"]
ENTRYPOINT ["sh", "/home/app/backend/.docker/dev/backend/entrypoint.sh" ]

# Start up the backend server
# CMD uvicorn src.main:backend_app --reload --workers 4 --host 0.0.0.0 --port 8000
