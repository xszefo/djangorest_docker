FROM python:3
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y netcat
RUN pip install --upgrade pip 
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ENTRYPOINT ["bash", "start-script.sh"]
EXPOSE 8000
ARG APP_ENV_FILE=app.env
COPY $APP_ENV_FILE /code/app.env
COPY start-script.sh /code/
COPY restapp/ /code/restapp
