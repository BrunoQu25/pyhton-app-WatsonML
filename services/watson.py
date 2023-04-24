import os
from flask import request
import requests
import logging
import time
import json

from utils.parser.parser import parse_predictions
from utils.tensorflow import preprocess

from exceptions.unauthorized import Unauthorized
from exceptions.watson_error import WatsonError

def classify():
    logging.info('[CLASSIFY] Inicio de petición')

    # INICIO CAMBIOS
    API_KEY = os.environ.get('APIKEY') # Paste the account APIKEY where the Watson Machine Learning service is
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]
    
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
    dic = request.json
    dic['creditCardAvg'] = dic['creditCardAvg']/1000 #Do not forget to do this. 

    # NOTE: manually define and pass the array(s) of values to be scored in the next line. You can appreciate that dic.age will be
    #       the age you ask to the customer in Watson Assistant.
    
    payload_scoring = {
        "input_data": [
            {
                "fields": [
                    "Age",
                    "Experience",
                    "Income",
                    "ZIP Code",
                    "Family",
                    "CCAvg",
                    "Education",
                    "Mortgage",
                    "Securities Account",
                    "CD Account",
                    "Online",
                    "CreditCard"
                    ],
                    "values": [
                        [
                            dic['age'],
                            dic['experience'],
                            dic['income'],
                            dic['ZIP'],
                            dic['family'],
                            dic['creditCardAvg'],
                            dic['education'],
                            dic['mortgage'],
                            dic['security'],
                            dic['CD'],
                            dic['online'],
                            dic['creditCard']
                        ]
                    ]
            }
        ]
    
    }
    response_scoring = requests.post(os.environ.get('URL'), json=payload_scoring, header = header)
    # REPLACE THE URL WITH YOUR DEPLOY URL.
      
    result = response_scoring.text
    result_json = json.loads(result)
    
    result_keys = result_json['predictions'][0]['fields']
    result_vals = result_json['predictions'][0]['values']
    
    result_dict = dict(zip(result_keys, result_vals[0]))
      
    x = zip(result_keys, result_vals[0])
    
    predict = result_dict["prediction"]
    
    
    
    final = f'Your application is presenting a {predict}'
    return { 'message': final } 
      
    print("final: ", final)
    # FINAL CAMBIOS

    # logging.info('[CLASSIFY] Preprocesando imagen')
    # processed_img = preprocess(photo)

    # model_payload = {"input_data": [ {"values": processed_img.tolist() } ]}

    # # iam_token = get_iam_token()
    # header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + os.environ.get('IAM_TOKEN')}

    # logging.info('[CLASSIFY] Clasificando imagen')
    
    # init_classification = time.time()
    # try:
    #     response_scoring = requests.post(os.environ.get("WATSONURL"), json=model_payload, headers=header)
    # except Exception as e:
    #     logging.error('[CLASSIFY] Error: Error de Watson %s', e)
    #     raise WatsonError('Error de Watson')
    # fin_classification = time.time()

    # logging.info('[CLASSIFY] Transformando respuesta')
    # scoring = response_scoring.json()["predictions"][0]["values"][0]
    # parsed_scores = parse_predictions(scoring)

    # logging.info('[CLASSIFY] Operación realizada con éxito')
    # fin_peticion = time.time()

    # classification_time = "{:.3f}".format(float(fin_classification - init_classification))
    # petition_time = "{:.3f}".format(float(fin_peticion - init_peticion))

    # logging.info('[CLASSIFY] Para la imagen "%s" se obtuvieron estos resultados: "%s". Tiempo de clasificación "%s" seg, tiempo total de petición: "%s" seg', photo.filename, parsed_scores, classification_time, petition_time)

    # return parsed_scores