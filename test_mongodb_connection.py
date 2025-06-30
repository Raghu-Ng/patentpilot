#!/usr/bin/env python3
"""
Test script to verify MongoDB Atlas connection
"""

import os
from dotenv import load_dotenv
from mongoengine import connect, disconnect
from config import Config

def test_mongodb_connection():
    """Test MongoDB Atlas connection"""
    print("Testing MongoDB Atlas connection...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    config = Config()
    
    try:
        # Connect to MongoDB Atlas
        print(f"Connecting to MongoDB Atlas...")
        print(f"Database: {config.MONGODB_DB}")
        
        # Mask the URI for security
        masked_uri = config.MONGODB_URI
        if '@' in masked_uri:
            parts = masked_uri.split('@')
            user_pass = parts[0].split(':')
            if len(user_pass) >= 3:
                masked_uri = f"{user_pass[0]}:***@{parts[1]}"
        
        print(f"URI: {masked_uri}")
        
        # Connect to MongoDB
        connect(
            db=config.MONGODB_DB,
            host=config.MONGODB_URI,
            alias='test_connection'
        )
        
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Test a simple operation
        from mongoengine.connection import get_db
        db = get_db('test_connection')
        collections = db.list_collection_names()
        print(f"✅ Database accessible. Collections found: {len(collections)}")
        
        # Disconnect
        disconnect(alias='test_connection')
        print("✅ Connection closed successfully")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check if your .env file exists and contains MONGODB_URI")
        print("2. Verify your MongoDB Atlas credentials")
        print("3. Ensure your IP is whitelisted in MongoDB Atlas")
        print("4. Check if the cluster is running")
        return False
    
    print("\n" + "=" * 50)
    print("MongoDB connection test completed!")
    return True

if __name__ == "__main__":
    test_mongodb_connection() 