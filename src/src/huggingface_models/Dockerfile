FROM python:3.12

COPY ./requirements.txt . 
RUN pip install -r requirements.txt

COPY ./src/get_huggingface_models.py .
CMD ["python3", "get_huggingface_models.py"]