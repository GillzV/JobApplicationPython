import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict, Any
import json
import re

class JobSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Sample job data for demonstration
        self.sample_jobs = [
            {
                'title': 'Software Engineer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'type': 'Full-time',
                'posted': '2024-01-15',
                'description': 'We are looking for a talented Software Engineer to join our team. Experience with Python, JavaScript, and cloud technologies required.',
                'salary': '$120,000 - $150,000',
                'url': 'https://example.com/job1'
            },
            {
                'title': 'Data Scientist',
                'company': 'Data Analytics Inc',
                'location': 'New York, NY',
                'type': 'Full-time',
                'posted': '2024-01-14',
                'description': 'Join our data science team to build machine learning models and analyze large datasets. Python, R, and SQL experience needed.',
                'salary': '$130,000 - $160,000',
                'url': 'https://example.com/job2'
            },
            {
                'title': 'Frontend Developer',
                'company': 'Web Solutions',
                'location': 'Remote',
                'type': 'Full-time',
                'posted': '2024-01-13',
                'description': 'Create beautiful and responsive web applications using React, Vue.js, and modern CSS frameworks.',
                'salary': '$90,000 - $120,000',
                'url': 'https://example.com/job3'
            },
            {
                'title': 'DevOps Engineer',
                'company': 'Cloud Systems',
                'location': 'Austin, TX',
                'type': 'Full-time',
                'posted': '2024-01-12',
                'description': 'Manage cloud infrastructure and CI/CD pipelines. Experience with AWS, Docker, and Kubernetes required.',
                'salary': '$110,000 - $140,000',
                'url': 'https://example.com/job4'
            },
            {
                'title': 'Product Manager',
                'company': 'Innovation Labs',
                'location': 'Seattle, WA',
                'type': 'Full-time',
                'posted': '2024-01-11',
                'description': 'Lead product development from concept to launch. Strong analytical and communication skills required.',
                'salary': '$140,000 - $180,000',
                'url': 'https://example.com/job5'
            }
        ]
    
    def search_jobs(self, keywords: str, location: str = "", job_type: str = "Full-time") -> List[Dict[str, Any]]:
        """
        Search for jobs based on keywords, location, and job type.
        For demonstration purposes, this returns sample data.
        In a real implementation, this would scrape actual job sites.
        """
        # Filter sample jobs based on search criteria
        filtered_jobs = []
        
        keywords_lower = keywords.lower()
        location_lower = location.lower() if location else ""
        
        for job in self.sample_jobs:
            # Check if job matches keywords
            title_match = keywords_lower in job['title'].lower()
            desc_match = keywords_lower in job['description'].lower()
            company_match = keywords_lower in job['company'].lower()
            
            # Check if job matches location
            location_match = not location or location_lower in job['location'].lower()
            
            # Check if job matches type
            type_match = job_type.lower() in job['type'].lower()
            
            if (title_match or desc_match or company_match) and location_match and type_match:
                filtered_jobs.append(job)
        
        # Add some randomization to simulate real search results
        random.shuffle(filtered_jobs)
        
        return filtered_jobs[:10]  # Return up to 10 jobs
    
    def search_indeed(self, keywords: str, location: str = "", job_type: str = "Full-time") -> List[Dict[str, Any]]:
        """
        Search Indeed for jobs (placeholder implementation).
        Note: Real implementation would require handling rate limiting and terms of service.
        """
        try:
            # Construct Indeed search URL
            base_url = "https://www.indeed.com/jobs"
            params = {
                'q': keywords,
                'l': location,
                'jt': job_type.lower().replace('-', '')
            }
            
            # This is a placeholder - real implementation would need to handle:
            # - Rate limiting
            # - CAPTCHA challenges
            # - Terms of service compliance
            # - Dynamic content loading
            
            print(f"Would search Indeed with: {params}")
            return []
            
        except Exception as e:
            print(f"Error searching Indeed: {e}")
            return []
    
    def search_linkedin(self, keywords: str, location: str = "", job_type: str = "Full-time") -> List[Dict[str, Any]]:
        """
        Search LinkedIn for jobs (placeholder implementation).
        Note: Real implementation would require API access or careful web scraping.
        """
        try:
            # LinkedIn job search URL structure
            base_url = "https://www.linkedin.com/jobs/search"
            params = {
                'keywords': keywords,
                'location': location,
                'f_JT': self._get_linkedin_job_type(job_type)
            }
            
            print(f"Would search LinkedIn with: {params}")
            return []
            
        except Exception as e:
            print(f"Error searching LinkedIn: {e}")
            return []
    
    def search_glassdoor(self, keywords: str, location: str = "", job_type: str = "Full-time") -> List[Dict[str, Any]]:
        """
        Search Glassdoor for jobs (placeholder implementation).
        """
        try:
            base_url = "https://www.glassdoor.com/Job"
            params = {
                'sc.keyword': keywords,
                'locT': 'N',
                'locId': '1',
                'jobType': job_type.lower()
            }
            
            print(f"Would search Glassdoor with: {params}")
            return []
            
        except Exception as e:
            print(f"Error searching Glassdoor: {e}")
            return []
    
    def _get_linkedin_job_type(self, job_type: str) -> str:
        """Convert job type to LinkedIn format."""
        type_mapping = {
            'Full-time': 'F',
            'Part-time': 'P',
            'Contract': 'C',
            'Internship': 'I'
        }
        return type_mapping.get(job_type, 'F')
    
    def get_job_details(self, job_url: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific job posting.
        """
        try:
            # In a real implementation, this would scrape the job details page
            # For now, return sample detailed information
            return {
                'title': 'Software Engineer',
                'company': 'Tech Corp',
                'location': 'San Francisco, CA',
                'type': 'Full-time',
                'posted': '2024-01-15',
                'description': '''
                We are looking for a talented Software Engineer to join our growing team.
                
                Responsibilities:
                - Develop and maintain web applications
                - Collaborate with cross-functional teams
                - Write clean, maintainable code
                - Participate in code reviews
                
                Requirements:
                - 3+ years of experience in software development
                - Proficiency in Python, JavaScript, and SQL
                - Experience with cloud platforms (AWS, Azure, or GCP)
                - Strong problem-solving skills
                - Excellent communication abilities
                
                Benefits:
                - Competitive salary
                - Health insurance
                - 401(k) matching
                - Flexible work arrangements
                - Professional development opportunities
                ''',
                'salary': '$120,000 - $150,000',
                'requirements': [
                    '3+ years of experience in software development',
                    'Proficiency in Python, JavaScript, and SQL',
                    'Experience with cloud platforms',
                    'Strong problem-solving skills'
                ],
                'benefits': [
                    'Competitive salary',
                    'Health insurance',
                    '401(k) matching',
                    'Flexible work arrangements'
                ]
            }
        except Exception as e:
            print(f"Error getting job details: {e}")
            return {}
    
    def filter_jobs_by_salary(self, jobs: List[Dict[str, Any]], min_salary: int = 0, max_salary: int = None) -> List[Dict[str, Any]]:
        """Filter jobs by salary range."""
        filtered_jobs = []
        
        for job in jobs:
            salary = job.get('salary', '')
            if salary and salary != 'N/A':
                # Extract salary numbers (simplified)
                salary_numbers = re.findall(r'\$?(\d+(?:,\d{3})*)', salary)
                if salary_numbers:
                    try:
                        job_salary = int(salary_numbers[0].replace(',', ''))
                        if min_salary <= job_salary and (max_salary is None or job_salary <= max_salary):
                            filtered_jobs.append(job)
                    except ValueError:
                        continue
            else:
                # If no salary info, include the job
                filtered_jobs.append(job)
        
        return filtered_jobs
    
    def filter_jobs_by_experience(self, jobs: List[Dict[str, Any]], experience_level: str) -> List[Dict[str, Any]]:
        """Filter jobs by experience level."""
        experience_keywords = {
            'entry': ['entry', 'junior', '0-2', '1-2', 'recent graduate'],
            'mid': ['mid', 'intermediate', '3-5', '4-6', 'experienced'],
            'senior': ['senior', 'lead', 'principal', '5+', '6+', 'expert']
        }
        
        keywords = experience_keywords.get(experience_level.lower(), [])
        filtered_jobs = []
        
        for job in jobs:
            title = job.get('title', '').lower()
            description = job.get('description', '').lower()
            
            for keyword in keywords:
                if keyword in title or keyword in description:
                    filtered_jobs.append(job)
                    break
        
        return filtered_jobs
    
    def save_job_search_results(self, jobs: List[Dict[str, Any]], filename: str = "job_search_results.json"):
        """Save job search results to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, indent=2, ensure_ascii=False)
            print(f"Job search results saved to {filename}")
        except Exception as e:
            print(f"Error saving job search results: {e}")
    
    def load_job_search_results(self, filename: str = "job_search_results.json") -> List[Dict[str, Any]]:
        """Load job search results from a JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"File {filename} not found")
            return []
        except Exception as e:
            print(f"Error loading job search results: {e}")
            return [] 