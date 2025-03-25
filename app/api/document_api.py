import tempfile
import os
import shutil
from flask import request, send_file, jsonify
from flask_restx import Namespace, Resource, fields
from app.services.document_service import generate_document
from app.validators.input_validator import validate_document_request
from app.utils.file_cleanup import file_cleanup

# Create namespace
document_ns = Namespace('api/v1', description='Document generation operations')

# Define request models for documentation
doc_model = document_ns.model('Document', {
    'content_html': fields.String(required=True, description='HTML content for the body'),
    'header_html': fields.String(required=False, description='HTML content for the header'),
    'footer_html': fields.String(required=False, description='HTML content for the footer'),
    'document_type': fields.String(required=True, description='Document type (pdf or docx)', enum=['pdf', 'docx']),
    'watermark': fields.String(required=False, description='HTML content for the watermark')
})

@document_ns.route('/generate')
class DocumentGenerator(Resource):
    @document_ns.expect(doc_model)
    @document_ns.response(200, 'Success - Returns document file')
    @document_ns.response(400, 'Validation Error')
    @document_ns.response(500, 'Internal Server Error')
    def post(self):
        """Generate a document (PDF or DOCX) from HTML content"""
        tmp_path = None
        response_file = None
        
        try:
            # Get request data
            data = request.json
            
            # Validate input
            validation_result = validate_document_request(data)
            if validation_result is not True:
                return {"error": validation_result}, 400
                
            # Extract parameters
            content_html = data.get('content_html', '')
            header_html = data.get('header_html', '')
            footer_html = data.get('footer_html', '')
            document_type = data.get('document_type', '').lower()
            watermark = data.get('watermark', None)
            
            # Create a temporary file for the output
            fd, tmp_path = tempfile.mkstemp(suffix=f'.{document_type}')
            os.close(fd)
            
            # Generate the document
            output_path = generate_document(
                content_html=content_html,
                header_html=header_html,
                footer_html=footer_html,
                document_type=document_type,
                output_path=tmp_path,
                watermark=watermark
            )
            
            # Create a copy of the file that Flask can safely send
            response_file = os.path.join(tempfile.gettempdir(), f"response_{os.path.basename(tmp_path)}")
            shutil.copy2(tmp_path, response_file)
            
            # Mark original file for cleanup
            file_cleanup.mark_for_cleanup(tmp_path)
            
            # Mark response file for delayed cleanup
            file_cleanup.mark_for_cleanup(response_file)
            
            # Return the copied file as a download attachment
            return send_file(
                response_file, 
                mimetype=f'application/{"pdf" if document_type == "pdf" else "vnd.openxmlformats-officedocument.wordprocessingml.document"}', 
                as_attachment=True,
                download_name=f'document.{document_type}',
                max_age=0
            )
                
        except Exception as e:
            # Clean up files in case of error
            for path in [tmp_path, response_file]:
                if path and os.path.exists(path):
                    try:
                        os.unlink(path)
                    except:
                        pass
            return {"error": str(e)}, 500