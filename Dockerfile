FROM python:2.7
LABEL author="Richard Crouch"
LABEL description="Cloud coverage microservice"

# Generate logs in unbuffered mode
ENV PYTHONUNBUFFERED=1

# install Yoctopuce dependencies
#RUN apt-get -y update
#RUN apt-get -y install libusb-1.0.0 libusb-1.0.0-dev

# Install Python dependencies
RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv install --system --deploy

RUN mkdir /test_images
COPY test_images/* /test_images/

# Copy application and files
RUN mkdir /app
COPY app/*.py /app/
WORKDIR /app

# see value in definitions.py
#EXPOSE 9503

# run Python unbuffered so the logs are flushed
#CMD ["python3", "-u", "light_service.py"]
CMD ["tail", "-f", "/dev/null"]
