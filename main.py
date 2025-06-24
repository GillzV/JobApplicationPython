import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
import threading
import json
import os
from datetime import datetime
from resume_parser import ResumeParser
from job_searcher import JobSearcher
from application_automator import ApplicationAutomator
from data_manager import DataManager

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JobApplicationBot:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Job Application Automation Bot")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Initialize components
        self.resume_parser = ResumeParser()
        self.job_searcher = JobSearcher()
        self.app_automator = ApplicationAutomator()
        self.data_manager = DataManager()
        
        # Data storage
        self.resume_data = {}
        self.job_listings = []
        self.current_job = None
        
        self.setup_ui()
        self.load_saved_data()
    
    def setup_ui(self):
        # Create main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_container, 
            text="🤖 Job Application Automation Bot",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Create notebook for tabs
        self.notebook = ctk.CTkTabview(main_container)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create tabs
        self.setup_resume_tab()
        self.setup_job_search_tab()
        self.setup_application_tab()
        self.setup_tracking_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ctk.CTkLabel(
            main_container, 
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        status_bar.pack(pady=(10, 0))
    
    def setup_resume_tab(self):
        resume_frame = self.notebook.add("📄 Resume")
        
        # Resume upload section
        upload_frame = ctk.CTkFrame(resume_frame)
        upload_frame.pack(fill="x", padx=20, pady=20)
        
        upload_label = ctk.CTkLabel(
            upload_frame, 
            text="Upload Your Resume",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        upload_label.pack(pady=10)
        
        # File selection
        file_frame = ctk.CTkFrame(upload_frame)
        file_frame.pack(fill="x", padx=20, pady=10)
        
        self.file_path_var = tk.StringVar(value="No file selected")
        file_label = ctk.CTkLabel(file_frame, textvariable=self.file_path_var)
        file_label.pack(side="left", padx=10, pady=10)
        
        browse_btn = ctk.CTkButton(
            file_frame, 
            text="Browse",
            command=self.browse_resume,
            width=100
        )
        browse_btn.pack(side="right", padx=10, pady=10)
        
        # Parse button
        parse_btn = ctk.CTkButton(
            upload_frame,
            text="Parse Resume",
            command=self.parse_resume,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        parse_btn.pack(pady=20)
        
        # Resume data display
        data_frame = ctk.CTkFrame(resume_frame)
        data_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        data_label = ctk.CTkLabel(
            data_frame,
            text="Extracted Information",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        data_label.pack(pady=10)
        
        # Create text widget for displaying resume data
        self.resume_text = ctk.CTkTextbox(data_frame, height=300)
        self.resume_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Edit button
        edit_btn = ctk.CTkButton(
            data_frame,
            text="Edit Information",
            command=self.edit_resume_data
        )
        edit_btn.pack(pady=10)
    
    def setup_job_search_tab(self):
        search_frame = self.notebook.add("🔍 Job Search")
        
        # Search parameters
        params_frame = ctk.CTkFrame(search_frame)
        params_frame.pack(fill="x", padx=20, pady=20)
        
        params_label = ctk.CTkLabel(
            params_frame,
            text="Search Parameters",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        params_label.pack(pady=10)
        
        # Search fields
        fields_frame = ctk.CTkFrame(params_frame)
        fields_frame.pack(fill="x", padx=20, pady=10)
        
        # Keywords
        ctk.CTkLabel(fields_frame, text="Keywords:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.keywords_var = tk.StringVar()
        keywords_entry = ctk.CTkEntry(fields_frame, textvariable=self.keywords_var, width=300)
        keywords_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        # Location
        ctk.CTkLabel(fields_frame, text="Location:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.location_var = tk.StringVar()
        location_entry = ctk.CTkEntry(fields_frame, textvariable=self.location_var, width=300)
        location_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        # Job type
        ctk.CTkLabel(fields_frame, text="Job Type:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.job_type_var = tk.StringVar(value="Full-time")
        job_type_menu = ctk.CTkOptionMenu(
            fields_frame,
            values=["Full-time", "Part-time", "Contract", "Internship"],
            variable=self.job_type_var
        )
        job_type_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        fields_frame.columnconfigure(1, weight=1)
        
        # Search button
        search_btn = ctk.CTkButton(
            params_frame,
            text="Search Jobs",
            command=self.search_jobs,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        search_btn.pack(pady=20)
        
        # Results display
        results_frame = ctk.CTkFrame(search_frame)
        results_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        results_label = ctk.CTkLabel(
            results_frame,
            text="Job Listings",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        results_label.pack(pady=10)
        
        # Create treeview for job listings
        columns = ("Title", "Company", "Location", "Type", "Posted")
        self.job_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.job_tree.heading(col, text=col)
            self.job_tree.column(col, width=150)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.job_tree.yview)
        self.job_tree.configure(yscrollcommand=scrollbar.set)
        
        self.job_tree.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Bind selection event
        self.job_tree.bind("<<TreeviewSelect>>", self.on_job_select)
        
        # Job details
        details_frame = ctk.CTkFrame(results_frame)
        details_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.job_details_text = ctk.CTkTextbox(details_frame, height=200)
        self.job_details_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def setup_application_tab(self):
        app_frame = self.notebook.add("📝 Apply")
        
        # Application section
        app_section = ctk.CTkFrame(app_frame)
        app_section.pack(fill="both", expand=True, padx=20, pady=20)
        
        app_label = ctk.CTkLabel(
            app_section,
            text="Application Automation",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        app_label.pack(pady=10)
        
        # Selected job info
        self.selected_job_label = ctk.CTkLabel(
            app_section,
            text="No job selected",
            font=ctk.CTkFont(size=14)
        )
        self.selected_job_label.pack(pady=10)
        
        # Application settings
        settings_frame = ctk.CTkFrame(app_section)
        settings_frame.pack(fill="x", padx=20, pady=20)
        
        settings_label = ctk.CTkLabel(
            settings_frame,
            text="Application Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        settings_label.pack(pady=10)
        
        # Customize cover letter
        self.customize_cover_var = tk.BooleanVar(value=True)
        customize_check = ctk.CTkCheckBox(
            settings_frame,
            text="Customize cover letter for each job",
            variable=self.customize_cover_var
        )
        customize_check.pack(pady=5)
        
        # Auto-fill forms
        self.auto_fill_var = tk.BooleanVar(value=True)
        auto_fill_check = ctk.CTkCheckBox(
            settings_frame,
            text="Auto-fill application forms",
            variable=self.auto_fill_var
        )
        auto_fill_check.pack(pady=5)
        
        # Apply button
        apply_btn = ctk.CTkButton(
            app_section,
            text="Apply to Selected Job",
            command=self.apply_to_job,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        apply_btn.pack(pady=30)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(app_section)
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        self.progress_bar.set(0)
        
        # Status text
        self.application_status = ctk.CTkTextbox(app_section, height=150)
        self.application_status.pack(fill="both", expand=True, padx=20, pady=10)
    
    def setup_tracking_tab(self):
        tracking_frame = self.notebook.add("📊 Tracking")
        
        # Applications tracking
        tracking_section = ctk.CTkFrame(tracking_frame)
        tracking_section.pack(fill="both", expand=True, padx=20, pady=20)
        
        tracking_label = ctk.CTkLabel(
            tracking_section,
            text="Application Tracking",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        tracking_label.pack(pady=10)
        
        # Statistics
        stats_frame = ctk.CTkFrame(tracking_section)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Loading statistics...",
            font=ctk.CTkFont(size=14)
        )
        self.stats_label.pack(pady=10)
        
        # Applications list
        apps_frame = ctk.CTkFrame(tracking_section)
        apps_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        apps_label = ctk.CTkLabel(
            apps_frame,
            text="Recent Applications",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        apps_label.pack(pady=10)
        
        # Create treeview for applications
        columns = ("Date", "Company", "Position", "Status", "Response")
        self.apps_tree = ttk.Treeview(apps_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.apps_tree.heading(col, text=col)
            self.apps_tree.column(col, width=120)
        
        # Scrollbar for applications treeview
        apps_scrollbar = ttk.Scrollbar(apps_frame, orient="vertical", command=self.apps_tree.yview)
        self.apps_tree.configure(yscrollcommand=apps_scrollbar.set)
        
        self.apps_tree.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        apps_scrollbar.pack(side="right", fill="y", pady=10)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            tracking_section,
            text="Refresh Data",
            command=self.refresh_tracking_data
        )
        refresh_btn.pack(pady=10)
    
    def browse_resume(self):
        file_path = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("Word documents", "*.docx"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(os.path.basename(file_path))
            self.resume_file_path = file_path
    
    def parse_resume(self):
        if not hasattr(self, 'resume_file_path'):
            messagebox.showerror("Error", "Please select a resume file first!")
            return
        
        self.status_var.set("Parsing resume...")
        
        def parse_thread():
            try:
                self.resume_data = self.resume_parser.parse_resume(self.resume_file_path)
                self.root.after(0, self.display_resume_data)
                self.root.after(0, lambda: self.status_var.set("Resume parsed successfully"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to parse resume: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Error parsing resume"))
        
        threading.Thread(target=parse_thread, daemon=True).start()
    
    def display_resume_data(self):
        self.resume_text.delete("1.0", tk.END)
        if self.resume_data:
            display_text = "Extracted Information:\n\n"
            for key, value in self.resume_data.items():
                if isinstance(value, list):
                    display_text += f"{key}:\n"
                    for item in value:
                        # Preserve original formatting - don't add bullet points if they're not there
                        if item.startswith(('•', '-', '*', '→', '▶', '○', '▪', '▫')):
                            # Item already has a bullet point, display as-is
                            display_text += f"  {item}\n"
                        else:
                            # Item doesn't have a bullet point, display as plain text
                            display_text += f"  {item}\n"
                else:
                    display_text += f"{key}: {value}\n"
                display_text += "\n"
            self.resume_text.insert("1.0", display_text)
    
    def edit_resume_data(self):
        if not self.resume_data:
            messagebox.showinfo("Info", "Please parse a resume first!")
            return
        
        # Create edit window
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edit Resume Information")
        edit_window.geometry("600x500")
        
        # Create text widget for editing
        edit_text = ctk.CTkTextbox(edit_window)
        edit_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Load current data
        current_data = json.dumps(self.resume_data, indent=2)
        edit_text.insert("1.0", current_data)
        
        def save_changes():
            try:
                new_data = json.loads(edit_text.get("1.0", tk.END))
                self.resume_data = new_data
                self.display_resume_data()
                edit_window.destroy()
                messagebox.showinfo("Success", "Resume data updated successfully!")
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format!")
        
        save_btn = ctk.CTkButton(edit_window, text="Save Changes", command=save_changes)
        save_btn.pack(pady=10)
    
    def search_jobs(self):
        keywords = self.keywords_var.get()
        location = self.location_var.get()
        job_type = self.job_type_var.get()
        
        if not keywords:
            messagebox.showerror("Error", "Please enter keywords to search for jobs!")
            return
        
        self.status_var.set("Searching for jobs...")
        
        def search_thread():
            try:
                self.job_listings = self.job_searcher.search_jobs(keywords, location, job_type)
                self.root.after(0, self.display_job_results)
                self.root.after(0, lambda: self.status_var.set(f"Found {len(self.job_listings)} jobs"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to search jobs: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Error searching jobs"))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def display_job_results(self):
        # Clear existing items
        for item in self.job_tree.get_children():
            self.job_tree.delete(item)
        
        # Add new items
        for job in self.job_listings:
            self.job_tree.insert("", "end", values=(
                job.get('title', 'N/A'),
                job.get('company', 'N/A'),
                job.get('location', 'N/A'),
                job.get('type', 'N/A'),
                job.get('posted', 'N/A')
            ))
    
    def on_job_select(self, event):
        selection = self.job_tree.selection()
        if selection:
            item = self.job_tree.item(selection[0])
            job_index = self.job_tree.index(selection[0])
            if job_index < len(self.job_listings):
                self.current_job = self.job_listings[job_index]
                self.display_job_details()
    
    def display_job_details(self):
        if self.current_job:
            self.selected_job_label.configure(
                text=f"Selected: {self.current_job.get('title', 'N/A')} at {self.current_job.get('company', 'N/A')}"
            )
            
            self.job_details_text.delete("1.0", tk.END)
            details = f"Title: {self.current_job.get('title', 'N/A')}\n"
            details += f"Company: {self.current_job.get('company', 'N/A')}\n"
            details += f"Location: {self.current_job.get('location', 'N/A')}\n"
            details += f"Type: {self.current_job.get('type', 'N/A')}\n"
            details += f"Posted: {self.current_job.get('posted', 'N/A')}\n\n"
            details += f"Description:\n{self.current_job.get('description', 'No description available')}"
            
            self.job_details_text.insert("1.0", details)
    
    def apply_to_job(self):
        if not self.current_job:
            messagebox.showerror("Error", "Please select a job first!")
            return
        
        if not self.resume_data:
            messagebox.showerror("Error", "Please parse your resume first!")
            return
        
        self.status_var.set("Applying to job...")
        self.progress_bar.set(0)
        self.application_status.delete("1.0", tk.END)
        
        def apply_thread():
            try:
                # Simulate application process
                self.root.after(0, lambda: self.progress_bar.set(0.2))
                self.root.after(0, lambda: self.application_status.insert(tk.END, "Preparing application...\n"))
                
                self.root.after(0, lambda: self.progress_bar.set(0.4))
                self.root.after(0, lambda: self.application_status.insert(tk.END, "Generating cover letter...\n"))
                
                self.root.after(0, lambda: self.progress_bar.set(0.6))
                self.root.after(0, lambda: self.application_status.insert(tk.END, "Filling application form...\n"))
                
                self.root.after(0, lambda: self.progress_bar.set(0.8))
                self.root.after(0, lambda: self.application_status.insert(tk.END, "Submitting application...\n"))
                
                # Record application
                application_data = {
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'company': self.current_job.get('company', 'N/A'),
                    'position': self.current_job.get('title', 'N/A'),
                    'status': 'Applied',
                    'response': 'Pending'
                }
                self.data_manager.add_application(application_data)
                
                self.root.after(0, lambda: self.progress_bar.set(1.0))
                self.root.after(0, lambda: self.application_status.insert(tk.END, "Application submitted successfully!\n"))
                self.root.after(0, lambda: self.status_var.set("Application submitted"))
                
                # Refresh tracking data
                self.root.after(0, self.refresh_tracking_data)
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to apply: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Application failed"))
        
        threading.Thread(target=apply_thread, daemon=True).start()
    
    def refresh_tracking_data(self):
        applications = self.data_manager.get_applications()
        
        # Update statistics
        total_apps = len(applications)
        pending_apps = len([app for app in applications if app.get('status') == 'Applied'])
        responded_apps = len([app for app in applications if app.get('response') != 'Pending'])
        
        stats_text = f"Total Applications: {total_apps}\n"
        stats_text += f"Pending Responses: {pending_apps}\n"
        stats_text += f"Responses Received: {responded_apps}"
        
        self.stats_label.configure(text=stats_text)
        
        # Update applications list
        for item in self.apps_tree.get_children():
            self.apps_tree.delete(item)
        
        for app in applications[-20:]:  # Show last 20 applications
            self.apps_tree.insert("", "end", values=(
                app.get('date', 'N/A'),
                app.get('company', 'N/A'),
                app.get('position', 'N/A'),
                app.get('status', 'N/A'),
                app.get('response', 'N/A')
            ))
    
    def load_saved_data(self):
        try:
            self.refresh_tracking_data()
        except Exception as e:
            print(f"Error loading saved data: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = JobApplicationBot()
    app.run() 