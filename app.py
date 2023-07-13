"""
Test each algorithm with image and optional question, and write results to a spreadsheet
"""

import os
import sys

from dotenv import load_dotenv

from helper import (data_to_scenex, process_csv, process_dir,
                    process_local_image, process_url, write_csv)

algos = [
        # 'Aqua',
        # 'Bolt',
        # 'Comet',
        # 'Dune',
        # 'Ember',
        # 'Flash',
        'Glide'
         ]

load_dotenv()
SCENEX_SECRET = os.getenv('SCENEX-SECRET')
IMG_PATH = sys.argv[1]

if len(sys.argv) > 2:
    question = sys.argv[2]
else:
    question = ''

# support single files
if os.path.isfile(IMG_PATH):
    ext = os.path.splitext(IMG_PATH)[-1]
    if ext == '.csv':
        images = process_csv(IMG_PATH)
        output_filename = IMG_PATH
    else:
        images = process_local_image(IMG_PATH, question)
        output_filename = f"{os.path.splitext(os.path.basename(IMG_PATH))[0]}.csv"

# support dirs of images
elif os.path.isdir(IMG_PATH):
    images = process_dir(IMG_PATH, question)
    output_filename = f"{IMG_PATH}.csv"

# support image URLs
else:
    images = process_url(IMG_PATH, question)
    output_filename = f"{IMG_PATH.split('/')[-1].split('.')[0]}.csv"

results = []
for i, image in enumerate(images, start=1):
    print(f"Processing image {i}/{len(images)}")
    for algo in algos:
        print(f"  - Getting result for {algo}")

        response = data_to_scenex([image])

        del image['image']  # otherwise csv gets bloated with base64
        image['algorithm'] = algo

        # sometimes this bugs out so skip the image
        if 'image' in response['result'][0].keys():
            image['scenex_url'] = response['result'][0]['image'],
        else:
            print("Problem processing image")
            continue

        if 'question' in image.keys():
            image['answer'] = response['result'][0]['answer']
        else:
            image['text'] = response['result'][0]['text'],

        results.append(image)

write_csv(results, output_filename)
