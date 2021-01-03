from datetime import datetime
from datetime import timedelta
import sys
sys.path.append('/home/ubuntu/twitter-semantic-analysis/twitter_crawler/')
sys.path.append('/home/ubuntu/twitter-semantic-analysis/')

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
    'start_date': datetime(2020, 12, 25),
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

##################     DAGS     ##################
artist_dag = DAG(
    'artist_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Artist archetype',
    schedule_interval="0 19 * * 5",
)

caregiver_dag = DAG(
    'caregiver_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Caregiver archetype',
    schedule_interval="20 19 * * 5",
)

everyman_dag = DAG(
    'everyman_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Everyman archetype',
    schedule_interval="40 19 * * 5",
)

explorer_dag = DAG(
    'explorer_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Explorer archetype',
    schedule_interval="0 20 * * 5",
)

guru_dag = DAG(
    'guru_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Guru archetype',
    schedule_interval="20 20 * * 5",
)

hero_dag = DAG(
    'hero_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Hero archetype',
    schedule_interval="40 20 * * 5",
)

innocent_dag = DAG(
    'innocent_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Innocent archetype',
    schedule_interval="0 21 * * 5",
)

jester_dag = DAG(
    'jester_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Jester archetype',
    schedule_interval="20 21 * * 5",
)

magician_dag = DAG(
    'magician_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Magician archetype',
    schedule_interval="40 21 * * 5",
)

rebel_dag = DAG(
    'rebel_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Rebel archetype',
    schedule_interval="0 22 * * 5",
)

ruler_dag = DAG(
    'ruler_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Ruler archetype',
    schedule_interval="20 22 * * 5",
)

seducer_dag = DAG(
    'seducer_crawler',
    default_args=default_args,
    description='A job for crawling Twitter for Seducer archetype',
    schedule_interval="40 22 * * 5",
)



#####################    JOBS    #######################

artist_job = PythonOperator(
        task_id='gather_artist_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'artist',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=artist_dag,
)

caregiver_job = PythonOperator(
        task_id='gather_caregiver_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'caregiver',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=caregiver_dag,
)

everyman_job = PythonOperator(
        task_id='gather_everyman_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'everyman',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=everyman_dag,
)

explorer_job = PythonOperator(
        task_id='gather_explorer_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'explorer',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=explorer_dag,
)

guru_job = PythonOperator(
        task_id='gather_guru_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'guru',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=guru_dag,
)

hero_job = PythonOperator(
        task_id='gather_hero_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'hero',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=hero_dag,
)

innocent_job = PythonOperator(
        task_id='gather_innocent_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'innocent',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=innocent_dag,
)

jester_job = PythonOperator(
        task_id='gather_jester_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'jester',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=jester_dag,
)

magician_job = PythonOperator(
        task_id='gather_magician_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'magician',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=magician_dag,
)

rebel_job = PythonOperator(
        task_id='gather_rebel_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'rebel',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=rebel_dag,
)

ruler_job = PythonOperator(
        task_id='gather_ruler_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'ruler',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=ruler_dag,
)

seducer_job = PythonOperator(
        task_id='gather_seducer_tweets',
        provide_context=False,
        python_callable=scrape_tweets,
        op_kwargs={'user_list_name': 'seducer',
                   'path_to_list' : '/home/ubuntu/twitter-semantic-analysis/archetype_lists/',
                   'auth_path' : '/home/ubuntu/auth/my_keys.yaml'},
        dag=seducer_dag,
)