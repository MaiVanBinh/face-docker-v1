FROM python:3.8

COPY ./requirements.txt /var/www/requirements.txt
WORKDIR /var/www/
ADD . /var/www/

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m pip install "pymongo[srv]"
COPY . /var/www/

ENTRYPOINT [ "python" ]

CMD [ "-m", "flask", "run"]   
