# Mofeed HIS - Custom ERPNext App

## Overview

This is the custom Frappe app for Al-Mofeed Hospital Information System (HIS), built on top of ERPNext and the Healthcare module.

## Main Files

### 1. hooks.py

**Location:** `mofeed_his/hooks.py`

**Purpose:** Main configuration file that defines how the mofeed_his app integrates with the Frappe/ERPNext framework.

**Key Integration Points:**
- `app_include_css/js`: Loads custom CSS/JS on all desk pages
- `website_route_rules`: Routes `/login` to custom login page
- `doctype_js`: Extends Patient, Appointment, and Encounter forms
- `doc_events`: Hooks into lifecycle events (before_insert, after_insert, validate)
- `fixtures`: Exports custom fields, translations, and print formats
- `scheduler_events`: Background tasks for queue management
- `permission_query_conditions`: Row-level security for multi-facility

---

### 2. DocTypes

#### Hospital (`mofeed_his/mofeed_his/doctype/hospital/`)

**Files:**
- `hospital.json` - DocType schema definition
- `hospital.py` - Controller with business logic

**Purpose:** Represents a healthcare facility (hospital, clinic, medical center).

**Key Features:**
- Multi-language support (English + Arabic names)
- MRN prefix for unique patient numbering per facility
- Links to ERPNext Price Lists for billing
- Governorate selection for Iraqi regions
- Working hours child table for scheduling

**Integration:**
- Generates unique Medical Record Numbers (MRN)
- Links to ERPNext Currency and Price List
- Patient Extension links back to Hospital

---

#### Clinic (`mofeed_his/mofeed_his/doctype/clinic/`)

**Files:**
- `clinic.json` - DocType schema definition  
- `clinic.py` - Controller with business logic

**Purpose:** Represents a department/specialty within a hospital.

**Key Features:**
- Links to parent Hospital
- Specialty classification (Dermatology, Cardiology, etc.)
- Consultation and follow-up fee settings
- Doctor and nurse assignment tables
- Appointment slot configuration
- Queue management methods

**Integration:**
- Links to Healthcare Practitioner for doctors
- Links to Medical Department for specialty
- Patient Appointment linked to Clinic
- Feeds into reception workspace queues

---

#### Patient Extension (`mofeed_his/mofeed_his/doctype/patient_extension/`)

**Files:**
- `patient_extension.json` - DocType schema definition
- `patient_extension.py` - Controller + doc_events handlers

**Purpose:** Extends the standard Healthcare Patient with Iraqi-specific fields.

**Key Features:**
- Unique MRN with hospital prefix (e.g., 2025-KRB-00001)
- Iraqi National ID validation
- Governorate/district location
- Insurance company, plan, and coverage
- Patient type (Cash, Insured, VIP, etc.)
- Emergency contact information
- Medical alerts for staff

**Integration:**
- 1:1 link with Healthcare Patient doctype
- Auto-created via doc_events when Patient inserted
- Fields synced back to Patient custom fields
- Insurance links to ERPNext Customer

---

### 3. Custom Login Page

#### Template (`mofeed_his/templates/pages/mofeed_login.html`)

**Purpose:** Custom login page with multi-language support and medical-themed UI.

**Features:**
- Language selector (Arabic, English, Kurdish)
- RTL support for Arabic/Kurdish
- Password visibility toggle
- Remember me functionality
- Clean, medical-themed design
- Responsive layout for tablets/mobile

**Integration:**
- Uses Frappe's CSRF token protection
- Calls `frappe.call('login')` for authentication
- Sets user language preference after login
- Redirects to role-based home page

---

#### Controller (`mofeed_his/www/mofeed_login.py`)

**Purpose:** Python controller for the login page template.

**Functions:**
- `get_context()`: Builds template context with logo, language, version
- `get_current_language()`: Detects language from URL/session/browser
- `get_home_page_for_user()`: Returns role-based redirect URL
- `login_with_language()`: Custom login API with language setting
- `set_session_language()`: API to change language before login

**Integration:**
- Route defined in hooks.py website_route_rules
- Extends Frappe's web.html base template
- Uses Frappe session and authentication

---

## Installation

```bash
# From frappe-bench directory
bench get-app mofeed_his [repo_url]
bench --site [site_name] install-app mofeed_his
```

## Dependencies

- Frappe Framework (v15+)
- ERPNext (v15+)
- Healthcare Module

## File Structure

```
mofeed_his/
├── __init__.py
├── hooks.py                              # Main configuration
├── modules.txt
├── mofeed_his/
│   ├── __init__.py
│   └── doctype/
│       ├── hospital/
│       │   ├── __init__.py
│       │   ├── hospital.json
│       │   └── hospital.py
│       ├── clinic/
│       │   ├── __init__.py
│       │   ├── clinic.json
│       │   └── clinic.py
│       └── patient_extension/
│           ├── __init__.py
│           ├── patient_extension.json
│           └── patient_extension.py
├── templates/
│   └── pages/
│       └── mofeed_login.html             # Custom login template
├── www/
│   └── mofeed_login.py                   # Login page controller
└── public/
    ├── css/
    └── js/
```

## License

MIT License
