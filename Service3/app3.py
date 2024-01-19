import numpy as np
import pytesseract
from PIL import Image
import re
from flask import Flask, request, jsonify
from flask import Flask, request, render_template, send_file




# Retourne l'OCR
def ocr(img):
    # Convert image to the expected data type
    img = img.astype(np.uint8)

    processed_text = pytesseract.image_to_string(img)
    # processed_text = processed_text.replace('\n', ' ')
    # print(processed_text)
    return processed_text



def preprocess_text(text):
    """
    Applique un prétraitement pour supprimer les lignes vides et les lignes non pertinentes.

    """
    # Supprimer les lignes vides
    non_empty_lines = [line.strip() for line in text.split('\n') if line.strip() != '']

    # Supprimer les lignes contenant une seule lettre ou des suites de lettres séparées par des espaces
    filtered_lines = []
    for line in non_empty_lines:
        if len(line) <= 1 or re.match(r'^[a-zA-Z]+( [a-zA-Z]+)*$', line):
            continue
        filtered_lines.append(line)

    return '\n'.join(filtered_lines)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert_to_text', methods=['POST'])
def convert_image_to_text():
    try:
        image_path = '/shared_data/image2.jpg'
        #uploaded_file = request.files['file']
        #if uploaded_file.filename != '':
        if image_path != '':

            #image = Image.open(uploaded_file)
            #image = np.array(Image.open(uploaded_file))
            image = np.array(Image.open(image_path))

            #OCR without any preprocessing
            ocr_res = ocr(image)

            # Prétraitement du texte OCR
            preprocessed_text = preprocess_text(ocr_res)

            meilleur_texte = preprocessed_text

            return meilleur_texte

        else:
            return "Aucun fichier téléchargé."
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run()

