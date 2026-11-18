# Resume-aware chatbot that uses the resume analysis context to provide helpful feedback.
# This is rule-based and does not require any external API keys.

DEFAULT_FAQ = {
    'format': 'Use a clean, consistent format with clear section headings: Contact, Summary/Objective, Education, Experience, Projects, Skills, Certifications. Stick to 1 page if early-career.',
    'objective': 'Keep objective/summary short (1-2 lines). Focus on what you bring and the role you seek.',
    'skills': 'Group skills (Programming, Frameworks, Tools) and include proficiency or years of experience where possible.',
    'experience': 'Use achievement-oriented bullets with action verbs, quantify impact (percent, money, time) where possible.',
}


def _format_list(items):
    if not items:
        return 'None detected.'
    return '\n'.join('- ' + i for i in items[:10])


def chatbot_response(message: str, analysis: dict = None) -> str:
    m = (message or '').strip().lower()

    # If user asks a generic FAQ
    for k in DEFAULT_FAQ:
        if k in m:
            return DEFAULT_FAQ[k]

    # If user asks to verify or review resume
    if any(kw in m for kw in ['review', 'verify', 'analyze', 'check my resume', 'how is my resume', 'grade']):
        if not analysis:
            return "Please upload your resume first so I can analyze it and give feedback."
        score = analysis.get('score')
        summary = analysis.get('human_summary')
        suggestions = analysis.get('suggestions', [])
        breakdown = analysis.get('score_breakdown', {})
        resp = []
        resp.append(f"Overall score: {score}/100.")
        resp.append(summary)
        if suggestions:
            resp.append('Top suggestions:')
            resp.append(_format_list(suggestions))
        # Add targeted hints
        if not breakdown.get('contact_email'):
            resp.append('- Add a professional email (e.g., firstname.lastname@domain.com).')
        if not breakdown.get('contact_phone'):
            resp.append('- Add a contact phone number with country code.')
        if not analysis.get('skills_detected'):
            resp.append('- Create a Skills section and list relevant technologies and tools.')
        else:
            resp.append('- You can improve your Skills section by stating proficiency (e.g., Python — Advanced).')
        if not analysis.get('education'):
            resp.append('- Add Education details (degree, institution, year, CGPA/percentage if strong).')
        if not analysis.get('projects'):
            resp.append('- Add 1-3 projects with bullets, technologies used, and impact.')
        return '\n'.join(resp)

    # If user requests skills detected
    if 'skills detected' in m or 'what skills' in m or 'list skills' in m:
        if not analysis:
            return 'Upload resume first to detect skills.'
        return 'Detected skills:\n' + _format_list(analysis.get('skills_detected', []))

    # If user asks for suggestions for a specific section
    if 'education' in m:
        if analysis and analysis.get('education'):
            return 'Education detected:\n' + _format_list(analysis.get('education')) + "\nTip: include degree, institution, year, and any notable coursework or percentage."
        return 'No education entries detected. Add degree, institute, year and notable achievements.'

    if 'projects' in m:
        if analysis and analysis.get('projects'):
            return 'Projects detected (sample lines):\n' + _format_list(analysis.get('projects')) + "\nTip: for each project, add 2-4 bullet points focusing on your contribution and impact."
        return 'No projects detected. Add 1-3 projects with concise bullets describing your role and results.'

    if 'email' in m or 'phone' in m or 'contact' in m:
        return 'Include a single contact block at the top with: Full name, professional email, phone number, and LinkedIn/GitHub links (optional).'

    # Fallback helpful response
    return "I can review your resume, list detected skills, and give targeted suggestions. Try: 'Review my resume', 'What skills are detected?', or ask about a section like 'Education' or 'Projects'."
