from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import cv2
from werkzeug.utils import secure_filename
from pose_estimation import process_video

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow React frontend to communicate with the backend

# Directories for uploads and processed videos
UPLOAD_FOLDER = "./uploads"
PROCESSED_FOLDER = "./processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route("/ok", methods=["GET"])
def test_api(): 
    return "API WORKING!"

# Route for uploading videos
@app.route("/upload", methods=["POST"])
def upload_video():
    # Check if a file is uploaded
    if "video" not in request.files:
        return jsonify({"error": "No video file uploaded"}), 400

    video_file = request.files["video"]
    if video_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded file
    filename = secure_filename(video_file.filename)
    upload_path = os.path.join(app.config['PROCCESSED_FOLDER'], filename)
    video_file.save(upload_path)

    try:
        processed_path = process_video(upload_path)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"downloadUrl": f"/download/{output_filename}"})
    # Generate download URL
    # download_url = f"http://localhost:5000/download/{os.path.basename(processed_path)}"
    # return jsonify({"downloadUrl": download_url})

# Route for downloading processed videos
@app.route("/download/<filename>", methods=["GET"])
def download_video(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

# Function to process video
# def process_video(input_path):
#     output_filename = f"processed_{os.path.basename(input_path)}"
#     output_path = os.path.join(PROCESSED_FOLDER, output_filename)

#     # Open the video file
#     cap = cv2.VideoCapture(input_path)
#     fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     # Create VideoWriter object
#     out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Apply gesture detection or any processing here
#         # Example: Drawing a rectangle on each frame
#         cv2.rectangle(frame, (50, 50), (200, 200), (0, 255, 0), 3)

#         # Write the processed frame
#         out.write(frame)

#     cap.release()
#     out.release()

#     return output_path

if __name__ == "__main__":
    app.run(debug=True)
