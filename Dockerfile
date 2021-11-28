FROM python:latest

WORKDIR /code

COPY app /code/

RUN pip install -r requirements.txt

EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
