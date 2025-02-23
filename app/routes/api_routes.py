import os
from flask import Blueprint, request, jsonify
from app.services.document_service import load_documents_aws
from app.services.query_service import get_qa_service
from werkzeug.utils import secure_filename
import boto3
import os
from botocore.exceptions import ClientError
from werkzeug.exceptions import BadRequest

api_bp = Blueprint('api', __name__)

os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")

S3_BUCKET = 'ringrag'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'json', 'txt'}

# Initialize S3 client
s3_client = boto3.client('s3')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def file_exists(bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if file_exists(S3_BUCKET, filename):
            action = 'replaced'
        else:
            action = 'uploaded'
        try:
            s3_client.upload_fileobj(
                file,
                S3_BUCKET,
                filename,
                ExtraArgs={'ContentType': file.content_type}
            )
            load_documents_aws()
            return jsonify({'message': f'File successfully {action} in S3'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Allowed file types are pdf, docx, json, txt'}), 400


@api_bp.route('/ask', methods=['POST'])
def ask_question():
    try:
        # Ensure the request contains JSON data
        if not request.is_json:
            raise BadRequest(description="Request must be in JSON format.")

        data = request.get_json()

        # Validate presence of 'question' and 'title' in the JSON data
        question = data.get('question')
        title = data.get('title')

        # Process the question and title
        response = get_qa_service(question, title=title)
        return jsonify(response), 200

    except BadRequest as e:
        # Handle client-side errors (400 series)
        return jsonify({"error": e.description}), e.code

    except Exception as e:
        # Handle server-side errors (500 series)
        return jsonify({"error": "An unexpected error occurred."}), 500


