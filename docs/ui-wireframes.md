# UI Wireframes – Al-Mofeed Hospital Information System (HIS)

This document contains low-fidelity wireframes for the main screens of the Al-Mofeed HIS product.  
The goal is to define layout, structure, and UX flow before building the actual theme or pages inside ERPNext/Frappe.

---

# 1. Login Screen (Multi-Language)

┌──────────────────────────────────────────────┐
│ [ Logo ] │
│ المفيد لإدارة المستشفيات HIS │
│ Al-Mofeed Hospital Information │
├──────────────────────────────────────────────┤
│ Username / اسم المستخدم │
│ [ ....................................... ] │
│ │
│ Password / كلمة المرور │
│ [ ************** 👁 ] │
│ │
│ Language / اللغة / زمان: [ عربي ▼ ] │
│ │
│ [ Login – تسجيل الدخول ] │
│ │
│ ✔ تذكرني | Remember me Forgot? │
└──────────────────────────────────────────────┘

yaml
Copy code

### Notes:
- Language options: **Arabic / English / Kurdish**
- RTL enabled when Arabic chosen
- Button should be large and high-contrast
- Keep it clean, medical-themed white/blue/gray

---

# 2. Reception Workspace (OPD Flow – Check-in)

┌──────────────────────────────────────────────┐
│ Al-Mofeed HIS – Reception Workspace │
├──────────────────────────────────────────────┤

Search Patient:
[ .......................................... ] (F2)

[ New Patient ] [ New Appointment ] [ Today’s Appointments ]

────────────────────────────────────────────────────────────────

Appointments (Today)
┌──────────────────────────────────────────────┐
│ Time | Patient Name | Doctor | Status │
│ 09:00 | Ali Hassan | Dr. X | Booked │
│ 09:15 | Zainab Ahmed | Dr. X | Arrived │
│ 09:30 | Ahmad Saeed | Dr. Y | Booked │
└──────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────

Waiting Queue (Dr. X)
┌──────────────────────────────────────────────┐
│ # | Patient Name | Arrival Time │
│ 1 | Zainab Ahmed | 09:10 │
│ 2 | Ali Hassan | 09:00 │
└──────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────

Selected Patient
┌──────────────────────────────────────────────┐
│ Name: Zainab Ahmed │
│ MRN: 2025-KRB-00123 │
│ Insurance: Al-Waha – 90% coverage │
│ Outstanding: 0 │
│ │
│ [ Check-In ] [ View File ] [ Billing ] │
└──────────────────────────────────────────────┘

└──────────────────────────────────────────────┘

yaml
Copy code

### Notes:
- Main navigation minimized.
- Large elements (suited for front desk speed).
- Search must support name/phone/national ID.
- Queue auto-sorted by arrival time.

---

# 3. Doctor Workbench

┌───────────────────────────────────────────────────────────────┐
│ Dr. Ahmed – Dermatology Clinic │
├────────────────────────────────────────────────────────────────┤

Left Panel (Queue) Encounter Panel
─────────────────────────────── ────────────────────────────────
• Patient Queue Patient: Zainab Ahmed

Zainab Ahmed (Arrived) MRN: 2025-KRB-00123

Ali Hassan Age: 32

Ahmad Saeed Insurance: Al-Waha (90%)
─────────────────────────────── ────────────────────────────────

Clinical Notes Diagnosis (ICD-10)
─────────────────────────────── ────────────────────────────────
Chief Complaint: Search ICD-10:
[...................................] [................................]

History of Present Illness: Selected Diagnoses:
[...................................] • L20.9 – Atopic dermatitis
• R21 – Rash

Past Medical History:
[...................................]

Medications:
[...................................]

Assessment & Plan:
[...................................]

[ 🎤 Voice Dictation ] [ AI Assist ] [ Save Encounter ]
─────────────────────────────────────────────────────────────

Documents Panel (Right Side)
───────────────────────────────────────────────
• Upload Document (PDF/JPG)
• View Lab Reports
• View Radiology Images
───────────────────────────────────────────────

└───────────────────────────────────────────────────────────────┘

yaml
Copy code

### Notes:
- English UI by default (doctors in Iraq prefer English).
- Voice dictation button must be always visible.
- AI Assist shows suggestions:
  - summarize  
  - suggest diagnosis  
  - generate SOAP  
- Documents shown in side panel for quick review.

---

# 4. Patient Medical Record (Unified View)

┌──────────────────────────────────────────────┐
│ Patient Medical Record – Zainab Ahmed │
├──────────────────────────────────────────────┤

Patient Info
───────────────────────────────────────────────
• MRN: 2025-KRB-00123
• Gender: Female
• Age: 32
• Phone: 0770 XXX XXX
• Insurance: Al-Waha – Plan A (90%)

Timeline
───────────────────────────────────────────────
• 2025-02-01 – Dermatology Visit (Dr. Ahmed)
- Diagnosis: L20.9, R21
- Prescription: Cetirizine
- Notes: mild eczema flare

• 2024-12-15 – General Checkup
- Diagnosis: Z00.0
- Labs: CBC normal
- Attached Document (PDF)

• 2024-10-05 – Dermatology Visit
- Rash evaluation
- Photo attached (JPG)

───────────────────────────────────────────────

All Documents
───────────────────────────────────────────────
• 2025-02-01_lab_report.pdf
• 2024-12-15_cbc.pdf
• 2024-10-05_skin_photo.jpg

Medication Summary
───────────────────────────────────────────────
• Cetirizine 10mg – Daily
• Betamethasone Cream – PRN

└──────────────────────────────────────────────┘

markdown
Copy code

### Notes:
- Timeline must be scrollable and sorted by date.
- Unified view replaces many ERPNext screens.
- Should open from Reception + Doctor Workbench.

---

# 5. UI/UX Guidelines Summary

## Color Scheme (Healthcare Clean)
- Primary: **#0C82E6** (Medical Blue)
- Secondary: **#26C6DA** (Cyan)
- Accent: **#4CAF50** (Green)
- Background: **#F9FAFB**
- Text: **#1F2937**

## Fonts
- Arabic: **Cairo**, **Noto Sans Arabic**
- English: **Inter**, **Roboto**

## RTL/Arabic Rules
- All reception screens default RTL.
- Doctor screens default LTR unless Arabic selected.
- Numbers always LTR even داخل النص العربي.

## Buttons
- Big, rounded, with icon.
- Primary actions highlighted.
- Keyboard shortcuts:
  - F1 → New patient  
  - F2 → Search  
  - F3 → New appointment  
  - F4 → Check-in  

## Performance
- All search bars must respond within <2 seconds.
- Queues must refresh automatically via socket.

---

# 6. Notes for Developers

- All UI should be built using standard Frappe/Jinja + custom JS.
- Avoid hard-coded Arabic; use translation keys (`_("text")`).
- Reception & Doctor are **Workspace Pages** (Desk pages).
- For future mobile use, keep layouts simple and responsive.
