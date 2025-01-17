from flask import Flask, render_template, request
import json
import spacy
from spacy import displacy
from nerclient import NamedEntityClient
import os
app = Flask(__name__, template_folder=os.path.abspath('templates')) 
print(f"Template folder: {app.template_folder}")  # Print the template folder path
ner = spacy.load("en_core_web_sm")
ner = NamedEntityClient(ner, displacy)

@app.route('/')
def index():
       print("Rendering index.html")
       return render_template('index.html')
@app.route('/ner', methods=['POST'])
def get_named_ents():
    data = request.get_json()
    result = ner.get_ents(data['sentence'])
    response = { "entities": result.get('ents'), "html": result.get('html') }
    return json.dumps(response)


if __name__ == "__main__":
       app.run(debug=True, host="0.0.0.0", port=5000)
   