import re
import yaml
from pathlib import Path


def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def get_text_list(list_path):
    text_list = list_path.read_text(encoding='utf-8').splitlines()
    text_list = list(set(text_list))
    text_list.sort()
    print(len(text_list))
    return text_list

def map_text_vol(nalanda_text_list, derge_index):
    nalanda_text_vol_mapping = {}
    for uuid, text in derge_index['annotations'].items():
        if text['work_id'] in nalanda_text_list:
            text_vols = []
            for span in text['span']:
                text_vols.append(span['vol'])
            nalanda_text_vol_mapping[text['work_id']] = text_vols
    return nalanda_text_vol_mapping


if __name__ == "__main__":
    nalanda_text_list = get_text_list(Path('./nalanda_text_ready.txt'))
    derge_index = from_yaml(Path('./opfs/P000002.opf/index.yml'))
    text_vol_mapping = map_text_vol(nalanda_text_list, derge_index)
    nalanda_vols = []
    for text_id, vols in text_vol_mapping.items():
        for vol in vols:
            if str(vol) not in nalanda_vols:
                nalanda_vols.append(str(vol))
    Path('./nalanda_text_vol.txt').write_text("\n".join(nalanda_vols), encoding='utf-8')