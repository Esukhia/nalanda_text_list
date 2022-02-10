import yaml
from pathlib import Path
from openpecha.serializers import HFMLSerializer

def from_yaml(yml_path):
    return yaml.safe_load(yml_path.read_text(encoding="utf-8"))

def get_hfml_text(opf_path, text_id, index=None):
    """Return hmfl of text from the pecha opf

    Args:
        opf_path (str): opf path
        text_id (str): text id
        index (dict, optional): pecha index. Defaults to None.

    Returns:
        dict: vol id as key and hfml as the content
    """
    serializer = HFMLSerializer(
        opf_path, text_id=text_id, index_layer=index, layers=["Pagination", "Durchen"]
    )
    serializer.apply_layers()
    hfml_text = serializer.get_result()
    return hfml_text


def save_hfml(text_id, hfml, parma):
    for vol_id, hfml_text in hfml.items():
        Path(f'./hfml/{parma}/{text_id}_{vol_id}.txt').write_text(hfml_text, encoding='utf-8')

def get_text_list(list_path):
    text_list = list_path.read_text(encoding='utf-8').splitlines()
    text_list = list(set(text_list))
    text_list.sort()
    return text_list

if __name__ == "__main__":
    # parma = "derge_google_pedurma"
    # opf_path = Path('./opfs/12d32eb31c1a4cc59741cda99ebc7211.opf')
    
    parma = "namsel_pedurma"
    opf_path = Path('./opfs/187ed94f85154ea5b1ac374a651e1770.opf')
    text_ids = get_text_list(Path('./nalanda_text_need_to_prepare.txt'))
    index = from_yaml((opf_path / "index.yml"))
    for text_id in text_ids:
        hfmls = get_hfml_text(opf_path, text_id, index=index)
        save_hfml(text_id, hfmls, parma)
        print(f'{text_id} completed ..')