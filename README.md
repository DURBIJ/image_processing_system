# Image Processing System

This project is an image processing system that accepts a CSV file containing image URLs, compresses the images, stores the processed images, and provides APIs to track the status of the processing. The system is built using Flask, Celery, and MySQL.

## Features

- **Asynchronous Image Processing**: Compresses images by 50% of their original quality.
- **API Endpoints**: 
  - **Upload API**: Upload a CSV file containing product names and image URLs.
  - **Status API**: Check the status of the image processing request.
- **Webhook Integration**: Optional webhook to notify when processing is complete.
- **MySQL Database**: Tracks requests, products, and their associated images.

## Project Structure


image_processing_system/
│
├── app.py                  # Main Flask application
├── tasks.py                # Celery tasks for asynchronous processing
├── models.py               # Database models
├── config.py               # Configuration file
└── requirements.txt        # Project dependencies


**Requirements**

    - Python 3.8+
    - MySQL Server
    - Redis (for Celery task queue)


1. **Install Dependencies**
    - pip install -r requirements.txt

2. **Configure MySQL Database**
    - Create a MySQL database:
        - CREATE DATABASE image_processing_db;
    - Update config.py with your MySQL credentials:
        - SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/image_processing_db'

3. **Set Up Database Migrations**
    - flask db init
    - flask db migrate -m "Initial migration."
    - flask db upgrade

4. **Start the Celery Worker**
    - Ensure Redis is running, then start the Celery worker:
        - celery -A tasks.celery worker --loglevel=info

5. **Run the Flask Application**
    - flask run



# Usage
## Upload API

    - Endpoint: POST /upload

    - Description: Accepts a CSV file and returns a unique request ID.

    - Request:
        - Form-data with the CSV file.

    - Response:
        - 200 OK: { "request_id": "your-request-id" }

## Status API

    - Endpoint: GET /status/<request_id>
    - Description: Check the status of the image processing request.
    - Response:
        - 200 OK: { "status": "Pending/Processing/Completed" }
        - 404 Not Found: { "error": "Invalid request ID" }

# CSV Format
    ## Input CSV Format:
        - S. No., Product Name, Input Image Urls

    ## Output CSV Format (after processing):
        - S. No., Product Name, Input Image Urls, Output Image Urls