# SceneXplain testing scripts

These script use the SceneXplain API to compare algorithms

## One image all algos

Take image(s) and:

- Get descriptions using all algorithms (you can edit which algos in the script)
- Optionally ask a question
- Write output to a CSV file

### General syntax

```sh
python app.py <FILE_LOCATION> <OPTIONAL_QUESTION>
```

### Local file

```sh
python app.py foo.jpeg # read local file, write to foo.csv
```

### Local file with question

```sh
python app.py foo.jpeg "what color is the jacket?" # ask question about local file, write to foo.csv
```

### Local directory

You can add a question at the end that applies to all images in the directory

```sh
python app.py input_images # read from dir, write to input_images.csv
```

### URL

You can add an optional question at the end

```sh
python app.py https://bar.com/foo.jpg # read url, write to foo.csv
```

### CSV

Use `image` and optional `question` to specify each image/question

```sh
python app.py foo.csv # read url, write to foo.csv
```

### Example output

```csv
image_url,algorithm,question,output
https://storage.googleapis.com/causal-diffusion.appspot.com/imagePrompts%2F95d6fd07-ff76-4f78-acee-bf91821bfc0e%2Foriginal.png,Aqua,what color is the jacket?,The jacket worn by the central figure in the photograph is a vibrant green puffer jacket.
https://storage.googleapis.com/causal-diffusion.appspot.com/imagePrompts%2Faf0cd36d-3c0b-4c69-b5b2-22dc148fcac2%2Foriginal.png,Bolt,what color is the jacket?,The color of the jacket is green.
https://storage.googleapis.com/causal-diffusion.appspot.com/imagePrompts%2F5b9f8960-5e75-4720-b5ff-3b92a7e266cb%2Foriginal.png,Comet,what color is the jacket?,The color of the jacket worn by the young woman in the picture is green.
https://storage.googleapis.com/causal-diffusion.appspot.com/imagePrompts%2F427f1f2f-9fc0-4f30-ba53-a679db11cfcb%2Foriginal.png,Dune,what color is the jacket?,The color of the jacket is dark green.
https://storage.googleapis.com/causal-diffusion.appspot.com/imagePrompts%2F29622119-ee82-4887-b6e8-e7c450a56db9%2Foriginal.png,Ember,what color is the jacket?,The jacket worn by the second woman on the far right of the image is green.
https://storage.googleapis.com/causal-diffusion.appspot.com/imagePrompts%2Fc79605c3-a852-4be1-af20-0968f9468b53%2Foriginal.png,Flash,what color is the jacket?,The jacket is green.
https://storage.googleapis.com/causal-diffusion.appspot.com/imagePrompts%2F14c230dc-fbf1-4548-8854-0a06aa5817be%2Foriginal.png,Glide,what color is the jacket?,"The color of the jacket seen in the image is green, worn by one of the women standing on the steps in front of the house with the red door and metal railing."
```
