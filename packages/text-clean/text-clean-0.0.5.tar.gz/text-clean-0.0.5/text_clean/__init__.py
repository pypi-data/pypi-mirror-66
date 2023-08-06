import os
import sys
import requests
import logging
import text_clean.text_clean as text_clean

dependent_files = [
    "t2s_char_project.txt",
    "t2s_drop_project.txt",
    "t2s_word_project.txt",
    "digital_letter_normal.txt",
    "char_keep.txt"

]


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    stream=sys.stdout)


class TextClean(object):
    def __init__(self, a=True, b=True, c=False, update=False):
        data_path = os.getcwd() + "/data/"
        if not os.path.exists(data_path):
            logging.info("mkdir 'data/'.")
            os.makedirs(data_path)
        for file in dependent_files:
            if not os.path.exists(data_path + file) or update:
                logging.info("Downloading t2s_char_project.txt")
                _url = "https://raw.githubusercontent.com/mikuh/text_clean/master/data/{}".format(
                    file)
                _save_path = os.path.join(data_path, file)
                print(_save_path)
                if not self._download(_save_path, _url):
                    raise RuntimeError("File download failed.")
        text_clean.init(a, b, c)

    def _download(self, save_path, url):
        try:
            resp = requests.get(url)
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(resp.text)
        except Exception as e:
            print('\nError when retrieving the URL:', save_path)
            os.remove(save_path)
            return False
        return True

    def clean(self, text):
        return text_clean.clean(text)


__all__ = ["TextClean"]
