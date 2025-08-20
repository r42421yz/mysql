from flask import Flask, request, jsonify
from model import neuralNetwork
from flask_cors import CORS
from PIL import Image
import numpy as np
import io

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

n = neuralNetwork(784, 200, 10, 0.3)
n.load("model_weights.npz")

def preprocess(file_bytes):
    img = Image.open(io.BytesIO(file_bytes)).convert("L")
    img = img.resize((28,28))
    arr = np.array(img, dtype = np.float32)

    if arr.mean() > 127:
        arr = 255 - arr

    arr = (arr / 255.0 * 0.99) + 0.01
    return arr.flatten()

@app.route("/predict", methods = ["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error":"没有上传文件"}), 400
    
    file = request.files["file"]
    img_bytes = file.read()

    x = preprocess(img_bytes)
    outputs = n.query(x)
    label = int(np.argmax(outputs))

    return jsonify({
        "label":label,
        "probs":[float(p) for p in outputs]
    })

if __name__ == "__main__":
    app.run(debug=True)
