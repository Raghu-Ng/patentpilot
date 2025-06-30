import React, { useState } from 'react';
import { Draft, DraftUpdateData } from '../../types/draft';
import { draftApi } from '../../services/api';

interface Step2Props {
  draft: Draft;
  updateDraft: (data: DraftUpdateData) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const Step2Background: React.FC<Step2Props> = ({ draft, updateDraft, loading, error }) => {
  const [background, setBackground] = useState(draft.background || '');
  const [generating, setGenerating] = useState(false);

  const handleSave = async () => {
    await updateDraft({ background });
  };

  const handleGenerateWithAI = async () => {
    setGenerating(true);
    try {
      const response = await draftApi.generateSection(draft.id, 'background');
      if (response.success && response.data) {
        setBackground(response.data.content);
      }
    } catch (error) {
      console.error('Failed to generate background:', error);
    }
    setGenerating(false);
  };

  const handleRephrase = async () => {
    const instruction = prompt('How would you like to rephrase the background section?');
    if (instruction) {
      setGenerating(true);
      try {
        const response = await draftApi.rephraseSection(draft.id, 'background', instruction);
        if (response.success && response.data) {
          setBackground(response.data.content);
        }
      } catch (error) {
        console.error('Failed to rephrase:', error);
      }
      setGenerating(false);
    }
  };

  return (
    <div className="step-container">
      <div className="row">
        <div className="col-12">
          <h2 className="mb-4">
            <i className="fas fa-book text-primary me-2"></i>
            Step 2: Background of the Invention
          </h2>
          
          <div className="alert alert-info">
            <h5><i className="fas fa-info-circle me-2"></i>Background Section</h5>
            <p className="mb-0">
              Describe the existing technology, prior art, and context that your invention builds upon or improves.
            </p>
          </div>

          <div className="mb-3">
            <label htmlFor="background" className="form-label">
              <strong>Background of the Invention</strong>
            </label>
            <textarea
              className="form-control"
              id="background"
              rows={12}
              value={background}
              onChange={(e) => setBackground(e.target.value)}
              placeholder="Describe the current state of technology, existing solutions, and the problems they have..."
            ></textarea>
            <div className="form-text">
              Include information about existing technology, prior art, and the context that makes your invention necessary.
            </div>
          </div>

          <div className="d-flex justify-content-between mt-4">
            <div>
              <button
                type="button"
                className="btn btn-outline-primary me-2"
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
                className="btn btn-outline-secondary"
                onClick={handleRephrase}
                disabled={generating || !background.trim()}
              >
                <i className="fas fa-edit me-2"></i>
                Rephrase
              </button>
            </div>
            
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

export default Step2Background; 