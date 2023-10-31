# FROM python:3.10
# COPY app.py /
# RUN pip install flask
FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /app/static
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5555
# CMD ["python", "-m", "flask", "--app", "app", "run"]