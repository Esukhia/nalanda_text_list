import re
import csv
from pathlib import Path
import yaml

from fuzzy_match import algorithims

def to_yaml(dict_):
    return yaml.safe_dump(dict_, sort_keys=False, allow_unicode=True,)

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def get_similarity(title1, title2):
    similarity = algorithims.cosine(title1,title2)
    return similarity

def get_pedurma_page(nalanda_text, kunsel_melong):
    pedurma_page = ""
    author_code = ""
    for _, text in kunsel_melong.items():
        if get_similarity(text['title'], nalanda_text['title']) > 0.9 and (nalanda_text['derge_page'] == text['derge_page'] or nalanda_text['peking_page'] == text['peking_page']):
            pedurma_page,author_code = text['pedurma_page'], text['author_code']
    return pedurma_page, author_code

def nalanda_karchak():
    nalanda_text_karchak = from_yaml(Path('./nalanda_text_title_id_mapping.yml'))
    kunsel_melong = from_yaml(Path('./kunsel_melong_karchak.yml'))
    for text_id, nalanda_text in nalanda_text_karchak.items():
        pedurma_page, author_code = get_pedurma_page(nalanda_text, kunsel_melong)
        nalanda_text_karchak[text_id]['author_code'] = author_code
        nalanda_text_karchak[text_id]['pedurma_page'] = pedurma_page
    return nalanda_text_karchak

if __name__ == "__main__":
    nalanda_txt_karchak = nalanda_karchak()
    Path('./nalanda_karchak.yml').write_text(to_yaml(nalanda_txt_karchak), encoding='utf-8')
