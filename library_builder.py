"""
Build library of text files from valid_tag.json
"""

import json
from pathlib import Path

file_name = "20230419_valid_tag"
txt_path_operatore = Path(f"output/operatore/{file_name}_txt")
ann_path_operatore = Path(f"output/operatore/{file_name}_ann")
txt_path_debitore = Path(f"output/debitore/{file_name}_txt")
ann_path_debitore = Path(f"output/debitore/{file_name}_ann")

txt_path_operatore.mkdir(parents=True, exist_ok=True)
ann_path_operatore.mkdir(parents=True, exist_ok=True)
txt_path_debitore.mkdir(parents=True, exist_ok=True)
ann_path_debitore.mkdir(parents=True, exist_ok=True)

with open(f"{file_name}.json", "r", encoding="utf8") as f:
    data = json.load(f)

for obj in data:
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

        word_tags = obj["tag"].get("word_tags")
        if ordine_tag_no_dups and word_tags:  # se ci sono tag proveniente da word
            for tag_obj in word_tags:
                tag = tag_obj["tag"]
                testo = tag_obj["testo"]

                ordine_tag_no_dups.append(
                    {
                        "testo": testo,
                         "tags": [
                             {"tag": tag}
                         ]
                     }
                )

        #  identificazione speaker e creazione files
        for idx, tag_obj in enumerate(ordine_tag_no_dups):
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

