import re
from typing import Dict, List, Any, Optional
import PyPDF2
from docx import Document
import os

SECTION_HEADERS = [
    'profile', 'summary', 'objective',
    'projects', 'project experience',
    'technical skills', 'skills', 'technologies',
    'work experience', 'experience', 'employment',
    'education', 'academic background',
    'awards', 'certifications', 'certification', 'honors',
    'languages', 'language',
    'contact', 'contact information', 'personal information'
]

SECTION_MAP = {
    'profile': ['profile', 'summary', 'objective'],
    'projects': ['projects', 'project experience'],
    'skills': ['technical skills', 'skills', 'technologies'],
    'work_experience': ['work experience', 'experience', 'employment'],
    'education': ['education', 'academic background'],
    'awards_certifications': ['awards', 'certifications', 'certification', 'honors'],
    'languages': ['languages', 'language'],
    'contact': ['contact', 'contact information', 'personal information']
}

CONTACT_PATTERNS = {
    'email': r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
    'phone': r'(\+?\d{1,2}[\s-]?)?(\(?\d{3}\)?[\s-]?)?\d{3}[\s-]?\d{4}',
}


def extract_text(file_path: str) -> str:
    ext = file_path.lower().split('.')[-1]
    if ext == 'pdf':
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            return '\n'.join([page.extract_text() or '' for page in reader.pages])
    elif ext == 'docx':
        doc = Document(file_path)
        return '\n'.join([p.text for p in doc.paragraphs])
    elif ext == 'txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise ValueError('Unsupported file type')


def find_section_indices(lines: List[str]) -> List[tuple]:
    indices = []
    for i, line in enumerate(lines):
        header = line.strip().lower().rstrip(':')
        for canonical, variants in SECTION_MAP.items():
            if any(header == v for v in variants):
                indices.append((i, canonical))
    return indices


def group_sections(lines: List[str]) -> Dict[str, List[str]]:
    indices = find_section_indices(lines)
    if not indices:
        return {}
    indices.append((len(lines), None))  # Sentinel for last section
    sections = {}
    for idx in range(len(indices) - 1):
        start, section = indices[idx]
        end, _ = indices[idx + 1]
        content = [l for l in lines[start + 1:end] if l.strip()]
        if section:
            sections[section] = content
    return sections


def extract_contact(lines: List[str]) -> Dict[str, str]:
    contact = {'name': '', 'email': '', 'phone': ''}
    # Name: first non-empty line
    for line in lines:
        if line.strip():
            contact['name'] = line.strip()
            break
    # Email/Phone: anywhere in first 10 lines
    for line in lines[:10]:
        if not contact['email']:
            m = re.search(CONTACT_PATTERNS['email'], line)
            if m:
                contact['email'] = m.group()
        if not contact['phone']:
            m = re.search(CONTACT_PATTERNS['phone'], line)
            if m:
                contact['phone'] = m.group()
    return contact


def parse_bullets(section_lines: List[str]) -> List[str]:
    bullets = []
    for line in section_lines:
        line = line.strip()
        if line.startswith(('•', '-', '*', '→', '▶', '○', '▪', '▫')):
            # Only add bullet point for lines that actually start with bullet characters
            bullets.append(line)
        elif line:
            # Regular text lines are added as-is without bullet points
            bullets.append(line)
    return bullets


def parse_resume(file_path: str) -> Dict[str, Any]:
    text = extract_text(file_path)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    sections = group_sections(lines)
    contact = extract_contact(lines)

    parsed = {
        'name': contact['name'],
        'email': contact['email'],
        'phone': contact['phone'],
        'profile': [],
        'projects': [],
        'skills': [],
        'work_experience': [],
        'education': [],
        'awards_certifications': [],
        'languages': []
    }

    for key in parsed.keys():
        if key in ['name', 'email', 'phone']:
            continue
        if key in sections:
            if key in ['profile', 'skills', 'awards_certifications', 'languages']:
                parsed[key] = parse_bullets(sections[key])
            elif key == 'projects':
                parsed[key] = parse_bullets(sections[key])
            elif key == 'work_experience':
                parsed[key] = parse_bullets(sections[key])
            elif key == 'education':
                parsed[key] = parse_bullets(sections[key])
    return parsed


class ResumeParser:
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        return parse_resume(file_path)

    def validate_resume_data(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Validate extracted resume data and return any issues found."""
        issues = {
            'missing': [],
            'incomplete': [],
            'suggestions': []
        }
        
        # Check for missing critical information
        if not data.get('name') or data['name'] == "Name not found":
            issues['missing'].append("Name")
        
        if not data.get('email') or data['email'] == "Email not found":
            issues['missing'].append("Email address")
        
        if not data.get('phone') or data['phone'] == "Phone not found":
            issues['missing'].append("Phone number")
        
        # Check for incomplete sections
        if not data.get('summary') or data['summary'] == "Summary not found":
            issues['incomplete'].append("Professional summary")
        
        if not data.get('experience') or data['experience'] == ["Experience information not found"]:
            issues['incomplete'].append("Work experience")
        
        if not data.get('skills') or data['skills'] == ["Skills information not found"]:
            issues['incomplete'].append("Skills section")
        
        # Suggestions for improvement
        if len(data.get('education', [])) < 1:
            issues['suggestions'].append("Add education information")
        
        if len(data.get('projects', [])) < 1:
            issues['suggestions'].append("Add project portfolio")
        
        return issues 