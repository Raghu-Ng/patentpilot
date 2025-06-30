#!/usr/bin/env python3
"""
Test script for the AI-Powered Patent Drafting Module
Tests all API endpoints and functionality
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
DRAFTS_URL = f"{BASE_URL}/drafts"

class DraftingModuleTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.draft_id = None
        self.project_id = None
        
    def log_test(self, test_name, success, message=""):
        """Log test results"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
    def test_health_check(self):
        """Test if the server is running"""
        try:
            response = self.session.get(f"{BASE_URL}/")
            if response.status_code == 200:
                self.log_test("Health Check", True, "Server is running")
                return True
            else:
                self.log_test("Health Check", False, f"Server returned {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_start_draft(self):
        """Test starting a new draft"""
        try:
            data = {
                "user_id": "test_user_123",
                "project_title": "Test Patent Project",
                "project_description": "A test project for validation",
                "title": "Smart Home Automation System",
                "field_of_invention": "Home Automation and IoT",
                "brief_summary": "An intelligent system for automating home devices using AI",
                "key_components": "Sensors, AI Controller, Mobile App, Cloud Platform",
                "problem_solved": "Manual control of home devices and lack of intelligent automation"
            }
            
            response = self.session.post(f"{DRAFTS_URL}/start", json=data)
            
            if response.status_code == 201:
                result = response.json()
                if result.get("success"):
                    self.draft_id = result.get("draft_id")
                    self.project_id = result.get("project_id")
                    self.log_test("Start Draft", True, f"Draft created: {self.draft_id}")
                    return True
                else:
                    self.log_test("Start Draft", False, result.get("error", "Unknown error"))
                    return False
            else:
                self.log_test("Start Draft", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Start Draft", False, f"Exception: {str(e)}")
            return False
    
    def test_get_draft(self):
        """Test retrieving draft details"""
        if not self.draft_id:
            self.log_test("Get Draft", False, "No draft ID available")
            return False
            
        try:
            response = self.session.get(f"{DRAFTS_URL}/{self.draft_id}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    draft = result.get("draft", {})
                    if draft.get("title") == "Smart Home Automation System":
                        self.log_test("Get Draft", True, "Draft retrieved successfully")
                        return True
                    else:
                        self.log_test("Get Draft", False, "Draft data mismatch")
                        return False
                else:
                    self.log_test("Get Draft", False, result.get("error", "Unknown error"))
                    return False
            else:
                self.log_test("Get Draft", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Get Draft", False, f"Exception: {str(e)}")
            return False
    
    def test_update_draft(self):
        """Test updating draft sections"""
        if not self.draft_id:
            self.log_test("Update Draft", False, "No draft ID available")
            return False
            
        try:
            data = {
                "title": "Updated Smart Home Automation System",
                "current_step": 2
            }
            
            response = self.session.patch(f"{DRAFTS_URL}/{self.draft_id}", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Update Draft", True, "Draft updated successfully")
                    return True
                else:
                    self.log_test("Update Draft", False, result.get("error", "Unknown error"))
                    return False
            else:
                self.log_test("Update Draft", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Update Draft", False, f"Exception: {str(e)}")
            return False
    
    def test_generate_background(self):
        """Test AI generation of background section"""
        if not self.draft_id:
            self.log_test("Generate Background", False, "No draft ID available")
            return False
            
        try:
            response = self.session.post(f"{DRAFTS_URL}/{self.draft_id}/generate/background")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    content = result.get("content", "")
                    if len(content) > 100:  # Basic content validation
                        self.log_test("Generate Background", True, f"Generated {len(content)} characters")
                        return True
                    else:
                        self.log_test("Generate Background", False, "Generated content too short")
                        return False
                else:
                    self.log_test("Generate Background", False, result.get("error", "Unknown error"))
                    return False
            else:
                self.log_test("Generate Background", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Generate Background", False, f"Exception: {str(e)}")
            return False
    
    def test_generate_summary(self):
        """Test AI generation of summary section"""
        if not self.draft_id:
            self.log_test("Generate Summary", False, "No draft ID available")
            return False
            
        try:
            response = self.session.post(f"{DRAFTS_URL}/{self.draft_id}/generate/summary")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    content = result.get("content", "")
                    if len(content) > 50:
                        self.log_test("Generate Summary", True, f"Generated {len(content)} characters")
                        return True
                    else:
                        self.log_test("Generate Summary", False, "Generated content too short")
                        return False
                else:
                    self.log_test("Generate Summary", False, result.get("error", "Unknown error"))
                    return False
            else:
                self.log_test("Generate Summary", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Generate Summary", False, f"Exception: {str(e)}")
            return False
    
    def test_rephrase_section(self):
        """Test rephrasing a section"""
        if not self.draft_id:
            self.log_test("Rephrase Section", False, "No draft ID available")
            return False
            
        try:
            data = {
                "instruction": "Make it more technical and detailed"
            }
            
            response = self.session.post(f"{DRAFTS_URL}/{self.draft_id}/rephrase/background", json=data)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    self.log_test("Rephrase Section", True, "Section rephrased successfully")
                    return True
                else:
                    self.log_test("Rephrase Section", False, result.get("error", "Unknown error"))
                    return False
            else:
                self.log_test("Rephrase Section", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Rephrase Section", False, f"Exception: {str(e)}")
            return False
    
    def test_get_drawings(self):
        """Test getting drawings for a draft"""
        if not self.draft_id:
            self.log_test("Get Drawings", False, "No draft ID available")
            return False
            
        try:
            response = self.session.get(f"{DRAFTS_URL}/{self.draft_id}/drawings")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    drawings = result.get("drawings", [])
                    self.log_test("Get Drawings", True, f"Retrieved {len(drawings)} drawings")
                    return True
                else:
                    self.log_test("Get Drawings", False, result.get("error", "Unknown error"))
                    return False
            else:
                self.log_test("Get Drawings", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Get Drawings", False, f"Exception: {str(e)}")
            return False
    
    def test_get_user_projects(self):
        """Test getting user projects"""
        try:
            response = self.session.get(f"{DRAFTS_URL}/projects/test_user_123")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    projects = result.get("projects", [])
                    self.log_test("Get User Projects", True, f"Retrieved {len(projects)} projects")
                    return True
                else:
                    self.log_test("Get User Projects", False, result.get("error", "Unknown error"))
                    return False
            else:
                self.log_test("Get User Projects", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Get User Projects", False, f"Exception: {str(e)}")
            return False
    
    def test_get_project_drafts(self):
        """Test getting drafts for a project"""
        if not self.project_id:
            self.log_test("Get Project Drafts", False, "No project ID available")
            return False
            
        try:
            response = self.session.get(f"{DRAFTS_URL}/projects/{self.project_id}/drafts")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    drafts = result.get("drafts", [])
                    self.log_test("Get Project Drafts", True, f"Retrieved {len(drafts)} drafts")
                    return True
                else:
                    self.log_test("Get Project Drafts", False, result.get("error", "Unknown error"))
                    return False
            else:
                self.log_test("Get Project Drafts", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Get Project Drafts", False, f"Exception: {str(e)}")
            return False
    
    def test_download_draft(self):
        """Test downloading draft as DOCX"""
        if not self.draft_id:
            self.log_test("Download Draft", False, "No draft ID available")
            return False
            
        try:
            response = self.session.get(f"{DRAFTS_URL}/{self.draft_id}/download")
            
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
                    self.log_test("Download Draft", True, "DOCX file downloaded successfully")
                    return True
                else:
                    self.log_test("Download Draft", False, f"Unexpected content type: {content_type}")
                    return False
            else:
                self.log_test("Download Draft", False, f"HTTP {response.status_code}: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Download Draft", False, f"Exception: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        try:
            # Test invalid draft ID
            response = self.session.get(f"{DRAFTS_URL}/invalid_id")
            if response.status_code == 404:
                self.log_test("Error Handling", True, "Properly handled invalid draft ID")
                return True
            else:
                self.log_test("Error Handling", False, f"Expected 404, got {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Error Handling", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Patent Drafting Module Tests")
        print("=" * 50)
        
        tests = [
            self.test_health_check,
            self.test_start_draft,
            self.test_get_draft,
            self.test_update_draft,
            self.test_generate_background,
            self.test_generate_summary,
            self.test_rephrase_section,
            self.test_get_drawings,
            self.test_get_user_projects,
            self.test_get_project_drafts,
            self.test_download_draft,
            self.test_error_handling
        ]
        
        for test in tests:
            try:
                test()
                time.sleep(1)  # Small delay between tests
            except Exception as e:
                self.log_test(test.__name__, False, f"Test failed with exception: {str(e)}")
        
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['test']}: {result['message']}")
        
        # Save results to file
        with open("test_results.json", "w") as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: test_results.json")
        
        if passed_tests == total_tests:
            print("\n🎉 ALL TESTS PASSED! The drafting module is working correctly.")
        else:
            print(f"\n⚠️  {failed_tests} test(s) failed. Please check the implementation.")

def main():
    """Main function to run tests"""
    tester = DraftingModuleTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 