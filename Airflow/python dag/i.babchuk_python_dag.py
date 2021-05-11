from airflow.models import DAG
from airflow.operators import PythonOperator
#from airflow.operators import BashOperator
from datetime import datetime

import pandas as pd
import vk_api
import random
import requests
import json


def report_DataFrame(path, necessary_date):

    df = pd.read_csv(path)

    ctr_df = df.pivot_table(index="date", columns="event", values="time", aggfunc="count")
    ctr_df["ctr_%"] = round(ctr_df.click / (ctr_df.view)*100, 2)

    benefit_df = df.query("event == 'view'") \
                    .groupby("date") \
                    .agg({"ad_cost": "sum"}) \
                    .mul(0.001) \
                    .round(2) \
                    .rename(columns={"ad_cost": "earning"})

    total_df = ctr_df.merge(benefit_df, on="date")
    changes_df = round((total_df.loc[necessary_date] - total_df.loc['2019-04-01']) * 100 / total_df.loc['2019-04-01'], 2)
    changes_df = changes_df.to_frame().rename(columns={0: "change_rate_%"}).T

    return pd.concat([total_df, changes_df]), df.ad_id[0]


def text_report_creation(ad_id, final_df):

    months = {"01": "января",
             "02": "февраля",
             "03": "марта",
             "04": "апреля",
             "05": "мая",
             "06": "июня",
             "07": "июля",
             "08": "августа",
             "09": "сентября",
             "10": "октября",
             "11": "ноября",
             "12": "декабря"}


    date = final_df.index[-2][-2:]
    month = final_df.index[-2][-5:-3]
    waste = final_df.iloc[1, 3]
    clicks = final_df.iloc[1, 0]
    views = final_df.iloc[1, 1]
    ctr = final_df.iloc[1, 2]

    waste_p = final_df.iloc[2, 3]
    clicks_p = final_df.iloc[2, 0]
    views_p = final_df.iloc[2, 1]
    ctr_p = final_df.iloc[2, 2]

    with open("report.txt", "w") as f:
        f.write(f"Отчёт по объявлению {ad_id} за {date} {months[month]}:\n")
        f.write(f"Траты: {waste} рублей ({waste_p}%)\n")
        f.write(f"Показы: {views} ({views_p}%)\n")
        f.write(f"Клики: {clicks} ({clicks_p}%)\n")
        f.write(f"CTR: {ctr} ({ctr_p}%)\n")

        

def send_report_VK():

    token_vk = "a58a4e00e12767ccfcc9c88fc0337b9b6c001a73b3ea8e687de3181caef0644055c0395e21fe7ae17c531"
    chat_id = 1

    my_id = 65283794
    vk_session = vk_api.VkApi(token=token_vk)
    vk = vk_session.get_api()

    path_to_file = './report.txt'
    file_name = 'advertisement_account.txt'

    upload_url = vk.docs.getMessagesUploadServer(peer_id=my_id)["upload_url"]
    file = {'file': (file_name, open(path_to_file, 'rb'))}

    response = requests.post(upload_url, files=file)
    json_data = json.loads(response.text)

    saved_file = vk.docs.save(file=json_data['file'], title=file_name)
    attachment = 'doc{}_{}'.format(saved_file['doc']['owner_id'], saved_file['doc']['id'])

    vk.messages.send(
                        chat_id=chat_id,
                        random_id=random.randint(1, 2 ** 31),
                        message='Отчёт по объявлению за 02 апреля',
                        attachment=attachment)
        


def action():
    
    path = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR-ti6Su94955DZ4Tky8EbwifpgZf_dTjpBdiVH0Ukhsq94jZdqoHuUytZsFZKfwpXEUCKRFteJRc9P/pub?gid=889004448&single=true&output=csv'
    date = '2019-04-02'
    
    final_df, ad_id = report_DataFrame(path, date)

    text_report_creation(ad_id, final_df)

    send_report_VK()



default_args = {
    'owner': 'i-babchuk',
    'depends_on_past': False,
    'retries': 0
}


dag = DAG('Python_report_sender_i.babchuk', 
          default_args=default_args,
          schedule_interval='0 12 * * 1',
          start_date = datetime(2021, 2, 12))


task = PythonOperator(task_id='send_report_to_VK', 
                    python_callable=action,
                    dag=dag)


