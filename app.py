from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import time
import imageScaler as scaler
import os

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///images.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.config["UPLOAD_FOLDER"] = "static/uploads"
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/add")
def add():  
    mezi = request.args.get("c")
    return jsonify({"result": mezi})

@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    print("[-----] UPLOAD STARTED [-----]")
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["image"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    desc = request.form.get("title")
    
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    print(f"Saving file to: {file_path}")
    
    file.save(file_path)
    time.sleep(0.1)

    # Here, we pass only the filename (not the full path) to scaler.process_image
    processed_filename = scaler.process_image(file.filename)  # Correctly passing the filename

    os.remove(file_path)

    new_image = ImageData(image_path=f"/static/uploads/{processed_filename}", description=desc)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({"message": "File uploaded and processed successfully", "file_url": f"/static/uploads/{processed_filename}", "description": desc}), 200

@app.route("/random-image", methods=["GET"])
def get_random_image():
    print("[-----] USER REQUESTED A POST BY SERVER [-----]")    
    # Get a random image from the database
    random_image = ImageData.query.order_by(db.func.random()).first()

    if random_image:
        return jsonify({
            "file_url": random_image.image_path,
            "description": random_image.description
        }), 200
    else:
        return jsonify({"error": "No images found."}), 404

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)