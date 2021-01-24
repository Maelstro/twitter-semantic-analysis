FROM puckel/docker-airflow

# Copy Twitter Crawler
WORKDIR /app
COPY crawler_associated_files crawler_associated_files
COPY docs/archetype_lists archetype_lists

RUN pip install -r '/app/crawler_associated_files/requirements.txt'
RUN pip install pyyaml
RUN pip install dnspython
# Change dicrectory to DAG dir
WORKDIR /usr/local/airflow/dags

# Copy files associated with DAGs
COPY crawler_associated_files/separate_twitter_crawler_job.py separate_twitter_crawler_job.py
COPY crawler_associated_files/twitter_crawler_job.py twitter_crawler_job.py
