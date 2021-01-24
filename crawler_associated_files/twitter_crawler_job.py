from datetime import datetime
from datetime import timedelta
import sys
sys.path.append('/app/crawler_associated_files/twitter_crawler/')
sys.path.append('/app/')

LISTS_PATH = '/app/archetype_lists/'
KEYS_PATH = '/app/my_keys.yaml'

from crawler.crawler import scrape_tweets

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 15, 18, 0, 0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
dag = DAG(
    'twitter_crawler',
    default_args=default_args,
    description='A job for crawling Twitter',
    schedule_interval="0 19 * * 5",
)

artist_job = PythonOperator(
        task_id='gather_artist_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'artist',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)


caregiver_job = PythonOperator(
        task_id='gather_caregiver_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'caregiver',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

everyman_job = PythonOperator(
        task_id='gather_everyman_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'everyman',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

explorer_job = PythonOperator(
        task_id='gather_explorer_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'explorer',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

guru_job = PythonOperator(
        task_id='gather_guru_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'guru',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

hero_job = PythonOperator(
        task_id='gather_hero_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'hero',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

innocent_job = PythonOperator(
        task_id='gather_innocent_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'innocent',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

jester_job = PythonOperator(
        task_id='gather_jester_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'jester',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

magician_job = PythonOperator(
        task_id='gather_magician_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'magician',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

rebel_job = PythonOperator(
        task_id='gather_rebel_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'rebel',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

ruler_job = PythonOperator(
        task_id='gather_ruler_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'ruler',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

seducer_job = PythonOperator(
        task_id='gather_seducer_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'seducer',
                   'path_to_list' : LISTS_PATH,
                   'auth_path' : KEYS_PATH},
        dag=dag,
)

dly1 = BashOperator(
    task_id='delay_next_crawl1',
    bash_command='sleep 15m',
    dag=dag)

dly2 = BashOperator(
    task_id='delay_next_crawl2',
    bash_command='sleep 15m',
    dag=dag)

dly3 = BashOperator(
    task_id='delay_next_crawl3',
    bash_command='sleep 15m',
    dag=dag)

dly4 = BashOperator(
    task_id='delay_next_crawl4',
    bash_command='sleep 15m',
    dag=dag)

dly5 = BashOperator(
    task_id='delay_next_crawl5',
    bash_command='sleep 15m',
    dag=dag)

dly6 = BashOperator(
    task_id='delay_next_crawl6',
    bash_command='sleep 15m',
    dag=dag)

dly7 = BashOperator(
    task_id='delay_next_crawl7',
    bash_command='sleep 15m',
    dag=dag)

dly8 = BashOperator(
    task_id='delay_next_crawl8',
    bash_command='sleep 15m',
    dag=dag)

dly9 = BashOperator(
    task_id='delay_next_crawl9',
    bash_command='sleep 15m',
    dag=dag)

dly10 = BashOperator(
    task_id='delay_next_crawl10',
    bash_command='sleep 15m',
    dag=dag)

dly11 = BashOperator(
    task_id='delay_next_crawl11',
    bash_command='sleep 15m',
    dag=dag)

artist_job >> dly1 >> caregiver_job >> dly2 >> everyman_job >> dly3 >> explorer_job >> dly4 >> guru_job >> dly5 >> hero_job >> dly6 >> innocent_job >> dly7 >> jester_job >> dly8 >> magician_job >> dly9 >> rebel_job >> dly10 >> ruler_job >> dly11 >> seducer_job
