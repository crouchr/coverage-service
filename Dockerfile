FROM python:2.7
LABEL author="Richard Crouch"
LABEL description="Cloud coverage microservice"

# Generate logs in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install packages
RUN apt-get -y update
RUN apt-get -y install joe

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

EXPOSE 9502

# Note Python 2, not the usual Python 3
CMD ["python", "-u", "coverage_service.py"]
#CMD ["tail", "-f", "/dev/null"]
