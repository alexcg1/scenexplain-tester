"""
Test each algorithm with a single image and optional question, and write results to a spreadsheet
"""

import base64
import csv
import http.client
import json
import os
import sys
from os.path import isfile
from pprint import pprint

from dotenv import load_dotenv

# from jinaai import JinaAI

load_dotenv()
SCENEX_SECRET = os.getenv('SCENEX-SECRET')

# Create directory structure
os.makedirs('output/json', exist_ok=True)

IMG_URL = sys.argv[1]
CSV_FILENAME = IMG_URL.split('/')[-1].split('.')[0] + '.csv'

if len(sys.argv) > 2:
    QUESTION = sys.argv[2]

algos = ['Aqua', 'Bolt', 'Comet', 'Dune', 'Ember', 'Flash', 'Glide']

def image_to_data_uri(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded_image}"

if os.path.isfile(IMG_URL):
    image = image_to_data_uri(IMG_URL)
else:
    image = IMG_URL

headers = {
    "x-api-key": f"token {SCENEX_SECRET}",
    "content-type": "application/json",
}

results = []
for algo in algos:
    print(f"Getting result for {algo}")
    data = {
        "data": [
            {"image": image, "features": [], "algorithm": algo},
        ]
    }

    if 'QUESTION' in locals():
        data['data'][0]['features'].append('question_answer')
        data['data'][0]['question'] = QUESTION
    else:
        QUESTION = ''

    connection = http.client.HTTPSConnection("api.scenex.jina.ai")
    connection.request("POST", "/v1/describe", json.dumps(data), headers)
    response = connection.getresponse()

    response_data = response.read().decode("utf-8")
    response_json = json.loads(response_data)
    result = {
            'image_url': response_json['result'][0]['image'],
            'algorithm': algo,
            }

    if QUESTION:
        result['question'] = QUESTION
        result['output'] = response_json['result'][0]['answer']
    else:
        result['output'] = response_json['result'][0]['text'],

    results.append(result)

connection.close()

with open(CSV_FILENAME, 'w') as file:
    field_names = list(results[0].keys())

    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()

    for result in results:
        writer.writerow(result)

    print(f'{CSV_FILENAME} written')
