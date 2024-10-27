FROM python:3.12.6-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN pwd

RUN ls

CMD ["python", "-m", "movies_backend.main" ]
