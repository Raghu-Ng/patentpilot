import React, { useState, useEffect } from 'react';
import { Draft, Drawing } from '../../types/draft';
import { draftApi } from '../../services/api';

interface Step6Props {
  draft: Draft;
  updateDraft: (data: any) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const Step6Drawings: React.FC<Step6Props> = ({ draft, updateDraft, loading, error }) => {
  const [drawings, setDrawings] = useState<Drawing[]>([]);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [description, setDescription] = useState('');

  useEffect(() => {
    loadDrawings();
  }, [draft.id]);

  const loadDrawings = async () => {
    try {
      const response = await draftApi.getDrawings(draft.id);
      if (response.success && response.data) {
        setDrawings(response.data);
      }
    } catch (error) {
      console.error('Failed to load drawings:', error);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    try {
      const response = await draftApi.uploadDrawing(draft.id, selectedFile, description);
      if (response.success && response.data) {
        setDrawings(prev => [...prev, response.data!]);
        setSelectedFile(null);
        setDescription('');
        // Reset file input
        const fileInput = document.getElementById('drawingFile') as HTMLInputElement;
        if (fileInput) fileInput.value = '';
      }
    } catch (error) {
      console.error('Failed to upload drawing:', error);
    }
    setUploading(false);
  };

  const handleSave = async () => {
    await updateDraft({});
  };

  return (
    <div className="step-container">
      <div className="row">
        <div className="col-12">
          <h2 className="mb-4">
            <i className="fas fa-image text-primary me-2"></i>
            Step 6: Drawings
          </h2>
          
          <div className="alert alert-info">
            <h5><i className="fas fa-info-circle me-2"></i>Drawings Section</h5>
            <p className="mb-0">
              Upload drawings, diagrams, or schematics that illustrate your invention. These help explain the technical aspects of your invention.
            </p>
          </div>

          {/* Upload Section */}
          <div className="card mb-4">
            <div className="card-header">
              <h5 className="mb-0">Upload New Drawing</h5>
            </div>
            <div className="card-body">
              <div className="row">
                <div className="col-md-6 mb-3">
                  <label htmlFor="drawingFile" className="form-label">
                    <strong>Select File</strong>
                  </label>
                  <input
                    type="file"
                    className="form-control"
                    id="drawingFile"
                    accept="image/*,.pdf"
                    onChange={handleFileSelect}
                  />
                  <div className="form-text">
                    Supported formats: JPG, PNG, GIF, PDF (max 10MB)
                  </div>
                </div>
                <div className="col-md-6 mb-3">
                  <label htmlFor="description" className="form-label">
                    <strong>Description (Optional)</strong>
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    id="description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    placeholder="Brief description of the drawing..."
                  />
                </div>
              </div>
              <button
                type="button"
                className="btn btn-primary"
                onClick={handleUpload}
                disabled={!selectedFile || uploading}
              >
                {uploading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                    Uploading...
                  </>
                ) : (
                  <>
                    <i className="fas fa-upload me-2"></i>
                    Upload Drawing
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Drawings List */}
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Uploaded Drawings ({drawings.length})</h5>
            </div>
            <div className="card-body">
              {drawings.length === 0 ? (
                <p className="text-muted">No drawings uploaded yet.</p>
              ) : (
                <div className="row">
                  {drawings.map((drawing) => (
                    <div key={drawing.id} className="col-md-4 mb-3">
                      <div className="card">
                        <div className="card-body">
                          <h6 className="card-title">{drawing.original_filename}</h6>
                          {drawing.description && (
                            <p className="card-text small text-muted">{drawing.description}</p>
                          )}
                          <p className="card-text small">
                            Size: {(drawing.file_size / 1024).toFixed(1)} KB
                          </p>
                          <button
                            type="button"
                            className="btn btn-sm btn-outline-primary"
                            onClick={() => window.open(`/drafts/${draft.id}/drawings/${drawing.id}`, '_blank')}
                          >
                            <i className="fas fa-eye me-1"></i>
                            View
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="d-flex justify-content-end mt-4">
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

export default Step6Drawings; 