import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import DraftingWizard from './components/DraftingWizard';
import 'bootstrap/dist/css/bootstrap.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
          <div className="container">
            <Link className="navbar-brand" to="/">
              <i className="fas fa-lightbulb me-2"></i>
              Patent Drafting Assistant
            </Link>
            <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/">
                    <i className="fas fa-home me-1"></i>
                    Home
                  </Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/drafting">
                    <i className="fas fa-edit me-1"></i>
                    Start New Draft
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/drafting" element={<DraftingWizard />} />
          <Route path="/drafting/:draftId" element={<DraftingWizard />} />
        </Routes>
      </div>
    </Router>
  );
}

const HomePage: React.FC = () => {
  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-lg-8 text-center">
          <h1 className="display-4 mb-4">
            <i className="fas fa-lightbulb text-primary me-3"></i>
            AI-Powered Patent Drafting
          </h1>
          <p className="lead mb-4">
            Create professional patent specifications with the help of artificial intelligence. 
            Our step-by-step wizard guides you through the entire process.
          </p>
          
          <div className="row mb-5">
            <div className="col-md-4 mb-3">
              <div className="card h-100">
                <div className="card-body text-center">
                  <i className="fas fa-robot text-primary fa-3x mb-3"></i>
                  <h5 className="card-title">AI Assistance</h5>
                  <p className="card-text">Generate content with advanced AI technology</p>
                </div>
              </div>
            </div>
            <div className="col-md-4 mb-3">
              <div className="card h-100">
                <div className="card-body text-center">
                  <i className="fas fa-file-word text-primary fa-3x mb-3"></i>
                  <h5 className="card-title">DOCX Export</h5>
                  <p className="card-text">Download your patent as a professional document</p>
                </div>
              </div>
            </div>
            <div className="col-md-4 mb-3">
              <div className="card h-100">
                <div className="card-body text-center">
                  <i className="fas fa-shield-alt text-primary fa-3x mb-3"></i>
                  <h5 className="card-title">Secure Storage</h5>
                  <p className="card-text">Your drafts are safely stored in the cloud</p>
                </div>
              </div>
            </div>
          </div>

          <Link to="/drafting" className="btn btn-primary btn-lg">
            <i className="fas fa-plus me-2"></i>
            Start New Patent Draft
          </Link>
        </div>
      </div>
    </div>
  );
};

export default App;
