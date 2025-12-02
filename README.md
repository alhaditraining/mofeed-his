# Al-Mofeed HIS

Hospital Information System for clinics and hospitals in Iraq, built on top of **ERPNext + Healthcare + Custom App**.

This repository contains:

- Product definition and documentation
- Roadmap and milestones
- Source code for the custom ERPNext app (`mofeed_his`) and healthcare theme (later)

## Documentation

- [Product Definition (PDR)](docs/PDR.md)
- [Roadmap](docs/roadmap.md)
- [UI Wireframes](docs/ui-wireframes.md)

## Tech Stack (planned)

- ERPNext + Frappe Framework
- Healthcare App
- Custom App: `mofeed_his`
- Custom Theme: `mofeed_healthcare_theme`
- Optional AI services (voice dictation, diagnosis assistant, OCR)

## Installation

### Prerequisites

- Frappe Bench installed and configured
- ERPNext installed
- Healthcare app installed

### Install the mofeed_his App

```bash
# Navigate to your bench directory
cd ~/frappe-bench

# Get the app from this repository
bench get-app mofeed_his https://github.com/alhaditraining/mofeed-his.git

# Install on your site
bench --site your-site.local install-app mofeed_his

# Run migrations
bench --site your-site.local migrate
```

## App Structure

```
mofeed_his/
├── mofeed_his/          # Module: Mofeed HIS
│   └── doctype/
│       ├── hospital/           # Hospital/Facility management
│       ├── clinic/             # Clinic/Department management
│       ├── clinic_service/     # Child table for clinic services
│       └── patient_extension/  # Extended patient info (Iraqi healthcare)
├── config/
│   ├── desktop.py       # Module sidebar configuration
│   └── mofeed_his.py    # Module item links
├── templates/pages/
│   └── mofeed_login.*   # Custom multi-language login page
├── public/
│   ├── css/             # Stylesheets (login, desk)
│   └── js/              # JavaScript (login, desk)
└── hooks.py             # App configuration and hooks
```

## Features

### Milestone 0 (Current)
- ✅ Frappe app skeleton with standard layout
- ✅ Core doctypes: Hospital, Clinic, Patient Extension
- ✅ Custom login page with multi-language support (Arabic, English, Kurdish)
- ✅ RTL/LTR support based on language selection
- ✅ Healthcare-themed UI (Medical Blue color scheme)

## License

MIT
