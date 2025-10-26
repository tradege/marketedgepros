#!/usr/bin/env python3
"""
Course Drip Campaign Cron Job
Run this daily to send course module emails

Add to crontab:
0 9 * * * cd /path/to/backend && python3 run_drip_campaign.py
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import create_app
from src.tasks.course_drip_campaign import send_course_module_emails

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        print("Starting course drip campaign...")
        send_course_module_emails()
        print("Course drip campaign completed!")

