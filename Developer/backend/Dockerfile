FROM python:3.9-slim

WORKDIR /app
COPY ./backend /app

RUN pip install fastapi uvicorn gym numpy

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
