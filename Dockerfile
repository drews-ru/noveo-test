FROM python:3.9.6
ENV PYTHONUNBUFFERED 1
RUN git clone https://github.com/drewslee/noveo_test.git /noveo
WORKDIR /noveo
RUN ls .
RUN cd testtask
RUN pip install -r requirements.txt
VOLUME /noveo

EXPOSE 8080

CMD python manage.py makemigrations && python manage.py migrate && uvicorn testtask.asgi:application