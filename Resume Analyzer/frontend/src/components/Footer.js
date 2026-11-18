import React from 'react';

export default function Footer() {
  return (
    <footer className="footer-section">
      <div className="footer-content">
        <p className="developed-text">
          Developed By
        </p>
        <div className="developers-container">
          <span className="developer-name dev-1">Avishkar Kulkarni</span>
          <span className="separator">•</span>
          <span className="developer-name dev-2">Krishna Kulkarni</span>
          <span className="separator">•</span>
          <span className="developer-name dev-3">Rushikesh Joshi</span>
        </div>
      </div>
      <div className="footer-divider"></div>
    </footer>
  );
}
