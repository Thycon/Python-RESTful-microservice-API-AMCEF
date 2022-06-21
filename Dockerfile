FROM python:3

EXPOSE 80

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

WORKDIR /Python-RESTful-microservice-API-AMCEF

COPY . /Python-RESTful-microservice-API-AMCEF

CMD [ "python", "./main.py"]