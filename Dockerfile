FROM python:3
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y netcat
RUN pip install --upgrade pip 
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ENTRYPOINT ["bash", "start-script.sh"]
EXPOSE 8000
COPY app.env start-script.sh /code/
COPY restapp/ /code/restapp