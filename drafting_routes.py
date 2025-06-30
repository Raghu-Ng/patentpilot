from flask import Blueprint, request, jsonify, send_file
from models import Project, Draft, Drawing
from ai_service import PatentAIService
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from mongoengine.errors import DoesNotExist, ValidationError
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")

# Create blueprint for drafting routes
drafting_bp = Blueprint('drafting', __name__, url_prefix='/drafts')

# Initialize AI service
ai_service = PatentAIService()

# Configure upload settings
UPLOAD_FOLDER = 'uploads/drawings'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'pdf'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@drafting_bp.route('/start', methods=['POST'])
def start_draft():
    """Initialize a new patent draft"""
    try:
        data = request.get_json()
        
        # Create new project
        project = Project(
            user_id=data.get('user_id', 'default_user'),
            title=data.get('project_title', 'New Patent Project'),
            description=data.get('project_description', '')
        )
        project.save()
        
        # Create new draft
        draft = Draft(
            project_id=str(project.id),
            title=data.get('title', ''),
            field_of_invention=data.get('field_of_invention', ''),
            brief_summary=data.get('brief_summary', ''),
            key_components=data.get('key_components', ''),
            problem_solved=data.get('problem_solved', ''),
            current_step=1
        )
        draft.save()
        
        return jsonify({
            'success': True,
            'data': {
                'draft_id': str(draft.id),
                'project_id': str(project.id)
            },
            'message': 'Draft started successfully'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@drafting_bp.route('/<draft_id>', methods=['GET'])
def get_draft(draft_id):
    """Get draft details"""
    try:
        draft = Draft.objects.get(id=draft_id)
        return jsonify({
            'success': True,
            'data': draft.to_dict()
        }), 200
        
    except DoesNotExist:
        return jsonify({
            'success': False,
            'error': 'Draft not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@drafting_bp.route('/<draft_id>', methods=['PATCH'])
def update_draft(draft_id):
    """Update draft sections"""
    try:
        draft = Draft.objects.get(id=draft_id)
        data = request.get_json()
        
        # Update basic information
        if 'title' in data:
            draft.title = data['title']
        if 'field_of_invention' in data:
            draft.field_of_invention = data['field_of_invention']
        if 'brief_summary' in data:
            draft.brief_summary = data['brief_summary']
        if 'key_components' in data:
            draft.key_components = data['key_components']
        if 'problem_solved' in data:
            draft.problem_solved = data['problem_solved']
        
        # Update sections
        if 'background' in data:
            draft.background = data['background']
        if 'summary' in data:
            draft.summary = data['summary']
        if 'detailed_description' in data:
            draft.detailed_description = data['detailed_description']
        if 'claims' in data:
            draft.claims = data['claims']
        if 'abstract' in data:
            draft.abstract = data['abstract']
        
        # Update current step
        if 'current_step' in data:
            draft.current_step = data['current_step']
        
        draft.save()
        
        return jsonify({
            'success': True,
            'message': 'Draft updated successfully',
            'data': draft.to_dict()
        }), 200
        
    except DoesNotExist:
        return jsonify({
            'success': False,
            'error': 'Draft not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@drafting_bp.route('/<draft_id>/generate/<section>', methods=['POST'])
def generate_section(draft_id, section):
    """Generate AI content for a specific section"""
    try:
        draft = Draft.objects.get(id=draft_id)
        data = request.get_json()
        
        # Prepare draft data for AI
        draft_data = draft.to_dict()
        
        # Generate content based on section
        if section == 'background':
            content = ai_service.generate_background(draft_data)
            draft.background = content
        elif section == 'summary':
            content = ai_service.generate_summary(draft_data)
            draft.summary = content
        elif section == 'detailed_description':
            content = ai_service.generate_detailed_description(draft_data)
            draft.detailed_description = content
        elif section == 'claims':
            content = ai_service.generate_claims(draft_data)
            draft.claims = content
        elif section == 'abstract':
            content = ai_service.generate_abstract(draft_data)
            draft.abstract = content
        else:
            return jsonify({
                'success': False,
                'error': f'Invalid section: {section}'
            }), 400
        
        # Mark section as AI-generated
        draft.mark_section_generated(section)
        draft.add_generation_record(section, True)
        draft.save()
        
        return jsonify({
            'success': True,
            'data': {
                'content': content,
                'section': section
            },
            'message': f'{section.title()} generated successfully'
        }), 200
        
    except DoesNotExist:
        return jsonify({
            'success': False,
            'error': 'Draft not found'
        }), 404
    except Exception as e:
        try:
            draft.add_generation_record(section, False, str(e))
            draft.save()
        except:
            pass
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@drafting_bp.route('/<draft_id>/rephrase/<section>', methods=['POST'])
def rephrase_section(draft_id, section):
    """Rephrase or improve a specific section"""
    try:
        draft = Draft.objects.get(id=draft_id)
        data = request.get_json()
        
        instruction = data.get('instruction', 'improve clarity')
        
        # Get current section content
        current_content = getattr(draft, section, '')
        if not current_content:
            return jsonify({
                'success': False,
                'error': f'No content found for section: {section}'
            }), 400
        
        # Rephrase content
        new_content = ai_service.rephrase_section(current_content, section, instruction)
        
        # Update section
        setattr(draft, section, new_content)
        draft.save()
        
        return jsonify({
            'success': True,
            'content': new_content,
            'section': section,
            'message': f'{section.title()} rephrased successfully'
        }), 200
        
    except DoesNotExist:
        return jsonify({
            'success': False,
            'error': 'Draft not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@drafting_bp.route('/<draft_id>/upload-drawing', methods=['POST'])
def upload_drawing(draft_id):
    """Upload drawing/image for the draft"""
    try:
        draft = Draft.objects.get(id=draft_id)
        
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'File type not allowed'
            }), 400
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'success': False,
                'error': 'File too large (max 10MB)'
            }), 400
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Create drawing record
        drawing = Drawing(
            draft_id=str(draft.id),
            filename=unique_filename,
            original_filename=filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type,
            description=request.form.get('description', '')
        )
        drawing.save()
        
        return jsonify({
            'success': True,
            'drawing': drawing.to_dict(),
            'message': 'Drawing uploaded successfully'
        }), 201
        
    except DoesNotExist:
        return jsonify({
            'success': False,
            'error': 'Draft not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@drafting_bp.route('/<draft_id>/drawings', methods=['GET'])
def get_drawings(draft_id):
    """Get all drawings for a draft"""
    try:
        drawings = Drawing.objects(draft_id=draft_id)
        return jsonify({
            'success': True,
            'drawings': [drawing.to_dict() for drawing in drawings]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@drafting_bp.route('/<draft_id>/download', methods=['GET'])
def download_draft(draft_id):
    """Download draft as DOCX file"""
    try:
        draft = Draft.objects.get(id=draft_id)
        
        # Import here to avoid circular imports
        from docx_generator import generate_patent_docx
        
        # Generate DOCX file
        docx_path = generate_patent_docx(draft)
        
        return send_file(
            docx_path,
            as_attachment=True,
            download_name=f"patent_draft_{draft_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        )
        
    except DoesNotExist:
        return jsonify({
            'success': False,
            'error': 'Draft not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@drafting_bp.route('/projects/<user_id>', methods=['GET'])
def get_user_projects(user_id):
    """Get all projects for a user"""
    try:
        projects = Project.objects(user_id=user_id).order_by('-updated_at')
        return jsonify({
            'success': True,
            'projects': [project.to_dict() for project in projects]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@drafting_bp.route('/projects/<project_id>/drafts', methods=['GET'])
def get_project_drafts(project_id):
    """Get all drafts for a project"""
    try:
        drafts = Draft.objects(project_id=project_id).order_by('-updated_at')
        return jsonify({
            'success': True,
            'drafts': [draft.to_dict() for draft in drafts]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 