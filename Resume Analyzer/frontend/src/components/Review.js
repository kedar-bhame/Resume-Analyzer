import React, {useState, useRef} from 'react';
import {Doughnut} from 'react-chartjs-2';
import ATSBreakdown from './ATSBreakdown';
import Footer from './Footer';

export default function Review(){
  const [analysis, setAnalysis] = useState(null);
  const [messages, setMessages] = useState([{type:'system', text:'Upload a resume to begin.'}]);
  const fileRef = useRef();

  async function upload(){
    const f = fileRef.current.files[0]; if(!f) return alert('Choose file');
    const fd = new FormData(); fd.append('file', f);
    const res = await fetch('/api/upload', {method:'POST', body:fd});
    const j = await res.json(); setAnalysis(j); setMessages(m=>[...m,{type:'system',text:'Analysis complete: '+j.score}]);
  }

  async function sendChat(msg){
    setMessages(m=>[...m,{type:'user',text:msg}]);
    const res = await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body: JSON.stringify({message:msg, analysis})});
    const j = await res.json(); setMessages(m=>[...m,{type:'system',text:j.response}]);
  }

  const data = analysis ? {
    datasets:[{data:[analysis.score_breakdown.contact_email?15:0, analysis.score_breakdown.contact_phone?10:0, analysis.score_breakdown.skill_points||0, analysis.score_breakdown.experience_points||0, analysis.score_breakdown.education_present?10:0, analysis.score_breakdown.projects_present?10:0], backgroundColor:['#4ade80','#60a5fa','#f59e0b','#f97316','#a78bfa','#34d399']}],
    labels:['Email','Phone','Skills','Experience','Education','Projects']
  }: null;

  return (
    <div className="page-wrapper">
      {/* Upload Section */}
      <div className="section-container">
        <div className="card upload-card">
          <div className="section-header">
            <h2>📤 Upload Your Resume</h2>
            <p>Supported formats: PDF, DOCX, DOC, TXT, RTF, ODT</p>
          </div>
          <div className="upload-area">
            <input ref={fileRef} type="file" accept=".pdf,.doc,.docx,.txt" className="file-input" />
            <button className="btn primary btn-lg" onClick={upload}>Upload & Analyze</button>
          </div>
        </div>
      </div>

      {/* Results and Chat Section */}
      {analysis ? (
        <div className="section-container">
          <div className="results-chat-layout">
            {/* Results Column */}
            <div className="results-column">
              {/* Analysis Card */}
              <div className="card analysis-card">
                <div className="section-header">
                  <h2>📊 Analysis Results</h2>
                  <p>Your resume score and summary</p>
                </div>
                <div className="analysis-content">
                  <p className="summary-text">{analysis.human_summary}</p>
                  <div className="score-display">
                    <div className="score-chart">
                      <Doughnut data={data} />
                    </div>
                    <div className="score-info">
                      <div className="score-number">{analysis.score}/100</div>
                      <div className="score-recommendation">{analysis.suggestions && analysis.suggestions[0]}</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* ATS Breakdown Card */}
              <div className="card ats-card">
                <ATSBreakdown analysis={analysis} />
              </div>

              {/* Suggestions Card */}
              <div className="card suggestions-card">
                <div className="section-header">
                  <h2>💡 Improvement Suggestions</h2>
                </div>
                <div className="suggestions-list">
                  {analysis.suggestions && analysis.suggestions.map((suggestion, idx) => (
                    <div key={idx} className="suggestion-item">
                      <span className="suggestion-icon">→</span>
                      <span>{suggestion}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Templates Preview Card */}
              <div className="card templates-preview-card">
                <div className="section-header">
                  <h2>📋 Resume Templates</h2>
                  <p>Use our professional templates</p>
                </div>
                <p>Download one of our 5 professionally designed templates to improve your resume.</p>
                <a className="btn primary btn-block" href="/templates">Browse All Templates →</a>
              </div>
            </div>

            {/* Chat Column */}
            <div className="chat-column">
              <div className="card chat-card">
                <div className="section-header">
                  <h2>🤖 AI Assistant</h2>
                  <p>Ask questions about your resume</p>
                </div>
                <div className="chatbox">
                  <div className="msgs">
                    {messages.map((m,i)=>(<div key={i} className={m.type==='user'?'bubble user':'bubble system'}>{m.text}</div>))}
                  </div>
                  <ChatInput onSend={sendChat} />
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="section-container">
          <div className="card welcome-card">
            <div className="welcome-content">
              <h2>⬆️ Start by uploading your resume</h2>
              <p>Upload your resume above to get started with our AI-powered analysis.</p>
            </div>
          </div>
        </div>
      )}

      <Footer />
    </div>
  );
}

function ChatInput({onSend}){
  const [v,setV] = useState('');
  return (
    <div style={{display:'flex',gap:8}}>
      <input value={v} onChange={e=>setV(e.target.value)} style={{flex:1}} placeholder="Ask the assistant" />
      <button className="btn" onClick={()=>{onSend(v); setV('');}}>Send</button>
    </div>
  );
}
