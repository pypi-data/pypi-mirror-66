import requests
import json

def prepare_data_from_staturl(get_stat_url):
    data_stat_iter1 = requests.get(get_stat_url)
    data_stat_iter2_content = data_stat_iter1.content
    data_stat_json = json.loads(data_stat_iter2_content)

    data11 = ''
    for key in data_stat_json:
        if key != '':
            data11 = data11 + 'mhub,info=stat,name=' + key + ' value=' + data_stat_json[key] + '\n'
    return data11


def mhubtest():

    url = 'https://admin.br.mts.by/get_stat'
    hh = requests.get(url)
    a1 = hh.content

    a2 = json.loads(a1)

    print(hh.status_code)
    print(a2)


    for key in a2:
       print(key)
       print(a2[key])
       print("\n")
