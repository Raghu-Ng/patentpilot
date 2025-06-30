import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # MongoDB Atlas settings
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/patentpilot')
    MONGODB_DB = os.getenv('MONGODB_DB', 'patentpilot')
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'pdf'}
    
    # Document generation settings
    GENERATED_DOCS_FOLDER = 'generated_docs'
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        pass

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    MONGODB_URI = os.getenv('DEV_MONGODB_URI', 'mongodb://localhost:27017/patentpilot_dev')

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    MONGODB_URI = os.getenv('PROD_MONGODB_URI')

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    MONGODB_URI = os.getenv('TEST_MONGODB_URI', 'mongodb://localhost:27017/patentpilot_test')

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 