import re
import PyPDF2
from docx import Document
import json
from typing import Dict, List, Any

class ResumeParser:
    def __init__(self):
        self.name_patterns = [
            r'^[A-Z][a-z]+ [A-Z][a-z]+$',
            r'^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+$'
        ]
        
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Parse resume from various file formats and extract structured information."""
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            text = self._extract_text_from_pdf(file_path)
        elif file_extension == 'docx':
            text = self._extract_text_from_docx(file_path)
        elif file_extension == 'txt':
            text = self._extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        return self._extract_information(text)
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
        return text
    
    def _extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
        return text
    
    def _extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")
    
    def _extract_information(self, text: str) -> Dict[str, Any]:
        """Extract structured information from resume text."""
        lines = text.split('\n')
        
        # Initialize data structure
        resume_data = {
            'name': '',
            'email': '',
            'phone': '',
            'address': '',
            'summary': '',
            'education': [],
            'experience': [],
            'skills': [],
            'projects': [],
            'certifications': []
        }
        
        # Extract basic information
        resume_data['name'] = self._extract_name(lines)
        resume_data['email'] = self._extract_email(text)
        resume_data['phone'] = self._extract_phone(text)
        resume_data['address'] = self._extract_address(lines)
        
        # Extract sections
        resume_data['summary'] = self._extract_summary(text)
        resume_data['education'] = self._extract_education(text)
        resume_data['experience'] = self._extract_experience(text)
        resume_data['skills'] = self._extract_skills(text)
        resume_data['projects'] = self._extract_projects(text)
        resume_data['certifications'] = self._extract_certifications(text)
        
        return resume_data
    
    def _extract_name(self, lines: List[str]) -> str:
        """Extract name from resume lines."""
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line.split()) <= 4:  # Name should be 1-4 words
                for pattern in self.name_patterns:
                    if re.match(pattern, line):
                        return line
        return "Name not found"
    
    def _extract_email(self, text: str) -> str:
        """Extract email address from text."""
        emails = re.findall(self.email_pattern, text)
        return emails[0] if emails else "Email not found"
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from text."""
        phones = re.findall(self.phone_pattern, text)
        return phones[0] if phones else "Phone not found"
    
    def _extract_address(self, lines: List[str]) -> str:
        """Extract address from resume lines."""
        address_keywords = ['street', 'avenue', 'road', 'drive', 'lane', 'city', 'state', 'zip']
        
        for line in lines[:20]:  # Check first 20 lines
            line = line.strip().lower()
            if any(keyword in line for keyword in address_keywords):
                return line.title()
        return "Address not found"
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary from text."""
        summary_patterns = [
            r'summary[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'objective[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'profile[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        return "Summary not found"
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information from text."""
        education = []
        education_patterns = [
            r'education[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'degree[:\s]*(.*?)(?=\n|$)',
            r'university[:\s]*(.*?)(?=\n|$)',
            r'college[:\s]*(.*?)(?=\n|$)'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if match.strip() and len(match.strip()) > 10:
                    education.append(match.strip())
        
        return education if education else ["Education information not found"]
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract work experience from text."""
        experience = []
        experience_patterns = [
            r'experience[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'work history[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'employment[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if match.strip() and len(match.strip()) > 20:
                    experience.append(match.strip())
        
        return experience if experience else ["Experience information not found"]
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text."""
        skills = []
        skills_patterns = [
            r'skills[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'technical skills[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'programming languages[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        for pattern in skills_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Split by common delimiters
                skill_list = re.split(r'[,;•\n]', match)
                for skill in skill_list:
                    skill = skill.strip()
                    if skill and len(skill) > 2:
                        skills.append(skill)
        
        return skills if skills else ["Skills information not found"]
    
    def _extract_projects(self, text: str) -> List[str]:
        """Extract projects from text."""
        projects = []
        project_patterns = [
            r'projects[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'portfolio[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        for pattern in project_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if match.strip() and len(match.strip()) > 20:
                    projects.append(match.strip())
        
        return projects if projects else ["Projects information not found"]
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications from text."""
        certifications = []
        cert_patterns = [
            r'certifications[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'certificates[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            r'licenses[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)'
        ]
        
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                cert_list = re.split(r'[,;•\n]', match)
                for cert in cert_list:
                    cert = cert.strip()
                    if cert and len(cert) > 5:
                        certifications.append(cert)
        
        return certifications if certifications else ["Certifications information not found"]
    
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