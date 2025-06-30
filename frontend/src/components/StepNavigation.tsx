import React from 'react';
import { Draft } from '../types/draft';

interface StepNavigationProps {
  currentStep: number;
  onStepClick: (step: number) => void;
  draft: Draft | null;
}

const StepNavigation: React.FC<StepNavigationProps> = ({ currentStep, onStepClick, draft }) => {
  const steps = [
    { id: 1, title: 'Initial Questions', icon: 'fa-question-circle', description: 'Basic invention details' },
    { id: 2, title: 'Background', icon: 'fa-book', description: 'Prior art and context' },
    { id: 3, title: 'Summary', icon: 'fa-file-text', description: 'Brief overview' },
    { id: 4, title: 'Detailed Description', icon: 'fa-cogs', description: 'Technical specifications' },
    { id: 5, title: 'Claims', icon: 'fa-gavel', description: 'Legal protection scope' },
    { id: 6, title: 'Drawings', icon: 'fa-image', description: 'Visual representations' },
    { id: 7, title: 'Abstract', icon: 'fa-file-alt', description: 'Executive summary' },
    { id: 8, title: 'Preview & Download', icon: 'fa-download', description: 'Final review' }
  ];

  const isStepCompleted = (stepId: number) => {
    if (!draft) return false;
    
    switch (stepId) {
      case 1:
        return !!(draft.title && draft.field_of_invention && draft.brief_summary);
      case 2:
        return !!draft.background;
      case 3:
        return !!draft.summary;
      case 4:
        return !!draft.detailed_description;
      case 5:
        return !!draft.claims;
      case 6:
        return true; // Always accessible
      case 7:
        return !!draft.abstract;
      case 8:
        return true; // Always accessible
      default:
        return false;
    }
  };

  return (
    <nav className="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
      <div className="position-sticky pt-3">
        <ul className="nav flex-column">
          <li className="nav-item">
            <h6 className="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
              <span>Drafting Steps</span>
            </h6>
          </li>
          {steps.map((step) => {
            const isActive = currentStep === step.id;
            const isCompleted = isStepCompleted(step.id);
            const isAccessible = step.id <= currentStep || isCompleted;
            
            return (
              <li key={step.id} className="nav-item">
                <button
                  className={`nav-link ${isActive ? 'active' : ''} ${!isAccessible ? 'disabled' : ''}`}
                  onClick={() => isAccessible && onStepClick(step.id)}
                  disabled={!isAccessible}
                  style={{ textAlign: 'left', border: 'none', background: 'none', width: '100%' }}
                >
                  <div className="d-flex align-items-center">
                    <i className={`fas ${step.icon} me-2 ${isCompleted ? 'text-success' : isActive ? 'text-primary' : 'text-muted'}`}></i>
                    <div className="flex-grow-1">
                      <div className={`fw-bold ${isActive ? 'text-primary' : ''}`}>
                        {step.id}. {step.title}
                      </div>
                      <small className="text-muted">{step.description}</small>
                    </div>
                    {isCompleted && (
                      <i className="fas fa-check-circle text-success ms-2"></i>
                    )}
                  </div>
                </button>
              </li>
            );
          })}
        </ul>
        
        {draft && (
          <div className="mt-4 p-3">
            <h6 className="text-muted">Progress</h6>
            <div className="progress mb-2">
              <div 
                className="progress-bar" 
                role="progressbar" 
                style={{ width: `${(currentStep / 8) * 100}%` }}
                aria-valuenow={currentStep} 
                aria-valuemin={0} 
                aria-valuemax={8}
              ></div>
            </div>
            <small className="text-muted">
              Step {currentStep} of 8
            </small>
          </div>
        )}
      </div>
    </nav>
  );
};

export default StepNavigation; 