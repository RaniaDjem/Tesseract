from flask import Flask, request

app = Flask(__name__)

@app.route('/convert_to_text', methods=['POST'])
def convert_image_to_text():
    try:
        uploaded_file = request.files['file']
        # Ajoutez ici la logique pour traiter le fichier uploadé
        # (conversion d'image en texte, etc.)
        uploaded_file.save('/shared_data/image1.jpg')
        return "Traitement réussi"
    except Exception as e:
        return f"Erreur : {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)