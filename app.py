from flask import Flask, jsonify, request

from flask_cors import CORS
import numpy as np
import cv2
from ultralytics import YOLO
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.json.ensure_ascii = False

# Cho phép tất cả các nguồn
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# ma = Marshmallow(app)


@app.route('/', methods = ['GET'])
def get_articles():
    return jsonify({"Hello":"World"})

@app.route('/test', methods=['GET'])
def test_connection():
    return jsonify({"message": "Connection successful!"})


@app.route('/detect', methods=['POST'])
def detect_objects():
    try:
        # Load model
        model = YOLO("best.pt")

        # Print keys and information about received files for debugging
        print(request.files.keys())
        print(request.files['image'])

        # Get the image file from the request
        file = request.files['image']

        # Convert the file to a NumPy array
        file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)

        # Decode the image
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Perform object detection
        results = model.predict(image)

        # Process the results and create a list of object counts
        object_counts = []
        for result in results:
            names = result.names
            counts = Counter(result.boxes.cls.tolist())

            for class_id, count in counts.items():
                object_counts.append({
                    "class": names[class_id],
                    "count": count
                })

        # Optional: Save the annotated image
        im_array = results[0].plot()  # Sử dụng results[0] thay vì result
        im = Image.fromarray(im_array[..., ::-1]) 
        buffered = io.BytesIO()
        im.save(buffered, format="PNG")  # Lưu hình ảnh vào buffer dưới định dạng PNG
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')  # Chuyển đổi thành Base64
        
        # im.save('annotated_image.jpg')

        # Define the path or URL to the saved image
        # saved_image_path = 'received_image.jpg'  # Update this with the actual path or URL

        # Return a JSON response
        response_data = {
            'object_counts': object_counts,
            'image': img_str
            # 'saved_image_path': saved_image_path
        }
        return jsonify(response_data), 200

    except Exception as e:
        # Handle any exceptions that might occur during the processing
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred during processing.'}), 500


if __name__ == "__main__":
    app.run(debug=True)