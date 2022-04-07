import re
import csv
from pathlib import Path
import yaml


def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys=False, allow_unicode=True,)

def get_page(nalanda_text_info, pub):
    start_page = ""
    end_page = ""
    if pub == "derge" and nalanda_text_info[4]:
        start_page = re.search('\d+(a|b)', nalanda_text_info[4])[0]
        end_page = re.search('\d+(a|b)', nalanda_text_info[6])[0]
    elif pub == "peking" and nalanda_text_info[9]:
        start_page = re.search('\d+(a|b)', nalanda_text_info[9])[0]
        end_page = re.search('\d+(a|b)', nalanda_text_info[11])[0]
    page = f"{start_page}-{end_page}"
    return page

def get_nalanda_text(esu_karchak_csvreader):
    text_title_id_mapping = {}
    rows = []
    for row in esu_karchak_csvreader:
            rows.append(row)
    for text_walker, nalanda_text_info in enumerate(rows[2:]):
        print(nalanda_text_info[0])
        if nalanda_text_info[0] == '22':
            print('check')
        text_title = nalanda_text_info[1]
        cur_text = {
            "title": text_title,
            "work_id": "",
            "derge_page": "",
            "peking_page": ""
        }
        
        if "D" in nalanda_text_info[2]:
            cur_text["work_id"] = nalanda_text_info[2]
        elif "N" in nalanda_text_info[12]:
            cur_text["work_id"] = nalanda_text_info[12]
        elif "Q" in nalanda_text_info[7]:
            cur_text["work_id"] = nalanda_text_info[7]
        elif "C" in nalanda_text_info[17]:
            cur_text["work_id"] = nalanda_text_info[17]
        elif "GT" in nalanda_text_info[22]:
            cur_text["work_id"] = nalanda_text_info[22]
        else:
            cur_text["work_id"] = ""
        derge_page = get_page(nalanda_text_info, pub="derge")
        cur_text['derge_page'] = derge_page
        peking_page = get_page(nalanda_text_info, pub="peking")
        cur_text['peking_page'] = peking_page
        text_title_id_mapping[text_walker] = cur_text
    return text_title_id_mapping

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def get_nalanda_text_list():
    nalanda_texts = []
    nalanda_text_mapping = from_yaml(Path('./nalanda_text_title_id_mapping.yml'))
    for _, text in nalanda_text_mapping.items():
        nalanda_texts.append(text['work_id'])
    nalanda_texts.sort()
    Path('./nalanda_text_list.txt').write_text("\n".join(nalanda_texts), encoding='utf-8')

    
if __name__ == "__main__":
    karchak_file = open("Nalanda_location.csv")

    esu_karchak_csvreader = csv.reader(karchak_file)
    text_title_id_mapping = get_nalanda_text(esu_karchak_csvreader)
    Path('./nalanda_text_title_id_mapping.yml').write_text(to_yaml(text_title_id_mapping), encoding="utf-8")
    # get_nalanda_text()