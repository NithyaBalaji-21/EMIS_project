import requests
import re
from bs4 import BeautifulSoup
import config


def get_data_from_git(collection_patient):
    url = config.GIT_URL
    r = requests.get(url)
    print("Response code -", r.status_code)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, features="html.parser")
    a_tags = soup.find_all('a')
    file_urls = ['https://github.com' + re.sub('/blob', '/raw', link.get('href'))
                 for link in a_tags  if '.json' in link.get('href')]
    print("Total json files -", len(file_urls))

    upload_json_to_mongo(file_urls, collection_patient)


def upload_json_to_mongo(file_urls, collection_patient):

    x = delete_collection(collection_patient)
    print(x.deleted_count, " documents deleted.")

    for filename in file_urls:
        response = requests.get(filename)
        data = response.json()
        collection_patient.insert_one(data)

    print(" Documents uploaded successfully !")
    pass


def delete_collection(collection_patient):
    x = collection_patient.delete_many({})

    return x
