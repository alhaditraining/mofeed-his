# PDR – Al-Mofeed Hospital Information System (HIS)

## 1. Introduction

**Al-Mofeed HIS** is a hospital information system built on:

- ERPNext
- Healthcare App
- Custom App: `mofeed_his`

Target market: clinics, medical centers, and hospitals in Iraq.

Main goals:

- Manage patients, doctors, clinics, appointments, billing, insurance.
- Provide a unified medical record per patient.
- Offer Arabic-first UX with English/Kurdish support.
- Provide AI-assisted diagnosis, voice dictation, and medical document handling.

---

## 2. MVP Scope

The first release (MVP) focuses on:

- Outpatient Department flow (OPD Flow).
- Reception screen and patient flow.
- Doctor workbench (encounters, ICD-10, clinical notes, voice dictation).
- Basic billing + insurance integration.
- Uploading lab/radiology documents to the patient file.

Out of scope for MVP:

- Full inpatient (IPD) workflows.
- Deep LIS/RIS integration (placeholders only).
- Patient portal / mobile app.

---

## 3. Personas

- **Receptionist**: patient registration, appointment booking, check-in, queues.
- **Doctor**: encounters, clinical notes, diagnosis, orders, review medical record.
- **Accountant**: billing, payments, receivables, insurance finance.
- **Insurance Officer**: plans, coverage, co-pay, claim batches.
- **Admin / Manager**: clinics, doctors, reports, permissions.

---

## 4. Technical Architecture (High Level)

- **Core**: ERPNext + Frappe.
- **Modules used**: Accounts, Healthcare (Patient, Encounter, Appointment, etc.).
- **Custom App**: `mofeed_his`
  - Iraqi localization (fields, flows).
  - Insurance module.
  - Custom reception & doctor workspaces.
  - AI / voice / OCR integrations.
- **Custom Theme**: `mofeed_healthcare_theme`
  - Arabic RTL, fonts, colors, layouts for healthcare.

---

## 5. Core Data Model (Conceptual)

- **Hospital / Facility**
  - Name, code/prefix, location.
- **Clinic / Department**
  - Hospital, specialty, type, default services.
- **Healthcare Practitioner (Doctor)**
  - Name, specialty, clinics, schedule.
- **Patient**
  - MRN (with facility prefix), name, gender, DOB/age, national ID, phone, address, insurance link.
- **Appointment**
  - Patient, doctor, clinic, datetime, status.
- **Encounter (Visit)**
  - Patient, doctor, clinic, visit type, clinical notes, diagnosis, orders.
- **Billable Item / Service**
  - Service name, pricing (cash / insurance price lists).
- **Sales Invoice / Payment Entry**
  - Billing for visits/services, payments, outstanding amounts.
- **Insurance Company / Plan / Coverage Rule / Claim Batch**
  - Insurance definitions and claim management.
- **Medical Document**
  - Attached lab/radiology/report files linked to patient + encounter.

---

## 6. OPD Flow – Outpatient Department

High-level steps:

1. **Patient Registration**
   - Search by MRN, name, phone, national ID.
   - Create new patient with auto-generated MRN using facility prefix.
   - Avoid duplicates on national ID / phone where possible.

2. **Appointment Booking**
   - Choose clinic → doctor → time slot.
   - Support scheduled appointments and walk-in visits.
   - Allow reschedule/cancel with audit trail.

3. **Reception Check-in & Queues**
   - Dedicated **Reception Screen**:
     - Patient search.
     - Today’s appointments (filter by clinic/doctor).
     - Check-in button.
     - Waiting queue per doctor.
   - Display:
     - Insurance status.
     - Outstanding balance (optional).
     - Visit type (new / follow-up).

4. **Doctor Encounter**
   - Patient queue for each doctor.
   - Start/continue Encounter for selected patient.
   - Clinical notes, diagnosis, orders, file uploads.

5. **Billing**
   - Generate invoice for visit and services.
   - Cash / card / insurance / mixed.
   - Link invoice with encounter and patient.

---

## 7. Reception Screen (Functional Requirements)

- Single workspace for receptionist:
  - Fast search box.
  - List of today’s appointments.
  - List of arrived/check-in patients.
  - Per-doctor queues.
  - “New patient” and “New appointment” buttons.
- Arabic-first UI with RTL, large buttons, keyboard shortcuts.
- Integration with patient/appointment/encounter doctypes.

---

## 8. Doctor Workbench

- List of today’s patients (queue) with status (waiting, in progress, done).
- Open Encounter:
  - Patient demographics.
  - Clinical notes.
  - Diagnosis (ICD-10).
  - Orders placeholders (lab, radiology, prescription).
  - Medical documents (upload/view).
- Designed for English UI by default, with Arabic/Kurdish support where needed.

---

