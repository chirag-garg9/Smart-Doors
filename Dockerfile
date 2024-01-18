FROM  arm64v8/python:3.11.7-bookworm

WORKDIR /backend

# copy from the current directory of the Dockerfile to /backend in the image
COPY . /backend

EXPOSE 5000

RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]