FROM python:3.9-alpine
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

# Ensures python output is sent straight to terminal without being
# buffered − can then see real time outputs
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip

COPY requirements.txt $WORKDIR 

RUN pip install -r requirements.txt

COPY . $WORKDIR  
RUN rm -r env/

CMD python manage.py runserver 0.0.0.0:8000