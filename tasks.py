from celery import Celery
from app import create_app, db
from models import Request, Product

celery = Celery(__name__, broker='redis://localhost:6379/0')
celery.conf.update(result_backend='redis://localhost:6379/0')

@celery.task
def process_images(request_id):
    with create_app().app_context():
        req = Request.query.get(request_id)
        req.status = 'Processing'
        db.session.commit()

        for product in req.products:
            input_urls = product.input_image_urls.split(',')
            output_urls = []
            for url in input_urls:
                # Compress image logic
                output_url = compress_image(url)
                output_urls.append(output_url)
            product.output_image_urls = ','.join(output_urls)
            db.session.commit()

        req.status = 'Completed'
        db.session.commit()

def compress_image(url):
    # Mock compressing image
    return url.replace('public', 'compressed')
