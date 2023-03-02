FROM python:3.9.16-slim-bullseye

# where your code lives
WORKDIR $HOME_DIR

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip

# copy whole project to your docker home directory.
COPY . .

# run this command to install all dependencies
RUN pip install -r requirements.txt

# port where the Django app runs
EXPOSE 8000

RUN python manage.py makemigrations ingupdong
RUN python manage.py migrate
# start server
CMD gunicorn back.wsgi:application --bind 0.0.0.0:8000
