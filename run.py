# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask
from app.routes.gcs_upload import gcs_upload  # ✅ this is your blueprint

app = Flask(__name__)
app.register_blueprint(gcs_upload)  # ✅ register the upload route here

@app.route("/")
def home():
    return "Flask app is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

