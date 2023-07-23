FROM python:3.9-slim
WORKDIR /app
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
RUN apt-get update && apt-get install -y make
COPY . .
COPY data/fonts /app/media/fonts
CMD ["make", "run_gunicorn"]
