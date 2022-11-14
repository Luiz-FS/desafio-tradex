FROM python:3.9-slim

RUN apt update && apt upgrade -y && apt install git -y

COPY requirements/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt --no-cache-dir

WORKDIR /app/

COPY ./authenticator/ .

# CMD ["gunicorn", "-b", ":8000", "authenticator.wsgi:application"]
