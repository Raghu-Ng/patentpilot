import React, { useState } from 'react';
import { Draft, DraftUpdateData } from '../../types/draft';
import { draftApi } from '../../services/api';

interface Step1Props {
  draft: Draft;
  updateDraft: (data: DraftUpdateData) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const Step1InitialQuestions: React.FC<Step1Props> = ({ draft, updateDraft, loading, error }) => {
  const [formData, setFormData] = useState({
    title: draft.title || '',
    field_of_invention: draft.field_of_invention || '',
    brief_summary: draft.brief_summary || '',
    key_components: draft.key_components || '',
    problem_solved: draft.problem_solved || ''
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    await updateDraft(formData);
  };

  const handleGenerateWithAI = async () => {
    // AI generation is not applicable for basic form fields
    alert('AI generation is not available for this step. Please fill in the basic information manually.');
  };

  return (
    <div className="step-container">
      <div className="row">
        <div className="col-12">
          <h2 className="mb-4">
            <i className="fas fa-question-circle text-primary me-2"></i>
            Step 1: Initial Questions
          </h2>
          
          <div className="alert alert-info">
            <h5><i className="fas fa-info-circle me-2"></i>Getting Started</h5>
            <p className="mb-0">
              Let's start by understanding your invention. Answer these basic questions to help us create a comprehensive patent specification.
            </p>
          </div>

          <form onSubmit={(e) => { e.preventDefault(); handleSave(); }}>
            <div className="row">
              <div className="col-md-12 mb-3">
                <label htmlFor="title" className="form-label">
                  <strong>1. What is the title of your invention?</strong>
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleInputChange}
                  placeholder="e.g., Smart Home Energy Management System"
                  required
                />
                <div className="form-text">
                  Choose a clear, descriptive title that captures the essence of your invention.
                </div>
              </div>

              <div className="col-md-12 mb-3">
                <label htmlFor="field_of_invention" className="form-label">
                  <strong>2. What field of technology does your invention belong to?</strong>
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="field_of_invention"
                  name="field_of_invention"
                  value={formData.field_of_invention}
                  onChange={handleInputChange}
                  placeholder="e.g., Computer Science, Mechanical Engineering, Biotechnology"
                  required
                />
                <div className="form-text">
                  Specify the technical field or industry sector your invention relates to.
                </div>
              </div>

              <div className="col-md-12 mb-3">
                <label htmlFor="brief_summary" className="form-label">
                  <strong>3. Provide a brief summary of your invention</strong>
                </label>
                <textarea
                  className="form-control"
                  id="brief_summary"
                  name="brief_summary"
                  rows={4}
                  value={formData.brief_summary}
                  onChange={handleInputChange}
                  placeholder="Describe what your invention does and how it works in simple terms..."
                  required
                ></textarea>
                <div className="form-text">
                  Explain the core concept and functionality of your invention in 2-3 sentences.
                </div>
              </div>

              <div className="col-md-12 mb-3">
                <label htmlFor="key_components" className="form-label">
                  <strong>4. What are the key components or elements of your invention?</strong>
                </label>
                <textarea
                  className="form-control"
                  id="key_components"
                  name="key_components"
                  rows={3}
                  value={formData.key_components}
                  onChange={handleInputChange}
                  placeholder="List the main parts, systems, or features that make up your invention..."
                  required
                ></textarea>
                <div className="form-text">
                  Identify the essential parts, systems, or features that are central to your invention.
                </div>
              </div>

              <div className="col-md-12 mb-3">
                <label htmlFor="problem_solved" className="form-label">
                  <strong>5. What problem does your invention solve?</strong>
                </label>
                <textarea
                  className="form-control"
                  id="problem_solved"
                  name="problem_solved"
                  rows={3}
                  value={formData.problem_solved}
                  onChange={handleInputChange}
                  placeholder="Describe the problem or limitation that your invention addresses..."
                  required
                ></textarea>
                <div className="form-text">
                  Explain the specific problem, inefficiency, or limitation that your invention overcomes.
                </div>
              </div>
            </div>

            <div className="d-flex justify-content-between mt-4">
              <button
                type="button"
                className="btn btn-outline-secondary"
                onClick={handleGenerateWithAI}
                disabled={loading}
              >
                <i className="fas fa-info-circle me-2"></i>
                Help & Tips
              </button>
              
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                    Saving...
                  </>
                ) : (
                  <>
                    <i className="fas fa-save me-2"></i>
                    Save & Continue
                  </>
                )}
              </button>
            </div>
          </form>

          {error && (
            <div className="alert alert-danger mt-3">
              <i className="fas fa-exclamation-triangle me-2"></i>
              {error}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Step1InitialQuestions; 