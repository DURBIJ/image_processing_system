from flask import Flask, request, jsonify, send_from_directory
from models import db, Request, Product
from tasks import process_images
from uuid import uuid4
import os
import csv

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    @app.route('/upload', methods=['POST'])
    def upload_csv():
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file provided"}), 400

        # Save file
        request_id = str(uuid4())
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{request_id}.csv")
        file.save(filepath)

        # Parse CSV and store records
        with open(filepath, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip header
            req = Request(id=request_id)
            db.session.add(req)
            for row in csv_reader:
                product = Product(
                    id=str(uuid4()),
                    serial_number=row[0],
                    product_name=row[1],
                    input_image_urls=row[2],
                    request=req
                )
                db.session.add(product)
            db.session.commit()

        # Start processing
        process_images.delay(request_id)
        return jsonify({"request_id": request_id})

    @app.route('/status/<request_id>', methods=['GET'])
    def check_status(request_id):
        req = Request.query.get(request_id)
        if not req:
            return jsonify({"error": "Invalid request ID"}), 404
        return jsonify({"status": req.status})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
