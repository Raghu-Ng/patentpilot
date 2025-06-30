#!/usr/bin/env python3
"""
Script to create .env file with MongoDB Atlas connection string
"""

def create_env_file():
    """Create .env file with MongoDB Atlas configuration"""
    
    env_content = """# MongoDB Atlas Configuration
MONGODB_URI=mongodb+srv://unwelcome8:uEqMdayg3Z2gqzJg@patent.mhglrif.mongodb.net/?retryWrites=true&w=majority&appName=patent
MONGODB_DB=patentpilot

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_DEBUG=True

# OpenAI Configuration (add your API key here)
OPENAI_API_KEY=your-openai-api-key-here

# Development MongoDB URI (set to Atlas for development)
DEV_MONGODB_URI=mongodb+srv://unwelcome8:uEqMdayg3Z2gqzJg@patent.mhglrif.mongodb.net/?retryWrites=true&w=majority&appName=patent

# Production MongoDB URI (optional, for production deployment)
PROD_MONGODB_URI=mongodb+srv://unwelcome8:uEqMdayg3Z2gqzJg@patent.mhglrif.mongodb.net/?retryWrites=true&w=majority&appName=patent

# Testing MongoDB URI (optional, for testing)
TEST_MONGODB_URI=mongodb://localhost:27017/patentpilot_test
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file updated successfully!")
        print("📝 File now contains correct DEV_MONGODB_URI for MongoDB Atlas")
        return True
    except Exception as e:
        print(f"❌ Error updating .env file: {str(e)}")
        return False

if __name__ == "__main__":
    create_env_file() 