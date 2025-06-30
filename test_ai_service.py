#!/usr/bin/env python3
"""
Test script to check AI service functionality
"""

import os
from dotenv import load_dotenv

def test_ai_service():
    """Test AI service initialization and basic functionality"""
    print("Testing AI Service...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check OpenAI API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("❌ OPENAI_API_KEY not set or using default value")
        print("   Please add your OpenAI API key to the .env file")
        return False
    
    print("✅ OPENAI_API_KEY is set")
    
    # Test AI service initialization
    try:
        from ai_service import PatentAIService
        ai_service = PatentAIService()
        print("✅ AI service initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize AI service: {str(e)}")
        return False
    
    # Test basic content generation
    try:
        test_data = {
            'title': 'Test Invention',
            'field_of_invention': 'Technology',
            'brief_summary': 'A test invention for testing purposes',
            'key_components': 'Component A, Component B',
            'problem_solved': 'Testing the AI service'
        }
        
        print("🔄 Testing content generation...")
        content = ai_service.generate_background(test_data)
        
        if content and len(content) > 50:
            print("✅ Content generation successful")
            print(f"   Generated {len(content)} characters")
        else:
            print("❌ Content generation failed or returned empty content")
            return False
            
    except Exception as e:
        print(f"❌ Content generation failed: {str(e)}")
        return False
    
    print("\n" + "=" * 50)
    print("AI service test completed successfully!")
    return True

if __name__ == "__main__":
    test_ai_service() 