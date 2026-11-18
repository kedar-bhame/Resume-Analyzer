import os
from pdfminer.high_level import extract_text
import docx2txt
import re
import zipfile

# Optional OCR and RTF helpers
try:
    from PIL import Image
    import pytesseract
except Exception:
    Image = None
    pytesseract = None

try:
    from striprtf.striprtf import rtf_to_text
except Exception:
    rtf_to_text = None

# Try to import spaCy optionally. If not available, analyzer will use heuristics.
try:
    import spacy
    _nlp = spacy.load('en_core_web_sm')
except Exception:
    _nlp = None

SKILL_KEYWORDS = ['python','java','c++','c','javascript','react','node','django','flask','sql','mongodb','excel','git','docker','aws']
DEGREE_KEYWORDS = ['bachelor','bsc','b.a.','ba','b.e','be','btech','b.tech','bachelor of','master','m.sc','msc','mtech','m.tech','mca','mba','master of']


def extract_text_from_file(path):
    _, ext = os.path.splitext(path.lower())
    ext = ext or ''
    # PDF
    if ext == '.pdf':
        return extract_text(path)
    # Word .docx / .doc (docx2txt may handle both)
    elif ext in ['.doc', '.docx']:
        try:
            return docx2txt.process(path)
        except Exception:
            pass
    # RTF
    elif ext == '.rtf':
        try:
            if rtf_to_text:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    raw = f.read()
                return rtf_to_text(raw)
            else:
                # crude fallback: strip RTF control words and braces
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    raw = f.read()
                text = re.sub(r'\\[a-zA-Z]+-?\d*\b', ' ', raw)
                text = re.sub(r'[{}]', ' ', text)
                text = re.sub(r'\s+', ' ', text)
                return text
        except Exception:
            return ''
    # OpenDocument Text (.odt) - try to read content.xml
    elif ext == '.odt':
        try:
            with zipfile.ZipFile(path) as z:
                data = z.read('content.xml').decode('utf-8', errors='ignore')
            # strip xml tags
            text = re.sub(r'<[^>]+>', ' ', data)
            text = re.sub(r'\s+', ' ', text)
            return text
        except Exception:
            return ''
    # Images - OCR if available
    elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
        if pytesseract and Image:
            try:
                img = Image.open(path)
                return pytesseract.image_to_string(img)
            except Exception:
                return ''
        return ''
    # Plain text
    elif ext in ['.txt']:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    # Fallback: try to decode bytes
    else:
        try:
            with open(path, 'rb') as f:
                raw = f.read()
            # try UTF-8 then latin-1
            try:
                return raw.decode('utf-8')
            except Exception:
                try:
                    return raw.decode('latin-1')
                except Exception:
                    return ''
        except Exception:
            return ''


def _guess_name(lines, email):
    # If spaCy is available, prefer PERSON entities near the top of the document.
    if _nlp:
        head = '\n'.join(lines[:8])
        doc = _nlp(head)
        for ent in doc.ents:
            if ent.label_ == 'PERSON':
                name = ent.text.strip()
                # avoid emails or headers
                low = re.sub(r'[^a-zA-Z\s]', '', name).strip().lower()
                headers = set(['education','experience','projects','skills','contact','objective','summary'])
                if low and all(h not in low for h in headers) and (email is None or email.split('@')[0] not in low):
                    return name
    # Heuristic fallback: name often appears in the first non-empty lines and is not a common section header
    headers = set(['education','experience','projects','skills','contact','objective','summary'])
    for i in range(min(6, len(lines))):
        line = lines[i].strip()
        if not line:
            continue
        low = re.sub(r'[^a-zA-Z\s]', '', line).strip().lower()
        if low and all(h not in low for h in headers) and (email is None or email.split('@')[0] not in low):
            # Check if it looks like a name (2-4 words, capitalized)
            parts = line.split()
            if 1 < len(parts) <= 4 and sum(1 for p in parts if p and p[0].isupper()) >= 1:
                return line
    return None


