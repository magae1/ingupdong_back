FROM python:3.9.16-slim-bullseye

# 작업 디렉토리 설정
WORKDIR $HOME_DIR

# 환경변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 최신 pip로 업데이트
RUN pip install --upgrade pip

# 파일 복사
COPY . .

# requirement.txt의 라이브러리 설치
RUN pip install -r requirements.txt

# db 최신화
RUN ./manage.py migrate
# port where the Django app runs
EXPOSE 8000

# start server
CMD gunicorn config.wsgi:application --bind 0.0.0.0:8000
