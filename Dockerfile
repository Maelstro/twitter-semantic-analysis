FROM puckel/docker-airflow

# Copy Twitter Crawler
WORKDIR /app
COPY crawler_associated_files crawler_associated_files
COPY docs/archetype_lists archetype_lists
COPY auth/my_keys.yaml my_keys.yaml
RUN pip install -r '/app/crawler_associated_files/requirements.txt'
# Change dicrectory to DAG dir
WORKDIR /usr/local/airflow/dags

# Copy files associated with DAGs
COPY crawler_associated_files/separate_twitter_crawler_job.py separate_twitter_crawler_job.py
COPY crawler_associated_files/twitter_crawler_job.py twitter_crawler_job.py
