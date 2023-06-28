import json

# json_string = """
# [
#    {
#       "ID_Pratica":"2043081883",
#       "idchiamata":"09c708bb-803e-4308-8b03-e8f003e089b3",
#       "tag":{
#          "testo_intero":"S0: pronto sì pronto buongiorno signora Falzone\nS1: sì mi dica buongiorno salve sono il signor Scarcella signora sta chiamando dall' Italia per conto di FCE Bank\nS0: per quanto riguarda il contratto è intestato a lei della macchina\nS0: come sempre il corpo della chiamata è registrata come dal sito lei è nata il 21 uno 67 giusto Pietraperzia signora chiamato solo per sapere se avete messo a posto la rata di luglio quella scaduta giorno venti\nS0: oggi ne abbiamo 21 22 oggi la vado a pagare e mi raccomando signora così risulta\nS0: però va bene va bene ok buongiorno salve salve\n",
#          "operatore":{
#             "testo_operatore":"S1: sì mi dica buongiorno salve sono il signor Scarcella signora sta chiamando dall' Italia per conto di FCE Bank\n",
#             "analisi_operatore":{
#                "callId":"09c708bb-803e-4308-8b03-e8f003e089b3",
#                "presentazione":[
#                   {
#                      "rispetto_script":false
#                   },
#                   {
#                      "presentazione_societa":true,
#                      "S1: sì mi dica buongiorno salve sono il signor Scarcella signora sta chiamando dall' Italia per conto di FCE Bank\n":[
#                         {
#                            "start":0,
#                            "end":2
#                         },
#                         {
#                            "start":64,
#                            "end":67
#                         },
#                         {
#                            "start":4,
#                            "end":5
#                         },
#                         {
#                            "start":68,
#                            "end":77
#                         },
#                         {
#                            "start":39,
#                            "end":45
#                         },
#                         {
#                            "start":78,
#                            "end":82
#                         },
#                         {
#                            "start":14,
#                            "end":24
#                         },
#                         {
#                            "start":83,
#                            "end":89
#                         },
#                         {
#                            "start":56,
#                            "end":63
#                         },
#                         {
#                            "start":25,
#                            "end":30
#                         },
#                         {
#                            "start":90,
#                            "end":102
#                         },
#                         {
#                            "start":94,
#                            "end":99
#                         },
#                         {
#                            "start":31,
#                            "end":35
#                         },
#                         {
#                            "sentence_start":48
#                         }
#                      ]
#                   },
#                   {
#                      "presentazione_prodotto":false
#                   },
#                   {
#                      "dettaglio_esposizione":false
#                   },
#                   {
#                      "interlocutore_alternativo":false
#                   },
#                   {
#                      "recapiti_alternativi":false
#                   },
#                   {
#                      "stato_attivita_impresa":false
#                   }
#                ],
#                "trattativa":[
#                   {
#                      "scadenza_pagamento":false
#                   },
#                   {
#                      "volonta_risolutiva":false
#                   },
#                   {
#                      "pagamento_acconto":false
#                   },
#                   {
#                      "appuntamento":false
#                   },
#                   {
#                      "bene_finanziato":false
#                   },
#                   {
#                      "situazione_economica":false
#                   },
#                   {
#                      "altre_disponibilita":false
#                   },
#                   {
#                      "nucleo_familiare":false
#                   },
#                   {
#                      "capacita_di_rimborso":false
#                   },
#                   {
#                      "impegni_economici":false
#                   },
#                   {
#                      "proposta_agevolazione":false
#                   },
#                   {
#                      "proposta_saldo_e_stralcio":false
#                   },
#                   {
#                      "proposto_pdr":false
#                   },
#                   {
#                      "proposto_rifinanziamento":false
#                   },
#                   {
#                      "proposto_consolidamento":false
#                   },
#                   {
#                      "antiusura":false
#                   },
#                   {
#                      "proposto_accodamento":false
#                   },
#                   {
#                      "proiezione_medio_lungo_termine":false
#                   },
#                   {
#                      "sostegno_da_terzi":false
#                   },
#                   {
#                      "tempistiche_introiti":false
#                   },
#                   {
#                      "pagamento_effettuato":false
#                   },
#                   {
#                      "utilizzo_leve":false
#                   },
#                   {
#                      "vantaggio":false
#                   }
#                ],
#                "chiusura":[
#                   {
#                      "conferma_accordi":false
#                   },
#                   {
#                      "estremi_di_pagamento":false
#                   },
#                   {
#                      "richiesto_riscontro_di_pagamento":false
#                   },
#                   {
#                      "invio_modulistica":false
#                   },
#                   {
#                      "richiesta_documenti":false
#                   },
#                   {
#                      "invito_a_confronto_diretto":false
#                   }
#                ]
#             }
#          },
#          "debitore":{
#             "testo_debitore":"S0: pronto sì pronto buongiorno signora Falzone\nS0: per quanto riguarda il contratto è intestato a lei della macchina\nS0: come sempre il corpo della chiamata è registrata come dal sito lei è nata il 21 uno 67 giusto Pietraperzia signora chiamato solo per sapere se avete messo a posto la rata di luglio quella scaduta giorno venti\nS0: oggi ne abbiamo 21 22 oggi la vado a pagare e mi raccomando signora così risulta\nS0: però va bene va bene ok buongiorno salve salve\n",
#             "analisi_debitore":{
#                "callId":"09c708bb-803e-4308-8b03-e8f003e089b3",
#                "intenzionalita":[
#                   {
#                      "attesa_liquidita":false
#                   },
#                   {
#                      "chiede_rimanda_appuntamento":false
#                   },
#                   {
#                      "confronto_diretto_mandante":false
#                   },
#                   {
#                      "contestazione":false
#                   },
#                   {
#                      "dettagli_modalita_pagamento":false
#                   },
#                   {
#                      "ignora_debito":false
#                   },
#                   {
#                      "maggiori_dettagli_debito":false
#                   },
#                   {
#                      "potenziale_reclamo":false
#                   },
#                   {
#                      "richiesta_agevolazione":false
#                   },
#                   {
#                      "rifiuta_pagamento":false
#                   },
#                   {
#                      "volonta_pagamento":true,
#                      "S0: oggi ne abbiamo 21 22 oggi la vado a pagare e mi raccomando signora così risulta\n":[
#                         {
#                            "start":34,
#                            "end":38
#                         },
#                         {
#                            "start":39,
#                            "end":40
#                         },
#                         {
#                            "start":41,
#                            "end":47
#                         },
#                         {
#                            "sentence_start":445
#                         }
#                      ]
#                   },
#                   {
#                      "data_pagamento":true,
#                      "S0: oggi ne abbiamo 21 22 oggi la vado a pagare e mi raccomando signora così risulta\n":[
#                         {
#                            "start":4,
#                            "end":8
#                         },
#                         {
#                            "start":20,
#                            "end":22
#                         },
#                         {
#                            "start":26,
#                            "end":30
#                         },
#                         {
#                            "start":34,
#                            "end":38
#                         },
#                         {
#                            "start":41,
#                            "end":47
#                         },
#                         {
#                            "sentence_start":445
#                         }
#                      ]
#                   }
#                ],
#                "informative":[
#                   {
#                      "accordi_presenti":false
#                   },
#                   {
#                      "cliente_assente":false
#                   },
#                   {
#                      "debito_gia_pagato":false
#                   },
#                   {
#                      "difficolta_economiche":false
#                   },
#                   {
#                      "garanzie":false
#                   },
#                   {
#                      "ha_fonti_reddito":false
#                   },
#                   {
#                      "ha_qualcuno_che_puo_aiutare":false
#                   },
#                   {
#                      "importo_sostenibile":false
#                   },
#                   {
#                      "proposta_agevolazione":false
#                   },
#                   {
#                      "pagamento_non_effettuato":true,
#                      "S0: come sempre il corpo della chiamata è registrata come dal sito lei è nata il 21 uno 67 giusto Pietraperzia signora chiamato solo per sapere se avete messo a posto la rata di luglio quella scaduta giorno venti\n":[
#                         {
#                            "start":170,
#                            "end":174
#                         },
#                         {
#                            "start":192,
#                            "end":199
#                         },
#                         {
#                            "sentence_start":232
#                         }
#                      ],
#                      "S0: oggi ne abbiamo 21 22 oggi la vado a pagare e mi raccomando signora così risulta\n":[
#                         {
#                            "start":34,
#                            "end":38
#                         },
#                         {
#                            "start":41,
#                            "end":47
#                         },
#                         {
#                            "sentence_start":445
#                         }
#                      ]
#                   },
#                   {
#                      "procedimento_legale":false
#                   },
#                   {
#                      "prospettiva_temporale":false
#                   },
#                   {
#                      "reale_interlocutore":false
#                   },
#                   {
#                      "salute":false
#                   },
#                   {
#                      "stato_attivita_impresa":false
#                   },
#                   {
#                      "modulistica":false
#                   }
#                ]
#             }
#          },
#          "ordine_tag":[
#             {
#                "tag":"presentazione_societa",
#                "testo":"S1: sì mi dica buongiorno salve sono il signor Scarcella signora sta chiamando dall' Italia per conto di FCE Bank\n"
#             },
#             {
#                "tag":"pagamento_non_effettuato",
#                "testo":"S0: come sempre il corpo della chiamata è registrata come dal sito lei è nata il 21 uno 67 giusto Pietraperzia signora chiamato solo per sapere se avete messo a posto la rata di luglio quella scaduta giorno venti\n",
#                "errato":true
#             },
#             {
#                "tag":"data_pagamento",
#                "testo":"S0: oggi ne abbiamo 21 22 oggi la vado a pagare e mi raccomando signora così risulta\n"
#             },
#             {
#                "tag":"pagamento_non_effettuato",
#                "testo":"S0: oggi ne abbiamo 21 22 oggi la vado a pagare e mi raccomando signora così risulta\n",
#                "errato":true
#             },
#             {
#                "tag":"volonta_pagamento",
#                "testo":"S0: oggi ne abbiamo 21 22 oggi la vado a pagare e mi raccomando signora così risulta\n"
#             }
#          ]
#       }
#    }
# ]
# """


# Load the JSON data from a file or a string variable
with open("20230419_valid_tag.json", "r", encoding="utf8") as j:
    data = json.load(j, strict=False)

count_operatore_errors = 0
count_debitore_errors = 0

# Iterate over the objects in the "ordine_tag" array
for obj in data:
    if obj.get("tag"):
        # Iterate over the objects in the "ordine_tag" array
        for tag in obj['tag']['ordine_tag']:
            # Check if the "errato" key exists and has a truthy value
            if 'errato' in tag.keys():
                testo_errato = tag["testo"]
                # Check if the "testo" value of the object exists in the "analisi_debitore" and "analisi_operatore" arrays
                testo_debitore = obj["tag"].get("debitore", "").get("testo_debitore", "")
                testo_operatore = obj["tag"].get("operatore", "").get("testo_operatore", "")
                if testo_errato in testo_operatore:
                    # Set a flag indicating that the error occurred in the text said by the "operatore"
                    count_operatore_errors += 1
                elif testo_errato in testo_debitore:
                    # Set a flag indicating that the error occurred in the text said by the "debitore"
                    count_debitore_errors += 1

print("operatore", count_operatore_errors)
print("debitore", count_debitore_errors)