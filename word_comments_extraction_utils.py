import zipfile
from typing import Union
from bs4 import BeautifulSoup as Soup
import docx
from pathlib import Path
import re
from entities import taxonomy


def normalize_fucked_encoding(string) -> str:
    """
    Manually replace bad characters. See https://www.i18nqa.com/debug/utf8-debug.html

    :param string: text to be normalized
    :return: normalized string
    """
    char_to_replace = {
        "�": "è",  # almeno prendo la maggior parte dei verbi essere correttamente
        "Ã¬": "ì",
        "Ã©": "é",
        "Ã²": "ò",
        "Ã¨": "è",
        "Ã": "à",
        "Ã¹": "ù",
        "à¹": "ù",
        "Ãˆ": "È",
    }
    for key, value in char_to_replace.items():
        string = string.replace(key, value)
    return string


def get_text_from_doc(filename: Path) -> str:
    """
    Retrieve text from docx file

    :param filename: path of a single word document (.docx)
    :return: text in string form
    """
    doc = docx.Document(filename)
    full_text = []
    for para in doc.paragraphs:
        para.text = normalize_fucked_encoding(para.text)
        full_text.append(para.text)
    return ''.join(full_text).encode('cp1252').decode('ISO-8859-1')



def return_comments_dicts(doc_file_path: Path) -> Union[list, bool]:
    """
    In a word file, for every comment in it creates a dict with the text of the comment, the text on which the
    comment was placed, the start character of the comment and the end character of the comment. Then returns either a list
    of dictionaries (one dictionary per comment in the file), or False if no comment was found in the docx.

    :param doc_file_path: path of a single word document (.docx)
    :return: list of dictionaries (one for each comment) or False
    """

    unzip = zipfile.ZipFile(doc_file_path)
    try:
        comments = Soup(unzip.read('word/comments.xml'), 'lxml')
        doc = unzip.read('word/document.xml').decode()
        txt = get_text_from_doc(doc_file_path)
        txt = re.sub('(S\d+)', r'\n\1', txt)  # newline ogni enunciato
        txt = re.sub(' +', ' ', txt)

        #  populate comments_dicts list with dicts for every comment
        start_loc = {x.group(1): x.start() for x in re.finditer(r'<w:commentRangeStart.*?w:id="(.*?)"', doc)}
        end_loc = {x.group(1): x.end() for x in re.finditer(r'<w:commentRangeEnd.*?w:id="(.*?)".*?>', doc)}
        comments_dicts = []
        for c in comments.find_all('w:comment'):
            c_id = c.attrs['w:id']
            # Use the locations we found earlier to extract the xml fragment from the document for
            # each comment ID, adding spaces to separate any paragraphs in multi-paragraph comments
            xml = re.sub(r'(<w:p .*?>)', r'\1 ', doc[start_loc[c_id]:end_loc[c_id] + 1])
            # print(xml+"\n\n")
            cmt = ''.join(c.findAll(string=True))
            cmt = re.sub(' +', ' ', cmt)
            cmt = re.sub('-', '', cmt)
            text_reference_soup = Soup(xml, 'lxml').findAll(string=True)
            # print(text_reference_soup)
            if len(text_reference_soup) > 1:
                text_reference = "".join(text_reference_soup)
            elif len(text_reference_soup) == 1:
                text_reference = text_reference_soup[0]
            else:
                text_reference = "text reference not found"

            text_reference = normalize_fucked_encoding(text_reference)
            text_reference = re.sub(' +', ' ', text_reference)
            text_reference = re.sub('(S\d+)', r'\n\1', text_reference)

            clean_cmt = re.split(":|,|;", cmt)[0].strip().lower()
            cmt_and_txt = {"tag": taxonomy[clean_cmt], "testo": text_reference,
                           "start": txt.find(text_reference), "end": txt.find(text_reference) + len(text_reference)}
            # print(cmt_and_txt)

            comments_dicts.append(cmt_and_txt)
        return comments_dicts
    except KeyError:
        print(f"No comments found in {doc_file_path.name}")
        return False


if __name__ == '__main__':
    dicts = return_comments_dicts(r"C:\Users\smarotta\Desktop\mirco_file_validazione\output\2042312668_202204201623_6a78108d-3156-4569-8323-5c89e3b2d071_annotato.docx")
    [print(x) for x in dicts]

# Output:
# {'tag': 'rispetto_script', 'testo': "NOMECOGNOME dall' Italia ", 'start': 97, 'end': 122}
# {'tag': 'presentazione_societa', 'testo': "NOMECOGNOME dall' Italia dagli uffici AZIENDA per AZIENDA ", 'start': 97, 'end': 155}
# {'tag': 'rispetto_script', 'testo': 'ricordo che la mia telefonata verrà registrata ', 'start': 157, 'end': 204}  
# {'tag': 'volonta_risolutiva', 'testo': 'lei riesce non fare neanche un bonifico online', 'start': 626, 'end': 672}