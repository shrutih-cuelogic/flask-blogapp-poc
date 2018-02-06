FROM python 2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /flask-blogapp-poc
WORKDIR /flask-blogapp-poc
COPY . /flask-blogapp-poc
RUN rm -rf migrations
RUN apt-get -y update --fix-missing
RUN apt-get -y install curl wget make gcc build-essential --fix-missing
ADD requirements.txt /flask-blogapp-poc/
RUN pip install -r requirements.txt
ADD . /flask-blogapp-poc/
RUN chmod u+x docker-entrypoint.sh
ENTRYPOINT ["bash", "/flask-blogapp-poc/docker-initiate.sh"]