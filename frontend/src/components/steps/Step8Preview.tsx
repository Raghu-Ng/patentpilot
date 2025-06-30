import React, { useState } from 'react';
import { Draft } from '../../types/draft';
import { draftApi } from '../../services/api';

interface Step8Props {
  draft: Draft;
  updateDraft: (data: any) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const Step8Preview: React.FC<Step8Props> = ({ draft, updateDraft, loading, error }) => {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const blob = await draftApi.downloadDraft(draft.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `patent_application_${draft.title.replace(/\s+/g, '_')}.docx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Failed to download draft:', error);
    }
    setDownloading(false);
  };

  const handleComplete = async () => {
    await updateDraft({ is_complete: true });
  };

  return (
    <div className="step-container">
      <div className="row">
        <div className="col-12">
          <h2 className="mb-4">
            <i className="fas fa-download text-primary me-2"></i>
            Step 8: Preview & Download
          </h2>
          
          <div className="alert alert-success">
            <h5><i className="fas fa-check-circle me-2"></i>Congratulations!</h5>
            <p className="mb-0">
              You've completed your patent specification. Review the content below and download your document.
            </p>
          </div>

          {/* Preview Section */}
          <div className="card mb-4">
            <div className="card-header">
              <h5 className="mb-0">Patent Specification Preview</h5>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-6">
                  <h6>Basic Information</h6>
                  <p><strong>Title:</strong> {draft.title || 'Not provided'}</p>
                  <p><strong>Field:</strong> {draft.field_of_invention || 'Not provided'}</p>
                  <p><strong>Problem Solved:</strong> {draft.problem_solved || 'Not provided'}</p>
                </div>
                <div className="col-md-6">
                  <h6>Completion Status</h6>
                  <div className="mb-2">
                    <span className={`badge ${draft.title ? 'bg-success' : 'bg-warning'} me-2`}>
                      {draft.title ? '✓' : '○'} Title
                    </span>
                    <span className={`badge ${draft.background ? 'bg-success' : 'bg-warning'} me-2`}>
                      {draft.background ? '✓' : '○'} Background
                    </span>
                    <span className={`badge ${draft.summary ? 'bg-success' : 'bg-warning'} me-2`}>
                      {draft.summary ? '✓' : '○'} Summary
                    </span>
                  </div>
                  <div className="mb-2">
                    <span className={`badge ${draft.detailed_description ? 'bg-success' : 'bg-warning'} me-2`}>
                      {draft.detailed_description ? '✓' : '○'} Description
                    </span>
                    <span className={`badge ${draft.claims ? 'bg-success' : 'bg-warning'} me-2`}>
                      {draft.claims ? '✓' : '○'} Claims
                    </span>
                    <span className={`badge ${draft.abstract ? 'bg-success' : 'bg-warning'} me-2`}>
                      {draft.abstract ? '✓' : '○'} Abstract
                    </span>
                  </div>
                </div>
              </div>

              <hr />

              <div className="row">
                <div className="col-12">
                  <h6>Content Preview</h6>
                  <div className="accordion" id="previewAccordion">
                    {draft.background && (
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#backgroundPreview">
                            Background
                          </button>
                        </h2>
                        <div id="backgroundPreview" className="accordion-collapse collapse" data-bs-parent="#previewAccordion">
                          <div className="accordion-body">
                            <p>{draft.background.substring(0, 200)}...</p>
                          </div>
                        </div>
                      </div>
                    )}

                    {draft.summary && (
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#summaryPreview">
                            Summary
                          </button>
                        </h2>
                        <div id="summaryPreview" className="accordion-collapse collapse" data-bs-parent="#previewAccordion">
                          <div className="accordion-body">
                            <p>{draft.summary}</p>
                          </div>
                        </div>
                      </div>
                    )}

                    {draft.claims && (
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#claimsPreview">
                            Claims
                          </button>
                        </h2>
                        <div id="claimsPreview" className="accordion-collapse collapse" data-bs-parent="#previewAccordion">
                          <div className="accordion-body">
                            <pre style={{ whiteSpace: 'pre-wrap' }}>{draft.claims}</pre>
                          </div>
                        </div>
                      </div>
                    )}

                    {draft.abstract && (
                      <div className="accordion-item">
                        <h2 className="accordion-header">
                          <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#abstractPreview">
                            Abstract
                          </button>
                        </h2>
                        <div id="abstractPreview" className="accordion-collapse collapse" data-bs-parent="#previewAccordion">
                          <div className="accordion-body">
                            <p>{draft.abstract}</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="d-flex justify-content-between mt-4">
            <button
              type="button"
              className="btn btn-outline-primary"
              onClick={() => window.print()}
            >
              <i className="fas fa-print me-2"></i>
              Print Preview
            </button>
            
            <div>
              <button
                type="button"
                className="btn btn-success me-2"
                onClick={handleDownload}
                disabled={downloading}
              >
                {downloading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                    Downloading...
                  </>
                ) : (
                  <>
                    <i className="fas fa-download me-2"></i>
                    Download DOCX
                  </>
                )}
              </button>
              
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleComplete}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                    Completing...
                  </>
                ) : (
                  <>
                    <i className="fas fa-check me-2"></i>
                    Mark Complete
                  </>
                )}
              </button>
            </div>
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

export default Step8Preview;
