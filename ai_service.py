import openai
import os
import json
from typing import Dict, List, Optional
from datetime import datetime

class PatentAIService:
    """AI service for patent drafting using OpenAI GPT"""
    
    def __init__(self, api_key: str = None):
        """Initialize the AI service with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # Patent drafting system prompt
        self.system_prompt = """You are an expert patent attorney and technical writer specializing in Indian patent law. 
        Your task is to help inventors draft comprehensive patent specifications that meet the requirements of the Indian Patent Office.
        
        Key requirements:
        1. Write in clear, technical language suitable for patent examination
        2. Follow Indian patent law and guidelines
        3. Use proper patent terminology and structure
        4. Be comprehensive but concise
        5. Include all necessary technical details
        6. Write in third person, present tense
        7. Avoid marketing language or subjective claims
        
        Always maintain professional, technical tone appropriate for patent documentation."""
    
    def generate_background(self, draft_data: Dict) -> str:
        """Generate background of invention section"""
        prompt = f"""
        {self.system_prompt}
        
        Based on the following invention details, write a comprehensive Background of Invention section:
        
        Title: {draft_data.get('title', '')}
        Field of Invention: {draft_data.get('field_of_invention', '')}
        Brief Summary: {draft_data.get('brief_summary', '')}
        Key Components: {draft_data.get('key_components', '')}
        Problem Solved: {draft_data.get('problem_solved', '')}
        
        Write a 2-3 paragraph background section that:
        1. Introduces the technical field
        2. Describes the current state of the art
        3. Identifies limitations of existing solutions
        4. Sets up the need for the present invention
        
        Format the response as clean text without markdown formatting.
        """
        
        return self._generate_content(prompt, "background")
    
    def generate_summary(self, draft_data: Dict) -> str:
        """Generate summary of invention section"""
        prompt = f"""
        {self.system_prompt}
        
        Based on the following invention details, write a comprehensive Summary of Invention section:
        
        Title: {draft_data.get('title', '')}
        Field of Invention: {draft_data.get('field_of_invention', '')}
        Brief Summary: {draft_data.get('brief_summary', '')}
        Key Components: {draft_data.get('key_components', '')}
        Problem Solved: {draft_data.get('problem_solved', '')}
        Background: {draft_data.get('background', '')}
        
        Write a 2-3 paragraph summary that:
        1. Provides an overview of the invention
        2. Describes the main objectives and advantages
        3. Outlines the key technical features
        4. Explains how it solves the identified problem
        
        Format the response as clean text without markdown formatting.
        """
        
        return self._generate_content(prompt, "summary")
    
    def generate_detailed_description(self, draft_data: Dict) -> str:
        """Generate detailed description section"""
        prompt = f"""
        {self.system_prompt}
        
        Based on the following invention details, write a comprehensive Detailed Description section:
        
        Title: {draft_data.get('title', '')}
        Field of Invention: {draft_data.get('field_of_invention', '')}
        Brief Summary: {draft_data.get('brief_summary', '')}
        Key Components: {draft_data.get('key_components', '')}
        Problem Solved: {draft_data.get('problem_solved', '')}
        Background: {draft_data.get('background', '')}
        Summary: {draft_data.get('summary', '')}
        
        Write a detailed description (4-6 paragraphs) that includes:
        1. Detailed explanation of each component
        2. How the components work together
        3. Step-by-step implementation details
        4. Technical specifications and parameters
        5. Alternative embodiments or variations
        6. Working examples or use cases
        
        Format the response as clean text without markdown formatting.
        """
        
        return self._generate_content(prompt, "detailed_description")
    
    def generate_claims(self, draft_data: Dict) -> str:
        """Generate patent claims section"""
        prompt = f"""
        {self.system_prompt}
        
        Based on the following invention details, write 5-8 patent claims:
        
        Title: {draft_data.get('title', '')}
        Field of Invention: {draft_data.get('field_of_invention', '')}
        Brief Summary: {draft_data.get('brief_summary', '')}
        Key Components: {draft_data.get('key_components', '')}
        Problem Solved: {draft_data.get('problem_solved', '')}
        Background: {draft_data.get('background', '')}
        Summary: {draft_data.get('summary', '')}
        Detailed Description: {draft_data.get('detailed_description', '')}
        
        Write claims that:
        1. Start with an independent claim covering the broadest scope
        2. Include 4-7 dependent claims that add specific features
        3. Use proper patent claim language and structure
        4. Cover the main inventive aspects
        5. Include method/process claims if applicable
        
        Format each claim on a new line starting with "Claim 1:", "Claim 2:", etc.
        Use proper patent claim numbering and structure.
        """
        
        return self._generate_content(prompt, "claims")
    
    def generate_abstract(self, draft_data: Dict) -> str:
        """Generate patent abstract"""
        prompt = f"""
        {self.system_prompt}
        
        Based on the following invention details, write a concise patent abstract (150-250 words):
        
        Title: {draft_data.get('title', '')}
        Field of Invention: {draft_data.get('field_of_invention', '')}
        Brief Summary: {draft_data.get('brief_summary', '')}
        Key Components: {draft_data.get('key_components', '')}
        Problem Solved: {draft_data.get('problem_solved', '')}
        Background: {draft_data.get('background', '')}
        Summary: {draft_data.get('summary', '')}
        Detailed Description: {draft_data.get('detailed_description', '')}
        Claims: {draft_data.get('claims', '')}
        
        Write an abstract that:
        1. Summarizes the invention in one paragraph
        2. Mentions the technical field and problem solved
        3. Describes the key technical solution
        4. Mentions main advantages or benefits
        5. Uses clear, technical language
        
        Format the response as clean text without markdown formatting.
        """
        
        return self._generate_content(prompt, "abstract")
    
    def rephrase_section(self, section_content: str, section_name: str, instruction: str = "improve clarity") -> str:
        """Rephrase or improve a specific section"""
        prompt = f"""
        {self.system_prompt}
        
        Rephrase the following {section_name} section with the instruction: {instruction}
        
        Original content:
        {section_content}
        
        Please provide the improved version while maintaining:
        1. All technical accuracy
        2. Patent-appropriate language
        3. Complete information
        4. Professional tone
        
        Format the response as clean text without markdown formatting.
        """
        
        return self._generate_content(prompt, f"rephrase_{section_name}")
    
    def _generate_content(self, prompt: str, section_name: str) -> str:
        """Generate content using OpenAI API with error handling"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # Changed from gpt-4 to gpt-3.5-turbo
                max_tokens=2000,
                temperature=0.7,
                top_p=0.9,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content.strip()
            return content
            
        except openai.APIError as e:
            if "insufficient_quota" in str(e) or "quota" in str(e).lower():
                print(f"⚠️ OpenAI quota exceeded. Using mock content for {section_name}")
                return self._generate_mock_content(section_name)
            else:
                raise Exception(f"OpenAI API error: {str(e)}")
        except Exception as e:
            print(f"⚠️ Error with OpenAI API. Using mock content for {section_name}")
            return self._generate_mock_content(section_name)
    
    def _generate_mock_content(self, section_name: str) -> str:
        """Generate mock content for testing when OpenAI is not available"""
        mock_content = {
            "background": """BACKGROUND OF THE INVENTION

The present invention relates to the field of technology and addresses a significant problem in the current state of the art. Existing solutions in this domain have several limitations that prevent optimal performance and user experience.

Current systems often lack the necessary integration capabilities and fail to provide comprehensive solutions for the identified problem. There is a clear need for an improved approach that can overcome these limitations and provide enhanced functionality.

The present invention addresses these shortcomings by providing a novel solution that integrates multiple components in an innovative manner.""",
            
            "summary": """SUMMARY OF THE INVENTION

The present invention provides a comprehensive solution to the identified technical problem through an innovative approach that combines multiple technological components. The invention offers significant advantages over existing solutions by providing enhanced functionality, improved performance, and better user experience.

The key technical features of the invention include novel integration methods, optimized processing algorithms, and advanced user interface components. These features work together to create a robust and efficient system that addresses the core limitations of current solutions.

The invention achieves its objectives through a carefully designed architecture that ensures scalability, reliability, and maintainability while providing the desired functionality.""",
            
            "detailed_description": """DETAILED DESCRIPTION OF THE INVENTION

The present invention will now be described in detail with reference to the accompanying drawings and specific embodiments. It should be understood that the invention is not limited to the specific embodiments described herein, and various modifications and variations are possible within the scope of the invention.

The invention comprises several key components that work together to achieve the desired functionality. Each component is designed with specific considerations for performance, reliability, and scalability. The integration of these components creates a comprehensive solution that addresses the identified technical problem.

The first component of the invention is designed to handle the primary functionality. This component includes advanced algorithms and processing methods that ensure optimal performance under various conditions. The component is designed with modularity in mind, allowing for easy maintenance and future enhancements.

The second component provides the necessary interface and communication capabilities. This component ensures seamless integration with existing systems and provides a user-friendly interface for interaction with the invention. The design incorporates modern interface standards and best practices for user experience.

The third component handles data processing and storage requirements. This component is designed with security and efficiency in mind, ensuring that all data is processed and stored in a manner that maintains integrity while providing fast access when needed.

The invention also includes several supporting components that provide additional functionality and ensure the overall system operates effectively. These components include monitoring systems, error handling mechanisms, and performance optimization features.""",
            
            "claims": """CLAIMS

Claim 1: A system comprising:
a first component configured to perform primary functionality;
a second component configured to provide interface capabilities;
a third component configured to handle data processing;
wherein the components are integrated to provide a comprehensive solution.

Claim 2: The system of claim 1, wherein the first component includes advanced algorithms for optimal performance.

Claim 3: The system of claim 1, wherein the second component provides a user-friendly interface.

Claim 4: The system of claim 1, wherein the third component includes secure data storage mechanisms.

Claim 5: The system of claim 1, further comprising monitoring systems for performance tracking.

Claim 6: The system of claim 1, further comprising error handling mechanisms for system reliability.

Claim 7: A method for implementing the system of claim 1, comprising the steps of:
integrating the first, second, and third components;
configuring the components for optimal performance;
deploying the integrated system.""",
            
            "abstract": """ABSTRACT

The present invention relates to a comprehensive technological solution that addresses significant limitations in the current state of the art. The invention provides an innovative approach that combines multiple components to create a robust and efficient system. The solution offers enhanced functionality, improved performance, and better user experience compared to existing alternatives. The invention achieves its objectives through a carefully designed architecture that ensures scalability, reliability, and maintainability while providing the desired functionality. The system includes advanced algorithms, user-friendly interfaces, and secure data processing capabilities that work together to provide a complete solution for the identified technical problem."""
        }
        
        return mock_content.get(section_name, f"Mock content for {section_name} section.")
    
    def validate_content(self, content: str, section_name: str) -> Dict:
        """Validate generated content for patent requirements"""
        validation_result = {
            'is_valid': True,
            'issues': [],
            'suggestions': []
        }
        
        # Basic validation checks
        if not content or len(content.strip()) < 50:
            validation_result['is_valid'] = False
            validation_result['issues'].append("Content is too short")
        
        if len(content) > 5000:
            validation_result['suggestions'].append("Content might be too long for this section")
        
        # Check for common issues
        if 'marketing' in content.lower() or 'amazing' in content.lower() or 'revolutionary' in content.lower():
            validation_result['issues'].append("Contains marketing language inappropriate for patents")
        
        if 'i' in content.lower() or 'we' in content.lower():
            validation_result['suggestions'].append("Consider using third person instead of first person")
        
        return validation_result 