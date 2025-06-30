import React, { useState } from 'react';
import { Draft, DraftUpdateData } from '../../types/draft';
import { draftApi } from '../../services/api';

interface Step7Props {
  draft: Draft;
  updateDraft: (data: DraftUpdateData) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const Step7Abstract: React.FC<Step7Props> = ({ draft, updateDraft, loading, error }) => {
  const [abstract, setAbstract] = useState(draft.abstract || '');
  const [generating, setGenerating] = useState(false);

  const handleSave = async () => {
    await updateDraft({ abstract });
  };

  const handleGenerateWithAI = async () => {
    setGenerating(true);
    try {
      const response = await draftApi.generateSection(draft.id, 'abstract');
      if (response.success && response.data) {
        setAbstract(response.data.content);
      }
    } catch (error) {
      console.error('Failed to generate abstract:', error);
    }
    setGenerating(false);
  };

  return (
    <div className="step-container">
      <div className="row">
        <div className="col-12">
          <h2 className="mb-4">
            <i className="fas fa-file-alt text-primary me-2"></i>
            Step 7: Abstract
          </h2>
          
          <div className="alert alert-info">
            <h5><i className="fas fa-info-circle me-2"></i>Abstract Section</h5>
            <p className="mb-0">
              Write a concise abstract that summarizes your invention in 150 words or less.
            </p>
          </div>

          <div className="mb-3">
            <label htmlFor="abstract" className="form-label">
              <strong>Abstract</strong>
            </label>
            <textarea
              className="form-control"
              id="abstract"
              rows={6}
              value={abstract}
              onChange={(e) => setAbstract(e.target.value)}
              placeholder="Provide a brief summary of your invention, its key features, and benefits..."
              maxLength={150}
            ></textarea>
            <div className="form-text">
              Maximum 150 words. This should be a clear, concise summary of your invention.
            </div>
            <div className="form-text">
              Characters: {abstract.length}/150
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

export default Step7Abstract;
