import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Draft, DraftFormData, DraftUpdateData } from '../types/draft';
import { draftApi } from '../services/api';
import Step1InitialQuestions from './steps/Step1InitialQuestions';
import Step2Background from './steps/Step2Background';
import Step3Summary from './steps/Step3Summary';
import Step4DetailedDescription from './steps/Step4DetailedDescription';
import Step5Claims from './steps/Step5Claims';
import Step6Drawings from './steps/Step6Drawings';
import Step7Abstract from './steps/Step7Abstract';
import Step8Preview from './steps/Step8Preview';
import StepNavigation from './StepNavigation';
import 'bootstrap/dist/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import './DraftingWizard.css';

const DraftingWizard: React.FC = () => {
  const { draftId } = useParams<{ draftId: string }>();
  const navigate = useNavigate();
  
  const [draft, setDraft] = useState<Draft | null>(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (draftId) {
      loadDraft(draftId);
    } else {
      startNewDraft();
    }
  }, [draftId]);

  const loadDraft = async (id: string) => {
    setLoading(true);
    setError(null);
    
    const response = await draftApi.getDraft(id);
    if (response.success && response.data) {
      setDraft(response.data);
      setCurrentStep(response.data.current_step);
    } else {
      setError(response.error || 'Failed to load draft');
    }
    setLoading(false);
  };

  const startNewDraft = async () => {
    setLoading(true);
    setError(null);
    
    const formData: DraftFormData = {
      user_id: 'default_user',
      project_title: 'New Patent Project',
      project_description: '',
      title: '',
      field_of_invention: '',
      brief_summary: '',
      key_components: '',
      problem_solved: ''
    };

    const response = await draftApi.startDraft(formData);
    if (response.success && response.data) {
      const newDraftId = response.data.draft_id;
      navigate(`/drafting/${newDraftId}`);
    } else {
      setError(response.error || 'Failed to start new draft');
    }
    setLoading(false);
  };

  const updateDraft = async (data: DraftUpdateData) => {
    if (!draft) return;
    
    setSaving(true);
    const response = await draftApi.updateDraft(draft.id, data);
    if (response.success && response.data) {
      setDraft(response.data);
    } else {
      setError(response.error || 'Failed to save draft');
    }
    setSaving(false);
  };

  const goToStep = (step: number) => {
    if (step >= 1 && step <= 8) {
      setCurrentStep(step);
      if (draft) {
        updateDraft({ current_step: step });
      }
    }
  };

  const nextStep = () => {
    if (currentStep < 8) {
      goToStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      goToStep(currentStep - 1);
    }
  };

  const renderStep = () => {
    if (!draft) return null;

    const stepProps = {
      draft,
      updateDraft,
      loading,
      error
    };

    switch (currentStep) {
      case 1:
        return <Step1InitialQuestions {...stepProps} />;
      case 2:
        return <Step2Background {...stepProps} />;
      case 3:
        return <Step3Summary {...stepProps} />;
      case 4:
        return <Step4DetailedDescription {...stepProps} />;
      case 5:
        return <Step5Claims {...stepProps} />;
      case 6:
        return <Step6Drawings {...stepProps} />;
      case 7:
        return <Step7Abstract {...stepProps} />;
      case 8:
        return <Step8Preview {...stepProps} />;
      default:
        return <div>Invalid step</div>;
    }
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: '100vh' }}>
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger m-3" role="alert">
        <h4 className="alert-heading">Error</h4>
        <p>{error}</p>
        <button className="btn btn-primary" onClick={() => window.location.reload()}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="drafting-wizard">
      <div className="container-fluid">
        <div className="row">
          {/* Sidebar */}
          <div className="col-md-3 col-lg-2 d-md-block bg-light sidebar">
            <StepNavigation 
              currentStep={currentStep}
              onStepClick={goToStep}
              draft={draft}
            />
          </div>
          
          {/* Main Content */}
          <div className="col-md-9 ms-sm-auto col-lg-10 px-md-4">
            <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
              <h1 className="h2">AI-Powered Patent Drafting</h1>
              <div className="btn-toolbar mb-2 mb-md-0">
                <div className="btn-group me-2">
                  <button 
                    type="button" 
                    className="btn btn-sm btn-outline-secondary"
                    onClick={() => updateDraft({})}
                    disabled={saving}
                  >
                    {saving ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        Saving...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-save"></i> Save Progress
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
            
            {/* Step Content */}
            <div className="step-content">
              {renderStep()}
            </div>
            
            {/* Navigation Buttons */}
            <div className="d-flex justify-content-between mt-4">
              <button 
                type="button" 
                className="btn btn-secondary" 
                onClick={prevStep}
                disabled={currentStep === 1}
              >
                <i className="fas fa-arrow-left"></i> Previous
              </button>
              <button 
                type="button" 
                className="btn btn-primary" 
                onClick={nextStep}
                disabled={currentStep === 8}
              >
                {currentStep === 8 ? 'Complete' : 'Next'} <i className="fas fa-arrow-right"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DraftingWizard; 