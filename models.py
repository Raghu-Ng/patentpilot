from mongoengine import Document, StringField, DateTimeField, BooleanField, IntField, ListField, ReferenceField, EmbeddedDocument, EmbeddedDocumentField
from datetime import datetime
import json

class Project(Document):
    """Model for storing patent projects"""
    meta = {'collection': 'projects'}
    
    user_id = StringField(required=True, max_length=100)
    title = StringField(required=True, max_length=200)
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    status = StringField(default='draft', max_length=50)  # draft, completed, archived
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'status': self.status,
            'draft_count': Draft.objects(project_id=self.id).count()
        }
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)

class GenerationRecord(EmbeddedDocument):
    """Embedded document for AI generation history"""
    section = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)
    success = BooleanField(required=True)
    error_message = StringField()

class Drawing(Document):
    """Model for storing patent drawings/images"""
    meta = {'collection': 'drawings'}
    
    draft_id = StringField(required=True)
    filename = StringField(required=True, max_length=255)
    original_filename = StringField(required=True, max_length=255)
    file_path = StringField(required=True, max_length=500)
    file_size = IntField()
    mime_type = StringField(max_length=100)
    description = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'draft_id': self.draft_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'mime_type': self.mime_type,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

class Draft(Document):
    """Model for storing patent draft specifications"""
    meta = {'collection': 'drafts'}
    
    project_id = StringField(required=True)
    
    # Basic information
    title = StringField(max_length=200)
    field_of_invention = StringField(max_length=200)
    brief_summary = StringField()
    key_components = StringField()
    problem_solved = StringField()
    
    # Patent sections
    background = StringField()
    summary = StringField()
    detailed_description = StringField()
    claims = StringField()
    abstract = StringField()
    
    # Metadata
    current_step = IntField(default=1)  # 1-8 for the 8 drafting steps
    is_complete = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    # AI generation metadata
    ai_generated_sections = ListField(StringField(), default=list)
    generation_history = ListField(EmbeddedDocumentField(GenerationRecord), default=list)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'project_id': self.project_id,
            'title': self.title,
            'field_of_invention': self.field_of_invention,
            'brief_summary': self.brief_summary,
            'key_components': self.key_components,
            'problem_solved': self.problem_solved,
            'background': self.background,
            'summary': self.summary,
            'detailed_description': self.detailed_description,
            'claims': self.claims,
            'abstract': self.abstract,
            'current_step': self.current_step,
            'is_complete': self.is_complete,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'ai_generated_sections': self.ai_generated_sections,
            'generation_history': [
                {
                    'section': record.section,
                    'timestamp': record.timestamp.isoformat(),
                    'success': record.success,
                    'error_message': record.error_message
                } for record in self.generation_history
            ]
        }
    
    def update_section(self, section_name, content):
        """Update a specific section of the draft"""
        if hasattr(self, section_name):
            setattr(self, section_name, content)
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def mark_section_generated(self, section_name):
        """Mark a section as AI-generated"""
        if section_name not in self.ai_generated_sections:
            self.ai_generated_sections.append(section_name)
    
    def add_generation_record(self, section_name, success, error_message=None):
        """Add a record of AI generation attempt"""
        record = GenerationRecord(
            section=section_name,
            success=success,
            error_message=error_message
        )
        self.generation_history.append(record)
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs) 