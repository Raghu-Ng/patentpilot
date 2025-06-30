#!/usr/bin/env python3
"""
Test script to directly test the generate endpoint
"""

import requests
import json

def test_generate_endpoint():
    """Test the generate endpoint directly"""
    print("Testing generate endpoint...")
    print("=" * 50)
    
    # First, create a draft
    draft_data = {
        "user_id": "test_user",
        "project_title": "Test Project",
        "project_description": "Test Description",
        "title": "Test Invention",
        "field_of_invention": "Technology",
        "brief_summary": "A test invention",
        "key_components": "Component A, Component B",
        "problem_solved": "Testing the system"
    }
    
    try:
        # Create a draft
        print("Creating a test draft...")
        response = requests.post('http://localhost:5000/drafts/start', json=draft_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            draft_response = response.json()
            draft_id = draft_response['data']['draft_id']
            print(f"✅ Draft created with ID: {draft_id}")
            
            # Test generate background
            print(f"\nTesting generate background for draft {draft_id}...")
            generate_response = requests.post(
                f'http://localhost:5000/drafts/{draft_id}/generate/background',
                headers={'Content-Type': 'application/json'},
                json={}  # Empty JSON body
            )
            print(f"Status: {generate_response.status_code}")
            print(f"Response: {generate_response.text}")
            
            if generate_response.status_code == 200:
                print("✅ Generate endpoint working!")
            else:
                print("❌ Generate endpoint failed")
                
        else:
            print(f"❌ Failed to create draft: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask backend. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_generate_endpoint() 