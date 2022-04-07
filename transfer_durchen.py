import re

from pathlib import Path

def get_pages(vol_text):
    result = []
    pg_text = ""
    pages = re.split(r"(〔[𰵀-󴉱]?\d+〕)", vol_text)
    for i, page in enumerate(pages[1:]):
        if i % 2 == 0:
            pg_text += page
        else:
            pg_text += page
            result.append(pg_text)
            pg_text = ""
    return result

def to_nam_durchen(page):
    page = re.sub("<s(\d+)?>", "<r\g<1>>", page)
    page = re.sub("\n(\d+)", "\n<u\g<1>>", page)
    return page

def transfer_durchen(derge_text, namsel_text, text_id, vol_id):
    derge_text = re.sub('^(〔[𰵀-󴉱]?\d+〕\n)', '\g<1>{'+text_id+'}',derge_text)
    namsel_text = namsel_text.replace("{}", "")
    derge_pages = get_pages(derge_text)
    nam_pages = get_pages(namsel_text)
    new_nam_text = ''
    for d_p, n_p in zip(derge_pages, nam_pages):
        if "<d" in d_p:
            new_nam_text += to_nam_durchen(d_p)
        else:
            new_nam_text += n_p
    Path(f'./hfml/new_derge/{text_id}_{vol_id}.txt').write_text(derge_text, encoding='utf-8')
    Path(f'./hfml/new_namsel/{text_id}_{vol_id}.txt').write_text(new_nam_text, encoding='utf-8')


if __name__ == "__main__":
    derge_paths = list(Path("./hfml/derge_google_pedurma").iterdir())
    derge_paths.sort()
    for derge_path in derge_paths:
        text_id = derge_path.stem[:-5]
        vol_id = derge_path.stem[-4:]
        derge_text = derge_path.read_text(encoding='utf-8')
        namsel_text = Path(f'./hfml/namsel_pedurma/{text_id}_{vol_id}.txt').read_text(encoding='utf-8')
        transfer_durchen(derge_text, namsel_text, text_id, vol_id)