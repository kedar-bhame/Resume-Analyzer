#!/usr/bin/env python3
"""
Script to generate 5 professional resume templates
Run this script to create the templates in the templates folder
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_cell_border(cell, **kwargs):
    """Add borders to table cells"""
    tc = cell._element
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        if edge in kwargs:
            edge_element = OxmlElement(f'w:{edge}')
            edge_element.set(qn('w:val'), 'single')
            edge_element.set(qn('w:sz'), '4')
            edge_element.set(qn('w:space'), '0')
            edge_element.set(qn('w:color'), 'CCCCCC')
            tcBorders.append(edge_element)
    tcPr.append(tcBorders)

def create_template_1_minimal():
    """Template 1: Minimal Clean Resume"""
    doc = Document()
    
    # Set margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
    
    # Name
    name = doc.add_paragraph("YOUR NAME", style='Normal')
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name_format = name.runs[0].font
    name_format.size = Pt(24)
    name_format.bold = True
    
    # Contact Info
    contact = doc.add_paragraph("your.email@example.com | +1-XXX-XXX-XXXX | LinkedIn.com/in/yourprofile | City, State", style='Normal')
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_format = contact.runs[0].font
    contact_format.size = Pt(10)
    
    # Professional Summary
    doc.add_heading('PROFESSIONAL SUMMARY', level=1).runs[0].font.size = Pt(12)
    doc.add_paragraph("Brief overview of your professional background, key skills, and career objectives.")
    
    # Experience
    doc.add_heading('PROFESSIONAL EXPERIENCE', level=1).runs[0].font.size = Pt(12)
    
    job = doc.add_paragraph("Job Title", style='Normal')
    job.runs[0].font.bold = True
    job.runs[0].font.size = Pt(11)
    co_info = doc.add_paragraph("Company Name | City, State | Month Year – Present")
    co_info.runs[0].font.size = Pt(10)
    doc.add_paragraph("Achievement or responsibility with quantifiable results", style='List Bullet')
    doc.add_paragraph("Key contribution that demonstrates impact", style='List Bullet')
    
    # Education
    doc.add_heading('EDUCATION', level=1).runs[0].font.size = Pt(12)
    degree = doc.add_paragraph("Bachelor of Science in [Field]", style='Normal')
    degree.runs[0].font.bold = True
    degree.runs[0].font.size = Pt(11)
    school = doc.add_paragraph("University Name | Graduation: Month Year | GPA: 3.XX/4.0")
    school.runs[0].font.size = Pt(10)
    
    # Skills
    doc.add_heading('SKILLS', level=1).runs[0].font.size = Pt(12)
    doc.add_paragraph("Technical Skills: Python, JavaScript, SQL, AWS, Git, Docker")
    doc.add_paragraph("Soft Skills: Project Management, Team Leadership, Communication, Problem Solving")
    
    # Certifications
    doc.add_heading('CERTIFICATIONS', level=1).runs[0].font.size = Pt(12)
    doc.add_paragraph("Relevant Certification Name - Issuing Organization, Year", style='List Bullet')
    
    return doc

def create_template_2_professional():
    """Template 2: Professional Executive Resume"""
    doc = Document()
    
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
    
    # Header
    name = doc.add_paragraph("YOUR NAME", style='Normal')
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name_format = name.runs[0].font
    name_format.size = Pt(26)
    name_format.bold = True
    name_format.color.rgb = RGBColor(0, 51, 102)
    
    contact = doc.add_paragraph("Email: your.email@example.com | Phone: +1-XXX-XXX-XXXX | LinkedIn: linkedin.com/in/yourprofile", style='Normal')
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # Executive Profile
    doc.add_heading('EXECUTIVE PROFILE', level=1)
    para = doc.add_paragraph("Senior professional with 10+ years of experience in [Industry]. Proven track record of driving business growth, leading cross-functional teams, and implementing strategic initiatives.")
    
    # Core Competencies
    doc.add_heading('CORE COMPETENCIES', level=1)
    competencies = doc.add_paragraph()
    competencies.add_run("Leadership & Management, ").font.size = Pt(10)
    competencies.add_run("Strategic Planning, ").font.size = Pt(10)
    competencies.add_run("Business Development, ").font.size = Pt(10)
    competencies.add_run("Financial Analysis, ").font.size = Pt(10)
    competencies.add_run("Project Management")
    
    # Professional Experience
    doc.add_heading('PROFESSIONAL EXPERIENCE', level=1)
    
    # Job 1
    job1 = doc.add_paragraph()
    job1.add_run("Senior Manager").font.bold = True
    job1.add_run(" - CompanyName")
    ex1_date = doc.add_paragraph("January 20XX – Present")
    ex1_date.runs[0].font.size = Pt(10)
    ex1_date.runs[0].font.italic = True
    doc.add_paragraph("Led team of 15+ professionals across multiple departments", style='List Bullet')
    doc.add_paragraph("Increased revenue by 35% through strategic partnerships", style='List Bullet')
    doc.add_paragraph("Implemented cost-saving initiatives resulting in $500K annual savings", style='List Bullet')
    
    # Education
    doc.add_heading('EDUCATION', level=1)
    degree = doc.add_paragraph()
    degree.add_run("Master of Business Administration (MBA)").font.bold = True
    edu_inst = doc.add_paragraph("Prestigious University | Graduation: May 20XX")
    edu_inst.runs[0].font.italic = True
    
    return doc

def create_template_3_creative():
    """Template 3: Creative Modern Design Resume"""
    doc = Document()
    
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
    
    # Header
    name = doc.add_paragraph("YOUR NAME")
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name.runs[0].font.size = Pt(24)
    name.runs[0].font.bold = True
    
    title = doc.add_paragraph("Creative Professional")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    contact = doc.add_paragraph("your.email@example.com | +1-XXX-XXX-XXXX | LinkedIn.com/in/yourprofile | City, State")
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact.runs[0].font.size = Pt(9)
    
    doc.add_paragraph()  # Spacing
    
    # Summary
    summary_heading = doc.add_heading('ABOUT', level=1)
    summary_heading.runs[0].font.size = Pt(12)
    doc.add_paragraph("Creative professional with strong background in design and innovation. Passionate about solving complex problems and delivering impactful solutions.")
    
    # Experience
    exp_heading = doc.add_heading('EXPERIENCE', level=1)
    exp_heading.runs[0].font.size = Pt(12)
    
    exp_title = doc.add_paragraph("Creative Director")
    exp_title.runs[0].font.bold = True
    exp_company = doc.add_paragraph("Design Studio Name | 2020 – Present")
    exp_company.runs[0].font.italic = True
    exp_company.runs[0].font.size = Pt(10)
    doc.add_paragraph("Directed creative strategy for 50+ successful campaigns", style='List Bullet')
    doc.add_paragraph("Collaborated with stakeholders to deliver award-winning designs", style='List Bullet')
    
    # Skills
    skills_heading = doc.add_heading('SKILLS', level=1)
    skills_heading.runs[0].font.size = Pt(12)
    doc.add_paragraph("Design: Figma, Adobe Creative Suite, UI/UX Design, Prototyping")
    doc.add_paragraph("Development: HTML, CSS, JavaScript, React, Vue.js")
    doc.add_paragraph("Management: Agile, Team Leadership, Project Coordination")
    
    # Education
    doc.add_heading('EDUCATION', level=1)
    degree = doc.add_paragraph("Bachelor of Arts in Graphic Design")
    degree.runs[0].font.bold = True
    school = doc.add_paragraph("Design University | Graduation: May 20XX")
    
    return doc

def create_template_4_academic():
    """Template 4: Academic & Research CV"""
    doc = Document()
    
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
    
    # Header
    name = doc.add_paragraph("YOUR NAME, PhD")
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name.runs[0].font.size = Pt(22)
    name.runs[0].font.bold = True
    
    title = doc.add_paragraph("Assistant Professor of [Field]")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.runs[0].font.size = Pt(12)
    
    contact = doc.add_paragraph("your.email@university.edu | +1-XXX-XXX-XXXX | Office: Building XYZ, Room ###")
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact.runs[0].font.size = Pt(10)
    
    # Education
    doc.add_heading('EDUCATION', level=1)
    phd = doc.add_paragraph("PhD in [Field], University Name, Year")
    phd.runs[0].font.bold = True
    doc.add_paragraph("Dissertation: [Title of Research]")
    doc.add_paragraph("Master of Science in [Field], University Name, Year")
    doc.add_paragraph("Bachelor of Science in [Field], University Name, Year")
    
    # Research Interests
    doc.add_heading('RESEARCH INTERESTS', level=1)
    doc.add_paragraph("Research Area 1, Research Area 2, Research Area 3, Research Methodology")
    
    # Publications
    doc.add_heading('PUBLICATIONS', level=1)
    doc.add_paragraph("Author, A., et al. (Year). 'Article Title.' Journal Name, Volume(Issue), pp. XX-YY.", style='List Bullet')
    doc.add_paragraph("Author, A., et al. (Year). 'Research Paper Title.' Conference Proceedings, pp. XX-YY.", style='List Bullet')
    
    # Grants & Funding
    doc.add_heading('GRANTS & FUNDING', level=1)
    doc.add_paragraph("[$XXX,XXX] - Grant Title - Funding Agency - Years", style='List Bullet')
    
    # Teaching Experience
    doc.add_heading('TEACHING EXPERIENCE', level=1)
    doc.add_paragraph("Course Name (XXX) - Undergraduate/Graduate - Year", style='List Bullet')
    
    return doc

def create_template_5_technical():
    """Template 5: Technical Engineer Resume"""
    doc = Document()
    
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
    
    # Header
    name = doc.add_paragraph("YOUR NAME")
    name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    name.runs[0].font.size = Pt(24)
    name.runs[0].font.bold = True
    
    title = doc.add_paragraph("Senior Software Engineer | Full-Stack Developer")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    contact = doc.add_paragraph("Email: your.email@example.com | Phone: +1-XXX-XXX-XXXX | GitHub: github.com/username | LinkedIn: linkedin.com/in/username")
    contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact.runs[0].font.size = Pt(9)
    
    # Technical Skills
    doc.add_heading('TECHNICAL SKILLS', level=1)
    
    skills_table = doc.add_table(rows=4, cols=2)
    skills_table.autofit = False
    
    skills_data = [
        ['Programming Languages', 'Python, JavaScript, TypeScript, Java, C++, Go'],
        ['Web Technologies', 'React, Node.js, Django, Flask, FastAPI, AWS, Docker, Kubernetes'],
        ['Databases', 'PostgreSQL, MongoDB, Redis, MySQL, DynamoDB'],
        ['Tools & Platforms', 'Git, Jenkins, CircleCI, AWS, GCP, Azure, Linux, Docker']
    ]
    
    for i, (label, skills) in enumerate(skills_data):
        row_cells = skills_table.rows[i].cells
        row_cells[0].text = label
        row_cells[0].paragraphs[0].runs[0].font.bold = True
        row_cells[1].text = skills
    
    # Professional Experience
    doc.add_heading('PROFESSIONAL EXPERIENCE', level=1)
    
    job = doc.add_paragraph("Senior Software Engineer")
    job.runs[0].font.bold = True
    job_info = doc.add_paragraph("Tech Company | January 2022 – Present")
    job_info.runs[0].font.italic = True
    job_info.runs[0].font.size = Pt(10)
    doc.add_paragraph("Architected scalable microservices handling 1M+ requests/day using Python and Kubernetes", style='List Bullet')
    doc.add_paragraph("Led team of 5 engineers, improving code quality by 40% through CI/CD implementation", style='List Bullet')
    doc.add_paragraph("Optimized database queries, reducing API response time by 60%", style='List Bullet')
    doc.add_paragraph("Mentored junior developers and conducted technical interviews", style='List Bullet')
    
    # Projects
    doc.add_heading('NOTABLE PROJECTS', level=1)
    doc.add_paragraph("Real-time Data Pipeline - Designed ETL pipeline processing 100M+ records daily using Apache Spark and AWS", style='List Bullet')
    doc.add_paragraph("Mobile App Backend - Developed REST API using Node.js and MongoDB for iOS/Android app with 500K+ users", style='List Bullet')
    
    # Education
    doc.add_heading('EDUCATION', level=1)
    degree = doc.add_paragraph("Bachelor of Science in Computer Science")
    degree.runs[0].font.bold = True
    school = doc.add_paragraph("University Name | Graduation: May 20XX | GPA: 3.8/4.0")
    
    # Certifications
    doc.add_heading('CERTIFICATIONS', level=1)
    doc.add_paragraph("AWS Certified Solutions Architect - Professional, 20XX", style='List Bullet')
    doc.add_paragraph("Google Cloud Professional Data Engineer, 20XX", style='List Bullet')
    
    return doc

def generate_all_templates():
    """Generate all 5 templates"""
    templates_folder = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_folder, exist_ok=True)
    
    templates = [
        ('template_1_minimal_clean.docx', create_template_1_minimal, 'Minimal Clean Resume'),
        ('template_2_professional_executive.docx', create_template_2_professional, 'Professional Executive'),
        ('template_3_creative_modern.docx', create_template_3_creative, 'Creative Modern Design'),
        ('template_4_academic_cv.docx', create_template_4_academic, 'Academic & Research CV'),
        ('template_5_technical_engineer.docx', create_template_5_technical, 'Technical Engineer Resume')
    ]
    
    for filename, create_func, description in templates:
        filepath = os.path.join(templates_folder, filename)
        try:
            doc = create_func()
            doc.save(filepath)
            print(f"✓ Created: {description} ({filename})")
        except Exception as e:
            print(f"✗ Error creating {description}: {e}")

if __name__ == '__main__':
    generate_all_templates()
    print("\n✓ All templates generated successfully!")
