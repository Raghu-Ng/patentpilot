import React, { useState } from 'react';
import { Draft, DraftUpdateData } from '../../types/draft';
import { draftApi } from '../../services/api';

interface Step5Props {
  draft: Draft;
  updateDraft: (data: DraftUpdateData) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const Step5Claims: React.FC<Step5Props> = ({ draft, updateDraft, loading, error }) => {
  const [claims, setClaims] = useState(draft.claims || '');
  const [generating, setGenerating] = useState(false);

  const handleSave = async () => {
    await updateDraft({ claims });
  };

  const handleGenerateWithAI = async () => {
    setGenerating(true);
    try {
      const response = await draftApi.generateSection(draft.id, 'claims');
      if (response.success && response.data) {
        setClaims(response.data.content);
      }
    } catch (error) {
      console.error('Failed to generate claims:', error);
    }
    setGenerating(false);
  };

  return (
    <div className="step-container">
      <div className="row">
        <div className="col-12">
          <h2 className="mb-4">
            <i className="fas fa-gavel text-primary me-2"></i>
            Step 5: Claims
          </h2>
          
          <div className="alert alert-warning">
            <h5><i className="fas fa-exclamation-triangle me-2"></i>Important: Claims Section</h5>
            <p className="mb-0">
              Claims define the legal scope of your patent protection. They should be carefully drafted to cover your invention while avoiding prior art.
            </p>
          </div>

          <div className="mb-3">
            <label htmlFor="claims" className="form-label">
              <strong>Patent Claims</strong>
            </label>
            <textarea
              className="form-control"
              id="claims"
              rows={12}
              value={claims}
              onChange={(e) => setClaims(e.target.value)}
              placeholder="1. A [invention type] comprising: [list of elements]...&#10;&#10;2. The [invention type] of claim 1, further comprising: [additional elements]..."
            ></textarea>
            <div className="form-text">
              Each claim should be numbered and clearly define the scope of protection. Start with broad claims and add dependent claims for specific embodiments.
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

export default Step5Claims; 