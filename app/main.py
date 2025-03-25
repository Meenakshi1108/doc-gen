import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from app.api.document_api import document_ns

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Configure API documentation
    api = Api(
        app, 
        version='1.0', 
        title='Document Generation API',
        description='API for generating PDF and DOCX documents from HTML',
        doc='/api/docs',
        validate=True
    )
    
    # Add namespaces
    api.add_namespace(document_ns)
    
    @app.route('/', methods=['GET'])
    def health_check():
        return {"status": "healthy", "service": "Document Generation Service"}
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)