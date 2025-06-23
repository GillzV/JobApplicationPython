import json
import os
from typing import List, Dict, Any
from datetime import datetime

class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.applications_file = os.path.join(data_dir, "applications.json")
        self.resume_data_file = os.path.join(data_dir, "resume_data.json")
        self.settings_file = os.path.join(data_dir, "settings.json")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize default settings
        self.default_settings = {
            'auto_save': True,
            'backup_enabled': True,
            'max_backups': 10,
            'default_job_type': 'Full-time',
            'default_location': '',
            'cover_letter_templates': {
                'customize_automatically': True,
                'include_skills': True,
                'include_experience': True
            },
            'application_settings': {
                'auto_fill_forms': True,
                'upload_resume_automatically': True,
                'save_cover_letters': True
            }
        }
    
    def add_application(self, application_data: Dict[str, Any]) -> bool:
        """Add a new application to the database."""
        try:
            applications = self.get_applications()
            
            # Add timestamp if not present
            if 'timestamp' not in application_data:
                application_data['timestamp'] = datetime.now().isoformat()
            
            # Add unique ID
            application_data['id'] = self._generate_id()
            
            applications.append(application_data)
            
            # Save to file
            self._save_applications(applications)
            
            return True
            
        except Exception as e:
            print(f"Error adding application: {e}")
            return False
    
    def get_applications(self) -> List[Dict[str, Any]]:
        """Get all applications from the database."""
        try:
            if os.path.exists(self.applications_file):
                with open(self.applications_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return []
        except Exception as e:
            print(f"Error loading applications: {e}")
            return []
    
    def update_application(self, application_id: str, updated_data: Dict[str, Any]) -> bool:
        """Update an existing application."""
        try:
            applications = self.get_applications()
            
            for i, app in enumerate(applications):
                if app.get('id') == application_id:
                    # Update the application data
                    applications[i].update(updated_data)
                    applications[i]['last_updated'] = datetime.now().isoformat()
                    
                    # Save to file
                    self._save_applications(applications)
                    return True
            
            return False  # Application not found
            
        except Exception as e:
            print(f"Error updating application: {e}")
            return False
    
    def delete_application(self, application_id: str) -> bool:
        """Delete an application from the database."""
        try:
            applications = self.get_applications()
            
            # Filter out the application to delete
            filtered_applications = [app for app in applications if app.get('id') != application_id]
            
            if len(filtered_applications) < len(applications):
                self._save_applications(filtered_applications)
                return True
            else:
                return False  # Application not found
                
        except Exception as e:
            print(f"Error deleting application: {e}")
            return False
    
    def get_application_by_id(self, application_id: str) -> Dict[str, Any]:
        """Get a specific application by ID."""
        applications = self.get_applications()
        
        for app in applications:
            if app.get('id') == application_id:
                return app
        
        return {}
    
    def search_applications(self, search_term: str, field: str = 'all') -> List[Dict[str, Any]]:
        """Search applications by term and field."""
        applications = self.get_applications()
        search_term_lower = search_term.lower()
        
        if field == 'all':
            # Search in all text fields
            matching_apps = []
            for app in applications:
                for key, value in app.items():
                    if isinstance(value, str) and search_term_lower in value.lower():
                        matching_apps.append(app)
                        break
            return matching_apps
        else:
            # Search in specific field
            return [app for app in applications 
                   if field in app and search_term_lower in str(app[field]).lower()]
    
    def get_application_stats(self) -> Dict[str, Any]:
        """Get statistics about applications."""
        applications = self.get_applications()
        
        if not applications:
            return {
                'total_applications': 0,
                'applications_this_month': 0,
                'applications_this_week': 0,
                'success_rate': 0.0,
                'top_companies': [],
                'top_positions': []
            }
        
        # Calculate basic stats
        total = len(applications)
        
        # Calculate time-based stats
        now = datetime.now()
        this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        this_week = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        monthly_count = 0
        weekly_count = 0
        
        for app in applications:
            try:
                app_date = datetime.fromisoformat(app.get('date', app.get('timestamp', '')))
                if app_date >= this_month:
                    monthly_count += 1
                if app_date >= this_week:
                    weekly_count += 1
            except:
                continue
        
        # Calculate success rate
        successful = len([app for app in applications if app.get('status') == 'Applied'])
        success_rate = (successful / total) * 100 if total > 0 else 0.0
        
        # Get top companies and positions
        companies = {}
        positions = {}
        
        for app in applications:
            company = app.get('company', 'Unknown')
            position = app.get('position', 'Unknown')
            
            companies[company] = companies.get(company, 0) + 1
            positions[position] = positions.get(position, 0) + 1
        
        top_companies = sorted(companies.items(), key=lambda x: x[1], reverse=True)[:5]
        top_positions = sorted(positions.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_applications': total,
            'applications_this_month': monthly_count,
            'applications_this_week': weekly_count,
            'success_rate': success_rate,
            'top_companies': top_companies,
            'top_positions': top_positions
        }
    
    def save_resume_data(self, resume_data: Dict[str, Any]) -> bool:
        """Save resume data to file."""
        try:
            with open(self.resume_data_file, 'w', encoding='utf-8') as f:
                json.dump(resume_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving resume data: {e}")
            return False
    
    def load_resume_data(self) -> Dict[str, Any]:
        """Load resume data from file."""
        try:
            if os.path.exists(self.resume_data_file):
                with open(self.resume_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            print(f"Error loading resume data: {e}")
            return {}
    
    def get_settings(self) -> Dict[str, Any]:
        """Get application settings."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    # Merge with default settings
                    return {**self.default_settings, **saved_settings}
            else:
                return self.default_settings.copy()
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """Save application settings."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def update_setting(self, key: str, value: Any) -> bool:
        """Update a specific setting."""
        try:
            settings = self.get_settings()
            settings[key] = value
            return self.save_settings(settings)
        except Exception as e:
            print(f"Error updating setting: {e}")
            return False
    
    def backup_data(self) -> bool:
        """Create a backup of all data files."""
        try:
            if not self.get_settings().get('backup_enabled', True):
                return True
            
            backup_dir = os.path.join(self.data_dir, "backups")
            os.makedirs(backup_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Backup applications
            if os.path.exists(self.applications_file):
                backup_file = os.path.join(backup_dir, f"applications_{timestamp}.json")
                with open(self.applications_file, 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
            
            # Backup resume data
            if os.path.exists(self.resume_data_file):
                backup_file = os.path.join(backup_dir, f"resume_data_{timestamp}.json")
                with open(self.resume_data_file, 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
            
            # Clean up old backups
            self._cleanup_old_backups(backup_dir)
            
            return True
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def export_data(self, export_format: str = 'json') -> str:
        """Export all data in specified format."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if export_format.lower() == 'json':
                export_file = os.path.join(self.data_dir, f"export_{timestamp}.json")
                
                export_data = {
                    'applications': self.get_applications(),
                    'resume_data': self.load_resume_data(),
                    'settings': self.get_settings(),
                    'export_date': datetime.now().isoformat()
                }
                
                with open(export_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                return export_file
            
            elif export_format.lower() == 'csv':
                # CSV export would require additional implementation
                print("CSV export not yet implemented")
                return ""
            
            else:
                print(f"Unsupported export format: {export_format}")
                return ""
                
        except Exception as e:
            print(f"Error exporting data: {e}")
            return ""
    
    def _save_applications(self, applications: List[Dict[str, Any]]):
        """Save applications to file."""
        try:
            with open(self.applications_file, 'w', encoding='utf-8') as f:
                json.dump(applications, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving applications: {e}")
    
    def _generate_id(self) -> str:
        """Generate a unique ID for applications."""
        return datetime.now().strftime("%Y%m%d_%H%M%S_") + str(hash(datetime.now().timestamp()))[-6:]
    
    def _cleanup_old_backups(self, backup_dir: str):
        """Remove old backup files if there are too many."""
        try:
            max_backups = self.get_settings().get('max_backups', 10)
            
            backup_files = []
            for filename in os.listdir(backup_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(backup_dir, filename)
                    backup_files.append((filepath, os.path.getmtime(filepath)))
            
            # Sort by modification time (oldest first)
            backup_files.sort(key=lambda x: x[1])
            
            # Remove oldest files if we have too many
            if len(backup_files) > max_backups:
                files_to_remove = backup_files[:-max_backups]
                for filepath, _ in files_to_remove:
                    os.remove(filepath)
                    
        except Exception as e:
            print(f"Error cleaning up old backups: {e}") 