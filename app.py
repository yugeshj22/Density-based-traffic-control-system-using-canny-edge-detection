from flask import Flask, render_template, request
import cv2
import numpy as np
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    img = cv2.imread(filepath, 0)
    blurred = cv2.GaussianBlur(img, (5, 5), 1.4)
    edges = cv2.Canny(blurred, 50, 150)
    traffic_density = np.count_nonzero(edges)

    if traffic_density > 10000:
        green_time = 50
    elif traffic_density < 5000:
        green_time = 20
    else:
        green_time = 30

    return render_template('result.html', density=traffic_density, time=green_time, image=file.filename)

if __name__ == '__main__':
    app.run(debug=True)
