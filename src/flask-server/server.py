from flask import Flask, request, send_file
import backend
from damage_detection.detect_crack import detect_damage
import json

app = Flask(__name__)

data = {}

@app.route("/members", methods=['POST', 'GET'])
def members():
    global data
    if request.method == 'POST':
        images = [None for _ in range(5)]
        for i in range(5):
            images[i] = request.files.get(f'file{i}')
        print(images)
        post = request.form.get('data')
        masks, damages = detect_damage(images)
        res = backend.analyze_property(post)
        return {'masks': masks,
                'damages': damages,
                'result': res}
    
@app.route("/gen_pdf", methods=['GET'])
def gen_pdf():
    try:
        return send_file('Real_Estate_Report.pdf')
    except Exception as e:
        print('errored out')
        return str(e)

if __name__ == "__main__":
    app.run()