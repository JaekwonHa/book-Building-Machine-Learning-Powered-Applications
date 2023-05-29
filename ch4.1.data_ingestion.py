import xml.etree.ElementTree as EIT
import pandas as pd

from bs4 import BeautifulSoup
from tqdm import tqdm


def parse_xml_to_csv(path, save_path=None):
    """
    .xml 덤프 파일을 열고 텍스트를 토큰화하여 csv로 변환합니다.
    :param path:
    :param save_path:
    :return:
    """

    doc = EIT.parse(path)
    root = doc.getroot()

    all_rows = [row.attrib for row in root.findall("row")]

    for item in tqdm(all_rows):
        soup = BeautifulSoup(item["Body"], features="html.parser")
        item["body_text"] = soup.get_text()

    df = pd.DataFrame.from_dict(all_rows)
    if save_path:
        df.to_csv(save_path)
    return df