## 9. Diagnosis & ICD-10

- Use ICD-10 as the standard diagnosis coding system.
- Import full ICD-10 list into a searchable doctype or use existing Healthcare mapping.
- Features:
  - Fast search by code or description.
  - Multiple diagnoses per encounter.
  - Link diagnoses to billing and insurance rules.

---

## 10. Clinical Notes

- Structured and free-text clinical notes inside Encounter:
  - Chief Complaint
  - History of Present Illness (HPI)
  - Past Medical History
  - Medications
  - Allergies
  - Assessment & Plan
- Support:
  - Rich text.
  - Note templates per specialty (e.g., pediatrics, dermatology).
  - Re-use templates per doctor.

---

## 11. Voice Dictation (Doctor)

- Add microphone button inside Encounter for:
  - Clinical notes.
  - Summary/Assessment.
- Flow:
  - Doctor taps “Record”.
  - Voice is converted to text via Speech-to-Text (Whisper / cloud STT).
  - Text shown for review/edit, then saved into notes.
- Optional: store original audio file according to hospital policy.
- Language support:
  - Arabic (Iraqi medical dialect as possible).
  - English.
  - Kurdish in future.

---

## 12. AI-Assisted Diagnosis & Notes

- AI assistant available from doctor workbench to:
  - Suggest ICD-10 diagnoses based on clinical notes.
  - Summarize visit (SOAP style).
  - Improve/clean clinical notes wording.
  - Explain findings in patient-friendly language (optional).
- Implementation options:
  - Azure OpenAI / OpenAI API / local models via Ollama, etc.
- Doctor remains the final decision maker; AI suggestions are advisory only.

---

## 13. Medical Documents & OCR

- Upload lab and radiology documents as:
  - PDF, JPG, PNG (DICOM optional later).
- Attach to:
  - Patient.
  - Encounter/Visit.
- Optional OCR + AI extraction:
  - Extract test names, values, reference ranges.
  - Store them as Lab Result records.
- Provide a simple viewer to open documents from the medical record.

---

## 14. Unified Medical Record

Per patient, show a consolidated view:

- Demographics.
- Encounters / visits (timeline).
- Diagnoses (ICD-10).
- Prescriptions (future).
- Lab results.
- Radiology reports.
- Uploaded documents.
- Clinical notes.

---

## 15. Billing & Insurance

- **Billing**
  - Visit invoices (new visit, follow-up).
  - Service item billing (procedures, tests, etc.).
  - Multiple price lists (cash, insurance).
- **Insurance**
  - Insurance company, plans, coverage rules, co-pay.
  - Assign plan to patient.
  - Split invoice between patient and insurance.
  - Claim batch generation for insurers.

---

## 16. Multi-Language Support (Login & UI)

- System must support at least:
  - Arabic (primary for reception, accounting, nursing).
  - English (preferred by doctors and pharmacists).
  - Kurdish (planned; design must not block future addition).
- **Login screen**:
  - Username, password, **language selector** (ar/en/ku).
  - Selected language sets session language.
- **User preferences**:
  - Each user has a preferred language.
- Language switch button in header.
- All custom screens use translation keys, not hard-coded text.

---

## 17. Theme & UI Guidelines

- Custom healthcare theme:
  - Light, clean UI with medical color palette.
  - Proper Arabic RTL support.
  - Large controls for reception/touch screens.
- Layouts:
  - Reception workspace.
  - Doctor workspace.
  - Patient overview / medical record.
- Reusable UI components for:
  - Patient search.
  - Queues.
  - Clinical note panels.
  - Document upload.

---

## 18. Non-Functional Requirements

- **Performance**:
  - 20–30 concurrent users for MVP.
  - Search and main actions under ~3 seconds.
- **Security & Privacy**:
  - Role-based permissions (Admin, Receptionist, Doctor, Accountant, Insurance Officer).
  - Audit trail for changes on patient and medical data.
- **Reliability**:
  - Daily backups at minimum.
  - Logging and monitoring for production.
- **Compliance mindset**:
  - Design with healthcare privacy best practices in mind (HIPAA-like thinking, adapted to local context).

---

## 19. Roadmap Overview (High Level)

- **Milestone 0 – Theme & UI Foundation**
  - Login + multi-language.
  - Healthcare theme.
  - Reception & doctor layout skeleton.
- **Milestone 1 – OPD Flow**
  - Registration, appointments, reception, queues.
- **Milestone 2 – Doctor Workbench**
  - Clinical notes, ICD-10, voice dictation, AI assist.
- **Milestone 3 – Billing & Insurance**
  - Visit billing, insurance plans, claim batch.
- **Milestone 4 – Medical Documents & OCR**
  - Upload & OCR.
- **Milestone 5 – Unified Medical Record & Reports**
  - Timeline & management reports.
