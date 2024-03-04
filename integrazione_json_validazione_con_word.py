"""
Prende in input singolo json di validazione e cartella contentente annotazioni word e restituisce lo stesso json con tag word aggiunti alla chiave ordine tag
"""
import json
import zipfile
from pathlib import Path
from word_comments_extraction_utils import return_comments_dicts
from datetime import date
from logger import logger


file_validazione = "20230419_valid_tag"
doc_folder = Path(r"C:\Users\smarotta\Desktop\mirco_file_validazione\output")


with open(f"{file_validazione}.json", "r", encoding="utf8") as f:
    data = json.load(f)

for obj in data:
    idpratica = obj["ID_Pratica"]
    idchiamata = obj["idchiamata"]
    id_ = f"{idpratica}_{idchiamata}"

    ordine_tag = obj["tag"]["ordine_tag"]

    if ordine_tag:
        #  rimozione testi duplicati e accorpamento tag (per i casi in cui a uno stesso segmento di testo sono stati assegnati più di un tag)
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

        if ordine_tag_no_dups and word_tags:  # se ci sono tag provenienti da word
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
        
        if ordine_tag_no_dups_with_word:
            obj["tag"]["ordine_tag"] = ordine_tag_no_dups_with_word  # updating the original ordine_tag with the modified one

with open(f"{file_validazione}_updated.json", "w", encoding="utf8") as updated_file:
    json.dump(data, updated_file, ensure_ascii=False, indent=4)