from flask import Flask
from app.routes.gcs_upload import upload_file

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask app is running!", 200

# Register the upload route
app.add_url_rule('/upload', view_func=upload_file, methods=['POST'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


