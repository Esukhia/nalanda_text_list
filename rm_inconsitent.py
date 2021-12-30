from pathlib import Path



def rm_inconsistent_text(text_list, text_dir):
    for text_id in text_list:
        (text_dir / f"D{text_id}.txt").unlink()
    

if __name__ == "__main__":
    inconsistent_text_list = Path('./inconsistent_namsel.txt').read_text(encoding='utf-8').splitlines()
    text_dir = Path('./hfml/namsel_pedurma')
    rm_inconsistent_text(inconsistent_text_list, text_dir)
