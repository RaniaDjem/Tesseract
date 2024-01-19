from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/convert_to_text', methods=['POST'])
def convert_image_to_text():
    try:
        uploaded_file = request.files['file']
        # Vérifiez si le nom de fichier est vide
        if uploaded_file.filename == '':
            return "Aucun fichier sélectionné."
        
        # Vérifiez si le dossier shared_data existe, sinon le crée
        if not os.path.exists('/shared_data'):
            os.makedirs('/shared_data')

        uploaded_file.save('/shared_data/image1.jpg')
        return "Traitement réussi"
    
    except Exception as e:
        return f"Erreur : {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)