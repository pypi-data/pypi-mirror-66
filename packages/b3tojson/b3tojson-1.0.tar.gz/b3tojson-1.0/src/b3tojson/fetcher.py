import requests
import zipfile
import codecs

from os import path, remove

B3_NEGOTIABLE_URL = "http://bvmf.bmfbovespa.com.br/suplemento/ExecutaAcaoDownload.asp?arquivo=Titulos_Negociaveis.zip&server=L"
B3_ENCODING = "iso-8859-1"
FILES_DIR = "files"
TEMP_ZIP = path.join(FILES_DIR, "temp.zip")
JSON_FILE = path.join(FILES_DIR, "stocks_data.json")


def get_b3_data():
    response = requests.get(B3_NEGOTIABLE_URL, stream=True)

    if response.status_code != 200:
        print(f"Could not get resource from server! Status code got: {response.status_code}")
        raise Exception

    with open(TEMP_ZIP, "wb") as fd:
        for chunk in response.iter_content(chunk_size=512):
            fd.write(chunk)

    b3_name = None
    with zipfile.ZipFile(TEMP_ZIP, 'r') as zip_obj:
        zip_obj.extractall(FILES_DIR)

        b3_name = path.join(FILES_DIR, zip_obj.namelist().pop())
        _process_file(b3_name)

    remove(TEMP_ZIP)
    return b3_name


def _process_file(b3_name):
    """
    Process downloaded file in order to fix encoding.

    Args:
        b3_name(str): Path to the original file
    """
    with codecs.open(b3_name, 'r', B3_ENCODING) as source_file:
        contents = source_file.read()

    with codecs.open(b3_name, 'w', 'utf-8') as destination_file:
        destination_file.write(contents)
