import React, { useState, useEffect } from 'react';
import {Link, useNavigate} from 'react-router-dom';
import Footer from './components/Footer';

export default function App(){
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    navigate('/');
  };

  return (
    <div className="page-wrapper">
      <div className="hero">
        <div className="hero-content">
          <h1>AI-Powered Resume Analyzer</h1>
          <p>Get your resume scored, optimized, and ready for ATS systems in seconds</p>
          <div className="hero-buttons">
            <Link to="/review" className="btn primary btn-lg">🚀 Get Started</Link>
            <Link to="/templates" className="btn btn-lg">📋 View Templates</Link>
          </div>
        </div>
      </div>

      <div className="features-section">
        <div className="features-container">
          <h2>Why Use Resume Analyzer?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>ATS Score</h3>
              <p>Get an accurate score based on ATS system compatibility with detailed breakdown</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI Assistant</h3>
              <p>Chat with our AI to get personalized feedback and improvement suggestions</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📄</div>
              <h3>5 Templates</h3>
              <p>Download professional, ATS-optimized resume templates ready to use</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💡</div>
              <h3>Smart Suggestions</h3>
              <p>Receive context-aware recommendations to boost your resume score</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">✅</div>
              <h3>Multi-Format</h3>
              <p>Upload PDF, Word, DOC, TXT, RTF, or ODT files - we support them all</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔐</div>
              <h3>Secure & Private</h3>
              <p>Your resume data is processed securely and never shared externally</p>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
