from mongoengine import connect, disconnect
from config import config
import os

def init_database(app):
    """Initialize MongoDB connection"""
    try:
        # Get configuration
        config_name = os.getenv('FLASK_CONFIG', 'default')
        app_config = config[config_name]
        
        # Connect to MongoDB
        connect(
            db=app_config.MONGODB_DB,
            host=app_config.MONGODB_URI,
            alias='default'
        )
        
        app.logger.info(f"Connected to MongoDB: {app_config.MONGODB_URI}")
        
    except Exception as e:
        app.logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

def close_database():
    """Close MongoDB connection"""
    try:
        disconnect(alias='default')
    except Exception as e:
        print(f"Error closing database connection: {str(e)}")

def create_indexes():
    """Create database indexes for better performance"""
    from models import Project, Draft, Drawing
    
    try:
        # Project indexes
        Project._get_collection().create_index([("user_id", 1)])
        Project._get_collection().create_index([("updated_at", -1)])
        
        # Draft indexes
        Draft._get_collection().create_index([("project_id", 1)])
        Draft._get_collection().create_index([("user_id", 1)])
        Draft._get_collection().create_index([("updated_at", -1)])
        
        # Drawing indexes
        Drawing._get_collection().create_index([("draft_id", 1)])
        Drawing._get_collection().create_index([("created_at", -1)])
        
        print("Database indexes created successfully")
        
    except Exception as e:
        print(f"Error creating indexes: {str(e)}") 