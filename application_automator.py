import time
import random
from typing import Dict, Any, List
import json
from datetime import datetime
import re

class ApplicationAutomator:
    def __init__(self):
        self.application_history = []
        self.cover_letter_templates = {
            'software_engineer': self._get_software_engineer_template(),
            'data_scientist': self._get_data_scientist_template(),
            'product_manager': self._get_product_manager_template(),
            'general': self._get_general_template()
        }
    
    def apply_to_job(self, job_data: Dict[str, Any], resume_data: Dict[str, Any], 
                    customize_cover: bool = True, auto_fill: bool = True) -> Dict[str, Any]:
        """
        Automate the application process for a job.
        Returns application status and details.
        """
        application_result = {
            'status': 'pending',
            'job_title': job_data.get('title', 'Unknown'),
            'company': job_data.get('company', 'Unknown'),
            'applied_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cover_letter': '',
            'application_data': {},
            'errors': [],
            'success': False
        }
        
        try:
            # Step 1: Validate application data
            validation_result = self._validate_application_data(job_data, resume_data)
            if not validation_result['valid']:
                application_result['errors'] = validation_result['errors']
                application_result['status'] = 'failed'
                return application_result
            
            # Step 2: Generate cover letter
            if customize_cover:
                cover_letter = self._generate_cover_letter(job_data, resume_data)
                application_result['cover_letter'] = cover_letter
            
            # Step 3: Prepare application data
            application_data = self._prepare_application_data(job_data, resume_data)
            application_result['application_data'] = application_data
            
            # Step 4: Simulate form filling (in real implementation, this would use Selenium/Playwright)
            if auto_fill:
                fill_result = self._simulate_form_filling(job_data, application_data)
                if fill_result['success']:
                    application_result['status'] = 'submitted'
                    application_result['success'] = True
                else:
                    application_result['errors'] = fill_result['errors']
                    application_result['status'] = 'failed'
            
            # Step 5: Record application
            self._record_application(application_result)
            
        except Exception as e:
            application_result['errors'].append(f"Application failed: {str(e)}")
            application_result['status'] = 'failed'
        
        return application_result
    
    def _validate_application_data(self, job_data: Dict[str, Any], resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that we have all necessary data for the application."""
        errors = []
        
        # Check required resume data
        required_fields = ['name', 'email', 'phone']
        for field in required_fields:
            if not resume_data.get(field) or resume_data[field] == f"{field.title()} not found":
                errors.append(f"Missing {field}")
        
        # Check job data
        if not job_data.get('title'):
            errors.append("Missing job title")
        
        if not job_data.get('company'):
            errors.append("Missing company name")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _generate_cover_letter(self, job_data: Dict[str, Any], resume_data: Dict[str, Any]) -> str:
        """Generate a customized cover letter for the job."""
        job_title = job_data.get('title', '').lower()
        company = job_data.get('company', '')
        job_description = job_data.get('description', '')
        
        # Select appropriate template
        template_key = 'general'
        if 'software' in job_title or 'developer' in job_title or 'engineer' in job_title:
            template_key = 'software_engineer'
        elif 'data' in job_title or 'analyst' in job_title:
            template_key = 'data_scientist'
        elif 'product' in job_title or 'manager' in job_title:
            template_key = 'product_manager'
        
        template = self.cover_letter_templates[template_key]
        
        # Customize template with personal information
        cover_letter = template.format(
            name=resume_data.get('name', 'Your Name'),
            company=company,
            position=job_data.get('title', 'the position'),
            skills=self._format_skills_for_cover_letter(resume_data.get('skills', [])),
            experience=self._format_experience_for_cover_letter(resume_data.get('experience', [])),
            education=self._format_education_for_cover_letter(resume_data.get('education', []))
        )
        
        return cover_letter
    
    def _prepare_application_data(self, job_data: Dict[str, Any], resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare structured data for application forms."""
        return {
            'personal_info': {
                'name': resume_data.get('name', ''),
                'email': resume_data.get('email', ''),
                'phone': resume_data.get('phone', ''),
                'address': resume_data.get('address', ''),
                'linkedin': resume_data.get('linkedin', ''),
                'website': resume_data.get('website', '')
            },
            'education': resume_data.get('education', []),
            'experience': resume_data.get('experience', []),
            'skills': resume_data.get('skills', []),
            'projects': resume_data.get('projects', []),
            'certifications': resume_data.get('certifications', []),
            'summary': resume_data.get('summary', ''),
            'job_info': {
                'title': job_data.get('title', ''),
                'company': job_data.get('company', ''),
                'location': job_data.get('location', ''),
                'type': job_data.get('type', ''),
                'salary': job_data.get('salary', ''),
                'url': job_data.get('url', '')
            }
        }
    
    def _simulate_form_filling(self, job_data: Dict[str, Any], application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate the process of filling out application forms."""
        # This is a simulation - in real implementation, this would use Selenium/Playwright
        # to actually fill out forms on job sites
        
        result = {
            'success': True,
            'errors': [],
            'steps_completed': []
        }
        
        try:
            # Simulate form filling steps
            steps = [
                "Loading application page",
                "Filling personal information",
                "Uploading resume",
                "Filling work experience",
                "Filling education details",
                "Adding skills",
                "Writing cover letter",
                "Submitting application"
            ]
            
            for step in steps:
                # Simulate processing time
                time.sleep(random.uniform(0.5, 2.0))
                result['steps_completed'].append(step)
                
                # Simulate potential errors (5% chance)
                if random.random() < 0.05:
                    result['success'] = False
                    result['errors'].append(f"Error at step: {step}")
                    break
            
            if result['success']:
                result['steps_completed'].append("Application submitted successfully")
                
        except Exception as e:
            result['success'] = False
            result['errors'].append(f"Form filling failed: {str(e)}")
        
        return result
    
    def _record_application(self, application_result: Dict[str, Any]):
        """Record the application in history."""
        self.application_history.append(application_result)
    
    def _format_skills_for_cover_letter(self, skills: List[str]) -> str:
        """Format skills for inclusion in cover letter."""
        if not skills or skills == ["Skills information not found"]:
            return "various technical and professional skills"
        
        # Take first 5 skills
        relevant_skills = skills[:5]
        return ", ".join(relevant_skills)
    
    def _format_experience_for_cover_letter(self, experience: List[str]) -> str:
        """Format experience for inclusion in cover letter."""
        if not experience or experience == ["Experience information not found"]:
            return "relevant experience"
        
        # Take first experience entry
        return experience[0][:100] + "..." if len(experience[0]) > 100 else experience[0]
    
    def _format_education_for_cover_letter(self, education: List[str]) -> str:
        """Format education for inclusion in cover letter."""
        if not education or education == ["Education information not found"]:
            return "relevant education"
        
        # Take first education entry
        return education[0][:100] + "..." if len(education[0]) > 100 else education[0]
    
    def _get_software_engineer_template(self) -> str:
        """Get cover letter template for software engineering positions."""
        return """
Dear Hiring Manager,

I am writing to express my strong interest in the {position} position at {company}. With my background in software development and passion for creating innovative solutions, I believe I would be a valuable addition to your team.

My technical skills include {skills}, and I have experience in {experience}. I am particularly excited about the opportunity to contribute to {company}'s mission and work on challenging technical problems.

Throughout my career, I have demonstrated the ability to write clean, maintainable code and collaborate effectively with cross-functional teams. My education in {education} has provided me with a strong foundation in computer science principles and best practices.

I am confident that my technical expertise, problem-solving abilities, and collaborative approach would make me an asset to your team. I would welcome the opportunity to discuss how my skills and experience align with your needs.

Thank you for considering my application. I look forward to the possibility of contributing to {company}'s success.

Best regards,
{name}
"""
    
    def _get_data_scientist_template(self) -> str:
        """Get cover letter template for data science positions."""
        return """
Dear Hiring Manager,

I am excited to apply for the {position} position at {company}. With my analytical mindset and expertise in data science, I am confident I can contribute significantly to your data-driven initiatives.

My technical skills include {skills}, and I have experience in {experience}. I am particularly drawn to {company}'s commitment to leveraging data for strategic decision-making.

Throughout my career, I have successfully developed machine learning models, conducted statistical analyses, and translated complex data insights into actionable business recommendations. My education in {education} has equipped me with the theoretical foundation and practical skills needed for advanced data analysis.

I am eager to apply my analytical skills to help {company} uncover valuable insights and drive innovation through data.

Thank you for considering my application. I look forward to discussing how I can contribute to your data science team.

Best regards,
{name}
"""
    
    def _get_product_manager_template(self) -> str:
        """Get cover letter template for product management positions."""
        return """
Dear Hiring Manager,

I am writing to express my interest in the {position} position at {company}. With my strategic thinking and experience in product development, I believe I can help drive {company}'s product vision and growth.

My background includes {skills}, and I have experience in {experience}. I am particularly excited about the opportunity to lead product initiatives at {company} and work with talented teams to deliver exceptional user experiences.

Throughout my career, I have successfully managed product lifecycles, conducted market research, and collaborated with engineering and design teams to bring products from concept to market. My education in {education} has provided me with a strong foundation in business strategy and user-centered design.

I am confident that my product management expertise, analytical skills, and collaborative leadership style would make me a valuable addition to your team.

Thank you for considering my application. I look forward to discussing how I can contribute to {company}'s product success.

Best regards,
{name}
"""
    
    def _get_general_template(self) -> str:
        """Get general cover letter template."""
        return """
Dear Hiring Manager,

I am writing to express my interest in the {position} position at {company}. With my background and experience, I believe I would be a valuable addition to your team.

My skills include {skills}, and I have experience in {experience}. I am particularly excited about the opportunity to contribute to {company}'s mission and work on meaningful projects.

My education in {education} has provided me with a strong foundation in my field, and I am eager to apply my knowledge and skills in a dynamic environment like {company}.

I am confident that my abilities and enthusiasm would make me an asset to your organization. I would welcome the opportunity to discuss how my background aligns with your needs.

Thank you for considering my application. I look forward to the possibility of joining your team.

Best regards,
{name}
"""
    
    def get_application_history(self) -> List[Dict[str, Any]]:
        """Get the history of all applications."""
        return self.application_history
    
    def get_application_stats(self) -> Dict[str, Any]:
        """Get statistics about applications."""
        if not self.application_history:
            return {
                'total_applications': 0,
                'successful_applications': 0,
                'failed_applications': 0,
                'success_rate': 0.0
            }
        
        total = len(self.application_history)
        successful = len([app for app in self.application_history if app.get('success', False)])
        failed = total - successful
        
        return {
            'total_applications': total,
            'successful_applications': successful,
            'failed_applications': failed,
            'success_rate': (successful / total) * 100 if total > 0 else 0.0
        }
    
    def save_application_history(self, filename: str = "application_history.json"):
        """Save application history to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.application_history, f, indent=2, ensure_ascii=False)
            print(f"Application history saved to {filename}")
        except Exception as e:
            print(f"Error saving application history: {e}")
    
    def load_application_history(self, filename: str = "application_history.json"):
        """Load application history from a JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.application_history = json.load(f)
            print(f"Application history loaded from {filename}")
        except FileNotFoundError:
            print(f"File {filename} not found")
        except Exception as e:
            print(f"Error loading application history: {e}") 