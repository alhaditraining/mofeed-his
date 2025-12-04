"""
Reception Console Page
Al-Mofeed Hospital Information System

This page provides a unified workspace for receptionists to manage:
- Patient search
- Today's appointments
- Waiting queues
- Check-in operations
"""

import frappe


def get_context(context):
    """
    Provide context data for the reception console page.
    This will be used when the template is rendered.
    """
    context.no_cache = 1
    
    # Placeholder data for appointments
    context.appointments = [
        {
            "id": "APT-001",
            "time": "09:00",
            "patient_name": "Ali Hassan",
            "patient_id": "PAT-001",
            "doctor": "Dr. Ahmed",
            "department": "Dermatology",
            "status": "Booked"
        },
        {
            "id": "APT-002",
            "time": "09:15",
            "patient_name": "Zainab Ahmed",
            "patient_id": "PAT-002",
            "doctor": "Dr. Ahmed",
            "department": "Dermatology",
            "status": "Arrived"
        },
        {
            "id": "APT-003",
            "time": "09:30",
            "patient_name": "Ahmad Saeed",
            "patient_id": "PAT-003",
            "doctor": "Dr. Fatima",
            "department": "General",
            "status": "Booked"
        }
    ]
    
    # Placeholder data for waiting queue
    context.queue = [
        {
            "position": 1,
            "patient_name": "Zainab Ahmed",
            "patient_id": "PAT-002",
            "arrival_time": "09:10",
            "wait_time": "5 min"
        },
        {
            "position": 2,
            "patient_name": "Ali Hassan",
            "patient_id": "PAT-001",
            "arrival_time": "09:05",
            "wait_time": "10 min"
        }
    ]
    
    # Placeholder data for selected patient
    context.selected_patient = {
        "name": "Zainab Ahmed",
        "mrn": "2025-KRB-00123",
        "insurance": "Al-Waha",
        "coverage": "90%",
        "outstanding": 0,
        "phone": "0770 XXX XXX",
        "visit_type": "Follow-up"
    }
    
    return context
