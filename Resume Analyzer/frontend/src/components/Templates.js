import React from 'react';
import Footer from './Footer';

export default function Templates(){
  const list = [
    {name:'Minimal Clean Resume', path:'/templates/template_1_minimal_clean.docx', thumb:'📄', desc:'Simple, professional one-page format'},
    {name:'Professional Executive', path:'/templates/template_2_professional_executive.docx', thumb:'👔', desc:'Executive-level resume with detailed sections'},
    {name:'Creative Modern Design', path:'/templates/template_3_creative_modern.docx', thumb:'🎨', desc:'Modern design with attractive formatting'},
    {name:'Academic & Research CV', path:'/templates/template_4_academic_cv.docx', thumb:'🎓', desc:'Ideal for academics and researchers'},
    {name:'Technical Engineer Resume', path:'/templates/template_5_technical_engineer.docx', thumb:'💻', desc:'Tech-focused with skills emphasis'}
  ];
  
  return (
    <div className="page-wrapper">
      <div className="panel templates-panel">
        <div className="card">
          <h2 style={{marginTop: 0, color: '#cbd5e1'}}>Professional Resume Templates</h2>
          <p style={{color: '#94a3b8'}}>Download our curated templates below. Click any template to download as .docx file and edit in Microsoft Word or Google Docs.</p>
          
          <div className="templates-grid">
            {list.map((t,i)=>(
              <a key={i} className="template-card" href={t.path} download>
                <div className="template-icon">{t.thumb}</div>
                <h4 className="template-name">{t.name}</h4>
                <p className="template-desc">{t.desc}</p>
                <div className="template-action">Download →</div>
              </a>
            ))}
          </div>

          <div className="templates-tips">
            <h3>Tips for Using Templates:</h3>
            <ul>
              <li>✓ Customize all sections with your personal information</li>
              <li>✓ Keep formatting consistent throughout the document</li>
              <li>✓ Use ATS-friendly fonts (Arial, Calibri, Helvetica)</li>
              <li>✓ Save as PDF for final submission to ATS systems</li>
              <li>✓ Limit to 1-2 pages for most positions</li>
              <li>✓ Use quantifiable metrics for achievements</li>
              <li>✓ Add relevant keywords from job descriptions</li>
              <li>✓ Proofread carefully before submitting</li>
            </ul>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}
