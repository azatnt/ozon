FROM python:3.9.6-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN pip install --upgrade pip
COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code/

#RUN python /code/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "config.wsgi", "timeout", "300"]
