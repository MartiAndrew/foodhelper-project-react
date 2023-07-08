FROM python:3.9

WORKDIR /app

RUN pip install gunicorn==20.1.0

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "foodhelper.wsgi:application", "--bind", "0.0.0.0:8000" ]
