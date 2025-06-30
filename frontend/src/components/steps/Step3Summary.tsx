import React, { useState } from 'react';
import { Draft, DraftUpdateData } from '../../types/draft';
import { draftApi } from '../../services/api';

interface Step3Props {
  draft: Draft;
  updateDraft: (data: DraftUpdateData) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const Step3Summary: React.FC<Step3Props> = ({ draft, updateDraft, loading, error }) => {
  const [summary, setSummary] = useState(draft.summary || '');
  const [generating, setGenerating] = useState(false);

  const handleSave = async () => {
    await updateDraft({ summary });
  };

  const handleGenerateWithAI = async () => {
    setGenerating(true);
    try {
      const response = await draftApi.generateSection(draft.id, 'summary');
      if (response.success && response.data) {
        setSummary(response.data.content);
      }
    } catch (error) {
      console.error('Failed to generate summary:', error);
    }
    setGenerating(false);
  };

  return (
    <div className="step-container">
      <div className="row">
        <div className="col-12">
          <h2 className="mb-4">
            <i className="fas fa-file-text text-primary me-2"></i>
            Step 3: Summary of the Invention
          </h2>
          
          <div className="alert alert-info">
            <h5><i className="fas fa-info-circle me-2"></i>Summary Section</h5>
            <p className="mb-0">
              Provide a concise overview of your invention, its key features, and benefits.
            </p>
          </div>

          <div className="mb-3">
            <label htmlFor="summary" className="form-label">
              <strong>Summary of the Invention</strong>
            </label>
            <textarea
              className="form-control"
              id="summary"
              rows={8}
              value={summary}
              onChange={(e) => setSummary(e.target.value)}
              placeholder="Provide a brief overview of your invention, its main features, and advantages..."
            ></textarea>
            <div className="form-text">
              Summarize the key aspects of your invention in clear, concise language.
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

export default Step3Summary; 