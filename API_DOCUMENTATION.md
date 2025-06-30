# Patent Drafting Module API Documentation

## Overview

The Patent Drafting Module provides a comprehensive API for AI-powered patent specification drafting. It uses MongoDB Atlas for data storage and OpenAI GPT for content generation.

## Base URL

```
http://localhost:5000/drafts
```

## Authentication

Currently, the API uses a simple user ID system. In production, implement proper JWT authentication.

## API Endpoints

### 1. Start New Draft

**POST** `/drafts/start`

Creates a new patent draft and project.

**Request Body:**
```json
{
  "user_id": "string",
  "project_title": "string",
  "project_description": "string",
  "title": "string",
  "field_of_invention": "string",
  "brief_summary": "string",
  "key_components": "string",
  "problem_solved": "string"
}
```

**Response:**
```json
{
  "success": true,
  "draft_id": "string",
  "project_id": "string",
  "message": "Draft started successfully"
}
```

### 2. Get Draft Details

**GET** `/drafts/{draft_id}`

Retrieves a specific draft by ID.

**Response:**
```json
{
  "success": true,
  "draft": {
    "id": "string",
    "project_id": "string",
    "title": "string",
    "field_of_invention": "string",
    "brief_summary": "string",
    "key_components": "string",
    "problem_solved": "string",
    "background": "string",
    "summary": "string",
    "detailed_description": "string",
    "claims": "string",
    "abstract": "string",
    "current_step": 1,
    "is_complete": false,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "ai_generated_sections": ["background", "summary"],
    "generation_history": [
      {
        "section": "background",
        "timestamp": "2024-01-01T00:00:00",
        "success": true,
        "error_message": null
      }
    ]
  }
}
```

### 3. Update Draft

**PATCH** `/drafts/{draft_id}`

Updates draft sections and metadata.

**Request Body:**
```json
{
  "title": "string",
  "field_of_invention": "string",
  "brief_summary": "string",
  "key_components": "string",
  "problem_solved": "string",
  "background": "string",
  "summary": "string",
  "detailed_description": "string",
  "claims": "string",
  "abstract": "string",
  "current_step": 1
}
```

**Response:**
```json
{
  "success": true,
  "message": "Draft updated successfully",
  "draft": { /* draft object */ }
}
```

### 4. Generate AI Content

**POST** `/drafts/{draft_id}/generate/{section}`

Generates AI content for a specific section.

**Supported Sections:**
- `background`
- `summary`
- `detailed_description`
- `claims`
- `abstract`

**Response:**
```json
{
  "success": true,
  "content": "Generated content...",
  "section": "background",
  "message": "Background generated successfully"
}
```

### 5. Rephrase Section

**POST** `/drafts/{draft_id}/rephrase/{section}`

Rephrases or improves a specific section.

**Request Body:**
```json
{
  "instruction": "Make it more technical"
}
```

**Response:**
```json
{
  "success": true,
  "content": "Rephrased content...",
  "section": "background",
  "message": "Background rephrased successfully"
}
```

### 6. Upload Drawing

**POST** `/drafts/{draft_id}/upload-drawing`

Uploads a drawing or image for the draft.

**Request:** Multipart form data
- `file`: Image file (PNG, JPG, JPEG, GIF, BMP, TIFF, PDF)
- `description`: Optional description

**Response:**
```json
{
  "success": true,
  "drawing": {
    "id": "string",
    "draft_id": "string",
    "filename": "string",
    "original_filename": "string",
    "file_size": 12345,
    "mime_type": "image/png",
    "description": "string",
    "created_at": "2024-01-01T00:00:00"
  },
  "message": "Drawing uploaded successfully"
}
```

### 7. Get Drawings

**GET** `/drafts/{draft_id}/drawings`

Retrieves all drawings for a draft.

**Response:**
```json
{
  "success": true,
  "drawings": [
    {
      "id": "string",
      "draft_id": "string",
      "filename": "string",
      "original_filename": "string",
      "file_size": 12345,
      "mime_type": "image/png",
      "description": "string",
      "created_at": "2024-01-01T00:00:00"
    }
  ]
}
```

### 8. Download Draft

**GET** `/drafts/{draft_id}/download`

Downloads the complete patent specification as a DOCX file.

**Response:** DOCX file download

### 9. Get User Projects

**GET** `/drafts/projects/{user_id}`

Retrieves all projects for a user.

**Response:**
```json
{
  "success": true,
  "projects": [
    {
      "id": "string",
      "user_id": "string",
      "title": "string",
      "description": "string",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "status": "draft",
      "draft_count": 1
    }
  ]
}
```

### 10. Get Project Drafts

**GET** `/drafts/projects/{project_id}/drafts`

Retrieves all drafts for a project.

**Response:**
```json
{
  "success": true,
  "drafts": [
    {
      "id": "string",
      "project_id": "string",
      "title": "string",
      "current_step": 1,
      "is_complete": false,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  ]
}
```

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

## Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

## File Upload Limits

- Maximum file size: 10MB
- Supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF, PDF

## Environment Variables

Required environment variables:

```bash
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/database
OPENAI_API_KEY=your-openai-api-key
FLASK_CONFIG=development
SECRET_KEY=your-secret-key
```

## Example Usage

### Starting a New Draft

```bash
curl -X POST http://localhost:5000/drafts/start \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "project_title": "My Patent Project",
    "title": "Smart Home Automation System",
    "field_of_invention": "Home Automation",
    "brief_summary": "A system for automating home devices",
    "key_components": "Sensors, Controller, Mobile App",
    "problem_solved": "Manual control of home devices"
  }'
```

### Generating AI Content

```bash
curl -X POST http://localhost:5000/drafts/draft_id_here/generate/background \
  -H "Content-Type: application/json"
```

### Uploading a Drawing

```bash
curl -X POST http://localhost:5000/drafts/draft_id_here/upload-drawing \
  -F "file=@diagram.png" \
  -F "description=System Architecture Diagram"
```

## Testing

Use the provided test script or tools like Postman to test the API endpoints.

## Support

For issues and questions, please refer to the project documentation or create an issue in the repository. 