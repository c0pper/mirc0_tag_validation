"""
Build library of text files from valid_tag.json
"""
import datetime
import json
import sys
import zipfile
from pathlib import Path
from word_comments_extraction_utils import return_comments_dicts
from datetime import date
from logger import logger

WRITE_FILES = 0

# #  logger
# logger = logging.getLogger("logger")
# logger.setLevel(logging.DEBUG)
#
# logFileFormatter = logging.Formatter(
#     fmt=f"%(levelname)s %(asctime)s \t %(pathname)s F%(funcName)s L%(lineno)s - %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S",
# )
# fileHandler = logging.FileHandler(filename=f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
# fileHandler.setFormatter(logFileFormatter)
# fileHandler.setLevel(level=logging.INFO)
#
# logger.addHandler(fileHandler)

file_validazione = "20230419_valid_tag"
doc_folder = Path(r"C:\Users\smarotta\Desktop\mirco_file_validazione\output")
txt_path_operatore = Path(f"output/{date.today()}_{file_validazione}/operatore/txt")
ann_path_operatore = Path(f"output/{date.today()}_{file_validazione}/operatore/ann")
txt_path_debitore = Path(f"output/{date.today()}_{file_validazione}/debitore/txt")
ann_path_debitore = Path(f"output/{date.today()}_{file_validazione}/debitore/ann")

txt_path_operatore.mkdir(parents=True, exist_ok=True)
ann_path_operatore.mkdir(parents=True, exist_ok=True)
txt_path_debitore.mkdir(parents=True, exist_ok=True)
ann_path_debitore.mkdir(parents=True, exist_ok=True)

with open(f"{file_validazione}.json", "r", encoding="utf8") as f:
    data = json.load(f)