def _extract_education(full_text):
    edu_lines = []
    # If spaCy present, try to find ORG + DATE patterns near degree keywords
    if _nlp:
        doc = _nlp(full_text)
        for sent in doc.sents:
            s = sent.text.strip()
            low = s.lower()
            if any(d in low for d in DEGREE_KEYWORDS) or re.search(r'\b\d{4}\b', s):
                edu_lines.append(s)
        # dedupe
        return list(dict.fromkeys(edu_lines))

    for ln in full_text.splitlines():
        low = ln.lower()
        if any(d in low for d in DEGREE_KEYWORDS) or re.search(r'\b\d{4}\b', ln):
            edu_lines.append(ln.strip())
    return edu_lines


def _extract_sections(lines):
    sections = {}
    current = 'misc'
    buffer = []
    for ln in lines:
        l = ln.strip()
        key = None
        if re.match(r'^(education|experience|projects|skills|certifications|contact|objective|summary)\b', l.lower()):
            key = re.match(r'^(education|experience|projects|skills|certifications|contact|objective|summary)\b', l.lower()).group(1)
        if key:
            if buffer:
                sections.setdefault(current, []).extend(buffer)
            current = key
            buffer = []
            continue
        buffer.append(ln)
    if buffer:
        sections.setdefault(current, []).extend(buffer)
    return sections


def _parse_experience_section(exp_lines):
    # Return list of experience items with title, company, dates if possible
    items = []
    for ln in exp_lines:
        text = ln.strip()
        if not text:
            continue
        title = None; company = None; dates = None
        # try to split by at - common pattern: "Title at Company (2019-2021)"
        if ' at ' in text.lower():
            parts = re.split(r'\s+at\s+', text, flags=re.I)
            title = parts[0].strip()
            company = parts[1].strip() if len(parts)>1 else None
        # try to extract dates
        date_match = re.search(r'((?:19|20)\d{2})\s*[\-–to]{1,3}\s*((?:19|20)\d{2})', text)
        if date_match:
            dates = (int(date_match.group(1)), int(date_match.group(2)))
        else:
            # look for single year mentions
            y = re.search(r'\b(19|20)\d{2}\b', text)
            if y:
                dates = (int(y.group(0)),)
        items.append({'raw': text, 'title': title, 'company': company, 'dates': dates})
    return items


