FROM python:3.11-alpine

WORKDIR /app

# Alpine needs build deps for some packages
RUN apk add --no-cache gcc musl-dev libffi-dev

COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/api/ .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
