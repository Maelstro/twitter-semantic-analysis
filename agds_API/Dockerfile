FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
# Debian-based image, has apt

# Copy all the files to the image and switch to required directory
COPY app /app
WORKDIR /app

RUN pwd

# Install Python dependencies
RUN pip3 install -r requirements.txt

EXPOSE 8000

RUN python -m nltk.downloader punkt

ENTRYPOINT uvicorn --host 0.0.0.0 main:agds_api --reload