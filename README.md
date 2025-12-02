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

## Custom App: mofeed_his

The `mofeed_his` Frappe app includes:

### Pages / Workspaces

- **Reception Console** (`/app/reception-console`) - Unified workspace for receptionists:
  - Patient search bar
  - Today's appointments table
  - Waiting queue by doctor
  - Selected patient details card
  - Quick actions: Check-in, View File, Billing

### Installation

```bash
cd frappe-bench
bench get-app mofeed_his
bench install-app mofeed_his
```

## Tech Stack (planned)

- ERPNext + Frappe Framework
- Healthcare App
- Custom App: `mofeed_his`
- Custom Theme: `mofeed_healthcare_theme`
- Optional AI services (voice dictation, diagnosis assistant, OCR)
