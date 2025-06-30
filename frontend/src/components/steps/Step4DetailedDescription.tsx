import React, { useState } from 'react';
import { Draft, DraftUpdateData } from '../../types/draft';
import { draftApi } from '../../services/api';

interface Step4Props {
  draft: Draft;
  updateDraft: (data: DraftUpdateData) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const Step4DetailedDescription: React.FC<Step4Props> = ({ draft, updateDraft, loading, error }) => {
  const [detailedDescription, setDetailedDescription] = useState(draft.detailed_description || '');
  const [generating, setGenerating] = useState(false);

  const handleSave = async () => {
    await updateDraft({ detailed_description: detailedDescription });
  };

  const handleGenerateWithAI = async () => {
    setGenerating(true);
    try {
      const response = await draftApi.generateSection(draft.id, 'detailed_description');
      if (response.success && response.data) {
        setDetailedDescription(response.data.content);
      }
    } catch (error) {
      console.error('Failed to generate detailed description:', error);
    }
    setGenerating(false);
  };

  return (
    <div className="step-container">
      <div className="row">
        <div className="col-12">
          <h2 className="mb-4">
            <i className="fas fa-cogs text-primary me-2"></i>
            Step 4: Detailed Description
          </h2>
          
          <div className="alert alert-info">
            <h5><i className="fas fa-info-circle me-2"></i>Detailed Description</h5>
            <p className="mb-0">
              Provide a comprehensive technical description of your invention, including how it works and its components.
            </p>
          </div>

          <div className="mb-3">
            <label htmlFor="detailedDescription" className="form-label">
              <strong>Detailed Description of the Invention</strong>
            </label>
            <textarea
              className="form-control"
              id="detailedDescription"
              rows={15}
              value={detailedDescription}
              onChange={(e) => setDetailedDescription(e.target.value)}
              placeholder="Provide a detailed technical description of your invention, including components, operation, and implementation..."
            ></textarea>
            <div className="form-text">
              Include technical details, component descriptions, operation procedures, and implementation specifics.
            </div>
          </div>

          <div className="d-flex justify-content-between mt-4">
            <button
              type="button"
              className="btn btn-outline-primary"
              onClick={handleGenerateWithAI}
              disabled={generating}
            >
              {generating ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                  Generating...
                </>
              ) : (
                <>
                  <i className="fas fa-magic me-2"></i>
                  Generate with AI
                </>
              )}
            </button>
            
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleSave}
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

export default Step4DetailedDescription; 