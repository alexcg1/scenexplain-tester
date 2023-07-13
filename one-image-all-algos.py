"""
Test each algorithm with a single image and optional question, and write results to a spreadsheet
"""

import base64
import csv
import glob
import http.client
import json
import os
import sys
from datetime import datetime
from pprint import pprint

from dotenv import load_dotenv

# from jinaai import JinaAI

load_dotenv()
SCENEX_SECRET = os.getenv('SCENEX-SECRET')

# Create directory structure
os.makedirs('output/json', exist_ok=True)
os.makedirs('output/csv', exist_ok=True)

IMG_URL = sys.argv[1]
timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
os.makedirs(f"output/csv/{timestamp}", exist_ok=True)


if len(sys.argv) > 2:
    QUESTION = sys.argv[2]

algos = ['Aqua', 'Bolt', 'Comet', 'Dune', 'Ember', 'Flash', 'Glide']


def image_to_data_uri(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded_image}"


# support single files
if os.path.isfile(IMG_URL):
    images = [image_to_data_uri(IMG_URL)]
    csv_filename = f"output/csv/{timestamp}/{os.path.basename(IMG_URL)}.csv"

# support dirs of images
elif os.path.isdir(IMG_URL):
    png_files = glob.glob(f'{IMG_URL}/*.png')
    jpg_files = glob.glob(f'{IMG_URL}/*.jpg')
    jpeg_files = glob.glob(f'{IMG_URL}/*.jpeg')
    image_files = png_files + jpg_files + jpeg_files

    images = []
    for image in image_files:
        image = image_to_data_uri(image)
        images.append(image)

    csv_filename = f"output/csv/{timestamp}/{IMG_URL}.csv"

    print(images)

# support image URLs
else:
    images = [IMG_URL]
    csv_filename = f"output/csv/{timestamp}/{IMG_URL.split('/')[-1].split('.')[0]}.csv"


headers = {
    "x-api-key": f"token {SCENEX_SECRET}",
    "content-type": "application/json",
}

results = []
connection = http.client.HTTPSConnection("api.scenex.jina.ai")
for image in images:
    print(f"Processing {image}")
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

        connection.request("POST", "/v1/describe", json.dumps(data), headers)
        response = connection.getresponse()

        response_data = response.read().decode("utf-8")
        response_json = json.loads(response_data)
        # pprint(response_json['result'])
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

with open(csv_filename, 'w') as file:
    field_names = list(results[0].keys())

    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()

    for result in results:
        writer.writerow(result)

    print(f'{csv_filename} written')
