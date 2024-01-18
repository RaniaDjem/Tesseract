from flask import Flask, jsonify
import cv2
import numpy as np
import cv2
import pytesseract
import matplotlib.pyplot as plt
import os
from PIL import Image
import math
from typing import Tuple, Union
from deskew import determine_skew
import itertools
import re
from flask import Flask, request, jsonify
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

# FONCTION QUI RETOURNE L'IMAGE EN GRAYSCALE
def conv_gray(img):
    if len(img.shape) == 3:
        if img.dtype == np.uint8:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    return gray

def resize_image(image, scale_factor=1.2):
    # Obtient les dimensions de l'image d'origine
    height, width = image.shape[:2]

    # Calcule les nouvelles dimensions en fonction du facteur d'échelle
    new_height = int(height * scale_factor)
    new_width = int(width * scale_factor)

    # Redimensionne l'image en utilisant la nouvelle taille
    resized_image = cv2.resize(image, (new_width, new_height))

    return resized_image

# ROTATION/DESKEWING
# https://pypi.org/project/deskew/
def rotate(
    image: np.ndarray, angle: float, background: Union[int, Tuple[int, int, int]]
) -> np.ndarray:
    old_width, old_height = image.shape[:2]
    angle_radian = math.radians(angle)
    width = abs(np.sin(angle_radian) * old_height) + abs(
        np.cos(angle_radian) * old_width
    )
    height = abs(np.sin(angle_radian) * old_width) + abs(
        np.cos(angle_radian) * old_height
    )

    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    rot_mat[1, 2] += (width - old_width) / 2
    rot_mat[0, 2] += (height - old_height) / 2
    return cv2.warpAffine(
        image, rot_mat, (int(round(height)), int(round(width))), borderValue=background
    )


def deskewing(image):
    # niv de gris
    if len(image.shape) == 3:  # Vérification si l'image n'est pas déjà en niveaux de gris
        gray = gray = conv_gray(image)
    else:
        gray = image
    # gray = conv_gray(image)
    angle = determine_skew(gray)
    rotated = rotate(image, angle, (255, 255, 255))
    return rotated


def preprocess_image(image):
    # Conversion en niveaux de gris si l'image est en couleur
    if len(image.shape) == 3:
        gray_image = conv_gray(image)
    else:
        gray_image = image

    # Redimensionnement de l'image avec un facteur d'échelle
    scaled_image = resize_image(gray_image, scale_factor=1.2)

    # Correction de l'inclinaison
    deskewed_image = deskewing(scaled_image)
    

    return deskewed_image



# Endpoint récupérer et prétraiter l'image
@app.route('/process_image', methods=['GET'])
def process_image():
    # path vers l'img
    image_path = '-images.openfoodfacts.org-images-products-00000178-ingredients_en.17.400.jpg'

    image = cv2.imread(image_path)

    if image is None:   
        return jsonify({'result': 'error', 'message': 'Impossible de charger l\'image'})

    # prétraitement
    preprocessed_image = preprocess_image(image)

    # Retournez le résultat en tant que JSON (juste à titre d'exemple)
    return jsonify({'result': 'success', 'preprocessed_image': preprocessed_image.tolist()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
