# Patent Application Form Generator

This is a web application that generates patent application forms using a Word template. It provides a user-friendly interface to input all required information and generates a filled Word document.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure you have the Word template file (`form1_template.docx`) in the root directory.

3. Run the Flask application:
```bash
python app.py
```

4. Open your web browser and navigate to `http://localhost:5000`

## Features

- Clean, modern user interface
- Form validation
- Support for multiple applicants
- Automatic document generation
- Download generated document

## Usage

1. Fill in all the required fields in the web form
2. Click the "Generate Document" button
3. The filled Word document will be automatically downloaded

## File Structure

- `app.py` - Flask application
- `templates/index.html` - Web form template
- `form1_template.docx` - Word template for the patent application
- `requirements.txt` - Python dependencies #   p a t e n t p i l o t  
 