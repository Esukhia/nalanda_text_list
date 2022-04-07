import re
import csv
from pathlib import Path
import yaml


def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys=False, allow_unicode=True,)

def preprocess_page(page):
    page = re.sub('བ-', 'b-', page)
    page = re.sub('ན-', 'a-', page)
    page = re.sub('བ$', 'b', page)
    page = re.sub('ན$', 'a', page)
    if "-" in page:
        page = re.sub('[\u0F00-\u0FDA]', '', page)
    else:
        page = ""
    return page


def get_page(nalanda_text_info, pub):
    page = ""
    if pub == "pedurma" and nalanda_text_info[8]:
        page = nalanda_text_info[8]
    elif pub == "derge" and nalanda_text_info[10]:
        page = preprocess_page(nalanda_text_info[10])
    elif pub == "peking" and nalanda_text_info[9]:
        page = preprocess_page(nalanda_text_info[9])
    return page

def parse_kunsel_melong():
    karchak_file = open("kunsel_melong.csv")

    karchak_csvreader = csv.reader(karchak_file)

    karchak = {}
    rows = []
    for row in karchak_csvreader:
            rows.append(row)
    for text_walker, nalanda_text_info in enumerate(rows[1:]):
        print(nalanda_text_info[0])
        cur_text = {
            'title': nalanda_text_info[2],
            "derge_page": "",
            "peking_page": "",
            "pedurma_page": ""
        }
        derge_page = get_page(nalanda_text_info, pub="derge")
        cur_text['derge_page'] = derge_page
        peking_page = get_page(nalanda_text_info, pub="peking")
        cur_text['peking_page'] = peking_page
        peking_page = get_page(nalanda_text_info, pub="pedurma")
        cur_text['pedurma_page'] = peking_page
        karchak[text_walker] = cur_text
    return karchak

if __name__ == "__main__":
    kunsel_melong = parse_kunsel_melong()
    Path('./kunsel_melong_karchak.yml').write_text(to_yaml(kunsel_melong), encoding='utf-8')