for obj in data[:3]:
    idpratica = obj["ID_Pratica"]
    idchiamata = obj["idchiamata"]
    id_ = f"{idpratica}_{idchiamata}"
    operatore_text = obj["tag"]["operatore"]["testo_operatore"]
    debitore_text = obj["tag"]["debitore"]["testo_debitore"]
    speaker = ""

    all_tags_debitore = obj["tag"]["debitore"]["analisi_debitore"]["intenzionalita"] + \
                        obj["tag"]["debitore"]["analisi_debitore"]["informative"]
    all_tags_debitore = [list(x.keys())[0] for x in all_tags_debitore]

    all_tags_operatore = obj["tag"]["operatore"]["analisi_operatore"]["presentazione"] + \
                        obj["tag"]["operatore"]["analisi_operatore"]["trattativa"] + \
                        obj["tag"]["operatore"]["analisi_operatore"]["chiusura"]
    all_tags_operatore = [list(x.keys())[0] for x in all_tags_operatore]

    ordine_tag = obj["tag"]["ordine_tag"]

    if ordine_tag:
        #  rimozione testi duplicati e accorpamento tag
        ordine_tag_no_dups = []
        for tag_obj in ordine_tag:
            tag = tag_obj["tag"]
            testo = tag_obj["testo"]
            errato = tag_obj.get("errato", False)

            texts_in_ordine_tag_no_dups = [list(x.values())[0] for x in ordine_tag_no_dups]  # array con tutti i testi in ordine_tag_no_dups (inizialmente vuoto)
            if testo not in texts_in_ordine_tag_no_dups:
                #  se il testo non c'è già appendiamo l'intero dizionario con testo, tag e status errato
                ordine_tag_no_dups.append(
                    {
                        "testo": testo,
                        "tags": [
                            {
                                "tag": tag,
                                "errato": errato
                            }
                        ]
                    }
                )
            else:
                #  se il testo c'è già, aggiorniamo l'elenco di tags con il tag nuovo che si riferisce allo stesso testo
                for d in ordine_tag_no_dups:
                    if d["testo"] == testo:
                        d["tags"].append(
                            {
                                "tag": tag,
                                "errato": errato
                            }
                        )

        # Trattamento commenti word
        # identificazione file word relativo alla chiamata
        for doc in doc_folder.glob("*"):
            if idchiamata in doc.name:
                path_file_trascrizione = doc_folder / doc.name
                try:
                    word_tags = return_comments_dicts(path_file_trascrizione)
                except zipfile.BadZipFile:
                    print(path_file_trascrizione)

        if ordine_tag_no_dups and word_tags:  # se ci sono tag proveniente da word
            ordine_tag_no_dups_with_word = ordine_tag_no_dups.copy()
            for tag_obj in word_tags:
                tag = tag_obj["tag"]
                testo = tag_obj["testo"]

                # check se il testo riportato in word non è già presente in uno dei tag estratti dal modulo linguistico
                for tag_obj2 in ordine_tag_no_dups:

                    # se il testo del word è assente nel testo di validazione -> inserire
                    if testo not in tag_obj2["testo"]:
                        print(f"{testo} not in {tag_obj2['testo']}")
                        word_tag_obj = {
                            "testo": testo,
                            "tags": [
                             {"tag": tag}
                            ],
                            "from_word": True
                        }

                    elif testo in tag_obj2["testo"]:
                        tags_presenti = [x["tag"] for x in tag_obj2["tags"] if not x.get("errato")]
                        if tag not in tags_presenti:
                            # se il testo del word è presente nel testo di validazione ma i tag sono diversi -> inserire
                            logger.warning(f"id chiamata: {idchiamata}\n[tag diversi] {testo} FOUND IN {tag_obj2['testo']} \n\t tag {tag} not in {tags_presenti}\n")
                            word_tag_obj = {
                                "testo": testo,
                                "tags": [
                                 {"tag": tag}
                                ],
                                "from_word": True
                            }
                        else:
                            # se il testo del word è presente nel testo di validazione e i tag sono uguali -> non inserire
                            logger.warning(f"id chiamata: {idchiamata}\n[tag uguali] {testo} FOUND IN {tag_obj2['testo']} \n\t tag {tag} FOUND IN {tags_presenti}\n")
                            word_tag_obj = False
                            break

                if word_tag_obj:
                    ordine_tag_no_dups_with_word.append(word_tag_obj)
            print(f"\n\n{id_}")
            print(ordine_tag_no_dups_with_word)
        else:
            raise FileNotFoundError(f"No word comments found for file {doc.name}")

        #  identificazione speaker e creazione files
        if WRITE_FILES:
            for idx, tag_obj in enumerate(ordine_tag_no_dups_with_word):
                tags = tag_obj["tags"]
                testo = tag_obj["testo"]

                if tags[0]["tag"] in all_tags_debitore:
                    speaker = "debitore"
                elif tags[0]["tag"] in all_tags_operatore:
                    speaker = "operatore"

                #  Creazione txt
                if speaker == "operatore":
                    with open(f"{txt_path_operatore}/{id_}_operatore_{idx}.txt", "w", encoding="utf-8") as f:
                        f.write(testo)
                elif speaker == "debitore":
                    with open(f"{txt_path_debitore}/{id_}_debitore_{idx}.txt", "w", encoding="utf-8") as f:
                        f.write(testo)

                #  Creazione ann
                if speaker == "operatore":
                    with open(f"{ann_path_operatore}/{id_}_operatore_{idx}.ann", "a", encoding="utf-8") as f:
                        for tag_obj in tags:
                            tag = tag_obj["tag"]
                            errato = tag_obj.get("errato", False)
                            if not errato:
                                f.write(f"C0		{tag}\n")

                elif speaker == "debitore":
                    with open(f"{ann_path_debitore}/{id_}_debitore_{idx}.ann", "a", encoding="utf-8") as f:
                        for tag_obj in tags:
                            tag = tag_obj["tag"]
                            errato = tag_obj.get("errato", False)
                            if not errato:
                                f.write(f"C0		{tag}\n")

