# pull official base image
FROM python:3.10

# set work directoryapk update \
                    #    && apk add postgresql-dev gcc python3-dev musl-dev
#RUN mkdir /usr/src/app
#RUN mkdir /usr/src/app/static
#RUN mkdir /usr/src/app/media
#WORKDIR /usr/src/app

ENV APP_HOME=/usr/src/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
WORKDIR $APP_HOME
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update  \
    && apt-get install netcat-traditional -y  \
    && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev


# install poetry
RUN pip install poetry
#ENV PATH "/root/.local/bin:$PATH"
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# install python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false --local
RUN poetry install --no-dev --no-root
COPY ./ $APP_HOME
COPY ./docker-entrypoint.sh .

## copy project
#COPY . .


RUN ["chmod", "+x", "/usr/src/app/docker-entrypoint.sh"]



RUN sed -i 's/\r$//g'  $APP_HOME/docker-entrypoint.sh
RUN chmod +x  $APP_HOME/docker-entrypoint.sh
#
## run entrypoint.sh
ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]