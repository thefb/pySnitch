# Import necessary modules
import os
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from werkzeug.utils import secure_filename

# Config
ALLOWED_EXTENSIONS = set(['xlsx'])
UPLOAD_FOLDER = './uploads'

# Create Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
swagger = Swagger(app)

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Create route to handle file upload
@app.route('/upload', methods=['POST'])
@swag_from('swagger_config.yml')
def upload_files():
        if 'file1' not in request.files or 'file2' not in request.files or 'file3' not in request.files:
                return jsonify({'error': 'One or more files missing!'}), 400

        file1 = request.files['file1']
        file2 = request.files['file2']
        file3 = request.files['file3']

        if file1.filename == '' or file2.filename == '' or file3.filename == '':
               return jsonify({'error': 'No selected files!'}), 400
        
        if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename) and file3 and allowed_file(file3.filename):
            # Get the uploaded files
            filename1 = secure_filename(file1.filename)
            filename2 = secure_filename(file2.filename)
            filename3 = secure_filename(file3.filename)

            # Save the files to disk
            file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))
            file3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))

            # Return a success message
            return jsonify({'message': 'Files uploaded successfully!'}), 200 

        return jsonify({'error': 'Invalid file type!'}), 400

if __name__ == '__main__':
       app.run(debug=True)