def analyze_resume(path):
    text = extract_text_from_file(path)
    if not text:
        return {'error': 'Unable to extract text from the uploaded resume.'}

    # Basic parsing
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    full_text = '\n'.join(lines)

    # Find email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", full_text)
    email = email_match.group(0) if email_match else None

    # Find phone (simple)
    phone_match = re.search(r"(\+?\d[\d\-\s]{7,}\d)", full_text)
    phone = phone_match.group(0) if phone_match else None

    # Experience detection (years) - improved: look for patterns like 'X years' or ranges
    exp_years = None
    m = re.search(r"(\d+(?:\.\d+)?)\s*(?:\+)?\s*(?:years|yrs)", full_text, re.I)
    if m:
        try:
            exp_years = float(m.group(1))
        except Exception:
            exp_years = None
    else:
        # Try to infer from dates (e.g., 2019 - 2022)
        years_all = [int(y) for y in re.findall(r"\b(19|20)\d{2}\b", full_text)]
        if years_all:
            if len(years_all) >= 2:
                exp_years = max(years_all) - min(years_all)

    # Skills
    found_skills = []
    for skill in SKILL_KEYWORDS:
        if re.search(r"\b"+re.escape(skill)+r"\b", full_text, re.I):
            found_skills.append(skill)

    # Sections
    sections = _extract_sections(lines)

    # Education / Projects / Experience lists
    education = _extract_education(full_text)
    projects = [ln for ln in lines if re.match(r'^(project|projects|project:)', ln.lower()) or 'project' in ln.lower()][:20]

    # Experience parsing
    experience_items = []
    if 'experience' in sections:
        experience_items = _parse_experience_section(sections.get('experience', []))
        # try to refine exp_years from parsed dates
        years = []
        for it in experience_items:
            if it.get('dates') and len(it['dates']) >= 2:
                years.append(it['dates'][1] - it['dates'][0])
        if years and not exp_years:
            exp_years = sum(years)

    # Guess name (spaCy preferred)
    name = _guess_name(lines, email)

    # Simple scoring breakdown
    score = 0
    details = {}

    if email:
        score += 15
        details['contact_email'] = True
    else:
        details['contact_email'] = False
    if phone:
        score += 10
        details['contact_phone'] = True
    else:
        details['contact_phone'] = False

    skill_points = min(20, 5 * len(found_skills))
    score += skill_points
    details['skill_points'] = skill_points

    if exp_years:
        exp_points = min(20, int(exp_years) * 4)
        score += exp_points
        details['experience_points'] = exp_points
    else:
        details['experience_points'] = 0

    if education:
        score += 10
        details['education_present'] = True
    else:
        details['education_present'] = False

    if projects:
        score += 10
        details['projects_present'] = True
    else:
        details['projects_present'] = False

    score = min(100, score)

    suggestions = []
    if not email:
        suggestions.append('Add a professional email address (ideally first.last@domain.com).')
    if not phone:
        suggestions.append('Add a contact phone number with country code.')
    if not found_skills:
        suggestions.append('List technical and soft skills in a dedicated Skills section.')
    if not education:
        suggestions.append('Add education details: degree, institution, year, and notable coursework or percentage/CGPA.')
    if not projects:
        suggestions.append('Add 1-3 projects with brief bullets describing your contribution and technologies used.')
    if len(found_skills) < 5:
        suggestions.append('Include more technical skills (aim for 8-12 relevant skills).')
    if not exp_years:
        suggestions.append('Add experience duration - recruiters look for relevant work history.')

    # Create detailed scoring breakdown explanation
    score_details = {
        'email': {
            'label': 'Email Address',
            'points': 15 if email else 0,
            'max': 15,
            'status': 'Complete' if email else 'Missing',
            'explanation': 'Professional contact email enhances ATS parsing and recruiter communication'
        },
        'phone': {
            'label': 'Phone Number',
            'points': 10 if phone else 0,
            'max': 10,
            'status': 'Complete' if phone else 'Missing',
            'explanation': 'Direct contact number is expected by most ATS systems'
        },
        'skills': {
            'label': f'Technical Skills ({len(found_skills)} found)',
            'points': skill_points,
            'max': 20,
            'status': f'{len(found_skills)}/8+ Skills',
            'explanation': 'Skills are crucial for ATS keyword matching and recruiter filtering'
        },
        'experience': {
            'label': f'Experience ({exp_years} years detected)',
            'points': details.get('experience_points', 0),
            'max': 20,
            'status': f'{exp_years} Years' if exp_years else 'Not Found',
            'explanation': 'Relevant work experience and years improve ATS scoring'
        },
        'education': {
            'label': 'Education',
            'points': 10 if education else 0,
            'max': 10,
            'status': 'Complete' if education else 'Missing',
            'explanation': 'Educational background is a key ATS screening criterion'
        },
        'projects': {
            'label': 'Projects',
            'points': 10 if projects else 0,
            'max': 10,
            'status': 'Complete' if projects else 'Missing',
            'explanation': 'Projects demonstrate practical experience and technical abilities'
        }
    }

    # Compose human-friendly summary
    summary_lines = []
    if name:
        summary_lines.append(f"Candidate name appears to be: {name}.")
    if email or phone:
        c = []
        if email: c.append(f"Email: {email}")
        if phone: c.append(f"Phone: {phone}")
        summary_lines.append('Contact found: ' + '; '.join(c))
    if found_skills:
        summary_lines.append('Top skills detected: ' + ', '.join(found_skills[:8]) + ('.' if len(found_skills)<=8 else '...'))
    if exp_years:
        summary_lines.append(f'Estimated experience: {exp_years} years.')
    if education:
        summary_lines.append('Education entries detected: ' + '; '.join(education[:3]))
    if experience_items:
        sample = [it['raw'] for it in experience_items[:3]]
        summary_lines.append('Sample experience lines: ' + '; '.join(sample))

    human_summary = ' '.join(summary_lines) if summary_lines else 'No strong signals found; resume needs more structure.'

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'experience_years': exp_years,
        'skills_detected': found_skills,
        'education': education,
        'projects': projects,
        'experience_items': experience_items,
        'sections': {k: len(v) for k, v in sections.items()},
        'suggestions': suggestions,
        'score': score,
        'score_breakdown': details,
        'score_details': score_details,
        'human_summary': human_summary,
        'raw_text_preview': full_text[:3000]
    }
