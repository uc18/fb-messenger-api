FROM python:3.7

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade -r /code/requirements.txt

COPY . /code
COPY ./pkg/fbchat/_state.py /usr/local/lib/python3.7/site-packages/fbchat/_state.py

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]