# pull official base image
FROM python:3.7.0

# set work directory
RUN mkdir /masklink
WORKDIR /masklink

# set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2
# RUN apk update
# RUN apk add --virtual build-deps gcc python3-dev musl-dev
# RUN apk add postgresql-dev
# RUN pip install psycopg2
# RUN apk del build-deps

# RUN apt-get update && apt-get upgrade -y && apt-get install -y libsqlite3-dev

# install dependencies
COPY ./requirements.txt /masklink/
RUN pip install -r /masklink/requirements.txt

# copy project
COPY . /masklink/

# add and run as non-root user
# RUN adduser -D myuser
# USER myuser

# run gunicorn
# CMD [ "python", "./manage.py", "migrate", "masklink"]
CMD python ./manage.py migrate masklink
# CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8080"]
# RUN python ./manage.py migrate masklink
# RUN python ./manage.py runserver 0.0.0.0:8080
# CMD [ "python", "./manage.py", "runserver", "$PORT"]
CMD python manage.py runserver 0.0.0.0:$PORT