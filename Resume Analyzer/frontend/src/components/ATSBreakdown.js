import React, { useState } from 'react';

export default function ATSBreakdown({ analysis }) {
  const [expanded, setExpanded] = useState(true);

  if (!analysis || !analysis.score_details) return null;

  const details = analysis.score_details;
  const categories = ['email', 'phone', 'skills', 'experience', 'education', 'projects'];

  return (
    <div className="ats-breakdown">
      <div className="breakdown-header" onClick={() => setExpanded(!expanded)}>
        <h4>ATS Score Breakdown</h4>
        <span className="expand-icon">{expanded ? '▼' : '▶'}</span>
      </div>

      {expanded && (
        <div className="breakdown-content">
          <p className="breakdown-intro">
            Your resume is scored out of 100 based on ATS (Applicant Tracking System) compatibility factors:
          </p>

          <div className="breakdown-items">
            {categories.map((key) => {
              const item = details[key];
              const percentage = (item.points / item.max) * 100;
              return (
                <div key={key} className="breakdown-item">
                  <div className="item-header">
                    <span className="item-label">{item.label}</span>
                    <span className={`item-status status-${item.points > 0 ? 'complete' : 'missing'}`}>
                      {item.status}
                    </span>
                  </div>
                  <div className="item-bar">
                    <div 
                      className="item-progress" 
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                  <div className="item-score">
                    {item.points}/{item.max} points
                  </div>
                  <p className="item-explanation">{item.explanation}</p>
                </div>
              );
            })}
          </div>

          <div className="breakdown-total">
            <strong>Total Score: {analysis.score}/100</strong>
            <p className="score-rating">
              {analysis.score >= 80 && "Excellent - Your resume is highly ATS-optimized"}
              {analysis.score >= 60 && analysis.score < 80 && "Good - Your resume has solid ATS compatibility"}
              {analysis.score >= 40 && analysis.score < 60 && "Fair - Consider adding more details to improve ATS scores"}
              {analysis.score < 40 && "Needs Improvement - Add missing elements like email, phone, and skills"}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
