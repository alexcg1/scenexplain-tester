import base64
import csv
import glob
import http.client
import json
import os
from datetime import datetime
from pprint import pprint

from dotenv import load_dotenv

load_dotenv()
SCENEX_SECRET = os.getenv('SCENEX-SECRET')

headers = {
    "x-api-key": f"token {SCENEX_SECRET}",
    "content-type": "application/json",

}


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def image_to_data_uri(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded_image}"


def process_url(url, question=''):
    image_dict = {'image': url, 'original_url': url}

    if question:
        image_dict['question'] = question
        image_dict['features'] = ['question_answer']

    return [image_dict]


def process_local_image(file_path, question=''):
    image_dict = {'image': image_to_data_uri(file_path)}

    if question:
        image_dict['question'] = question
        image_dict['features'] = ['question_answer']
        image_dict['original_url'] = file_path

    return [image_dict]


def process_dir(file_path, question=''):
    png_files = glob.glob(f'{file_path}/*.png')
    jpg_files = glob.glob(f'{file_path}/*.jpg')
    jpeg_files = glob.glob(f'{file_path}/*.jpeg')
    image_files = png_files + jpg_files + jpeg_files

    output_data = []

    for image in image_files:
        image_dict = process_local_image(image, question)
        output_data.extend(image_dict)

    return output_data


def process_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)

        data = list(reader)
        output_data = []

        for row in data:
            # output_row = {
                    # 'image': row['image']
                    # }

            if 'question' in row.keys():
                # output_row['question'] = row['question']
                row['features'] = ['question_answer']

            # output_data.append(output_row)

        return data


def data_to_scenex(data, algos=[]):
    input_data = {'data': data}
    connection = http.client.HTTPSConnection("api.scenex.jina.ai")
    connection.request("POST", "/v1/describe", json.dumps(input_data), headers)
    response = connection.getresponse()
    assert response.status == 200

    response_data = response.read().decode("utf-8")
    response_json = json.loads(response_data)
    connection.close()

    return response_json


def write_csv(dictionary, filename):
    csv_dir = f"output/csv/{get_timestamp()}"
    os.makedirs(csv_dir, exist_ok=True)

    with open(f'{csv_dir}/{filename}', 'w') as file:
        field_names = list(dictionary[0].keys())

        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()

        for record in dictionary:
            writer.writerow(record)

        print(f'{filename} written')
