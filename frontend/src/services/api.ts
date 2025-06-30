import axios from 'axios';
import { Draft, Project, Drawing, DraftFormData, DraftUpdateData, ApiResponse } from '../types/draft';

const API_BASE_URL = '/drafts';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const draftApi = {
  // Start a new draft
  startDraft: async (data: DraftFormData): Promise<ApiResponse<{ draft_id: string; project_id: string }>> => {
    try {
      const response = await api.post('/start', data);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
      };
    }
  },

  // Get draft details
  getDraft: async (draftId: string): Promise<ApiResponse<Draft>> => {
    try {
      const response = await api.get(`/${draftId}`);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
      };
    }
  },

  // Update draft
  updateDraft: async (draftId: string, data: DraftUpdateData): Promise<ApiResponse<Draft>> => {
    try {
      const response = await api.patch(`/${draftId}`, data);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
      };
    }
  },

  // Generate AI content for a section
  generateSection: async (draftId: string, section: string): Promise<ApiResponse<{ content: string; section: string }>> => {
    try {
      // Always send an empty object to ensure Content-Type: application/json
      const response = await api.post(`/${draftId}/generate/${section}`, {});
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
      };
    }
  },

  // Rephrase a section
  rephraseSection: async (draftId: string, section: string, instruction: string): Promise<ApiResponse<{ content: string; section: string }>> => {
    try {
      const response = await api.post(`/${draftId}/rephrase/${section}`, { instruction });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
      };
    }
  },

  // Upload drawing
  uploadDrawing: async (draftId: string, file: File, description?: string): Promise<ApiResponse<Drawing>> => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (description) {
        formData.append('description', description);
      }

      const response = await axios.post(`${API_BASE_URL}/${draftId}/upload-drawing`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
      };
    }
  },

  // Get drawings for a draft
  getDrawings: async (draftId: string): Promise<ApiResponse<Drawing[]>> => {
    try {
      const response = await api.get(`/${draftId}/drawings`);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
      };
    }
  },

  // Download draft as DOCX
  downloadDraft: async (draftId: string): Promise<Blob> => {
    const response = await api.get(`/${draftId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Get user projects
  getUserProjects: async (userId: string): Promise<ApiResponse<Project[]>> => {
    try {
      const response = await api.get(`/projects/${userId}`);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
      };
    }
  },

  // Get project drafts
  getProjectDrafts: async (projectId: string): Promise<ApiResponse<Draft[]>> => {
    try {
      const response = await api.get(`/projects/${projectId}/drafts`);
      return response.data;
    } catch (error: any) {
      return {
        success: false,
        error: error.response?.data?.error || error.message,
      };
    }
  },
}; 