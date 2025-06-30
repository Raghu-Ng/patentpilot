export interface Draft {
  id: string;
  project_id: string;
  title: string;
  field_of_invention: string;
  brief_summary: string;
  key_components: string;
  problem_solved: string;
  background: string;
  summary: string;
  detailed_description: string;
  claims: string;
  abstract: string;
  current_step: number;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
  ai_generated_sections: string[];
  generation_history: GenerationRecord[];
}

export interface Project {
  id: string;
  user_id: string;
  title: string;
  description: string;
  created_at: string;
  updated_at: string;
  status: string;
  draft_count: number;
}

export interface Drawing {
  id: string;
  draft_id: string;
  filename: string;
  original_filename: string;
  file_size: number;
  mime_type: string;
  description: string;
  created_at: string;
}

export interface GenerationRecord {
  section: string;
  timestamp: string;
  success: boolean;
  error_message?: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface DraftFormData {
  user_id: string;
  project_title: string;
  project_description: string;
  title: string;
  field_of_invention: string;
  brief_summary: string;
  key_components: string;
  problem_solved: string;
}

export interface DraftUpdateData {
  title?: string;
  field_of_invention?: string;
  brief_summary?: string;
  key_components?: string;
  problem_solved?: string;
  background?: string;
  summary?: string;
  detailed_description?: string;
  claims?: string;
  abstract?: string;
  current_step?: number;
} 