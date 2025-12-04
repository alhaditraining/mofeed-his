# Al-Mofeed HIS

A custom Frappe app for the Al-Mofeed Hospital Information System.

## Features

- Hospital and Clinic management
- Patient Extension with Iraqi localization
- Custom multi-language login page (Arabic/English/Kurdish)
- Healthcare theme with RTL support
- MRN (Medical Record Number) generation

## Installation

```bash
cd ~/frappe-bench
bench get-app mofeed_his /path/to/mofeed_his
bench --site yoursite install-app mofeed_his
```

## MRN (Medical Record Number) Generation

### Design Overview

Each patient receives a unique, facility-prefixed MRN in the format:

```
{HOSPITAL_CODE}-{YEAR}-{RUNNING_NUMBER}
```

**Example:** `KRBHOSP-2025-000123`

### Components

- **HOSPITAL_CODE**: Unique code from the Hospital doctype (e.g., "KRBHOSP")
- **YEAR**: 4-digit year when the patient was registered
- **RUNNING_NUMBER**: 6-digit zero-padded sequence number, unique per hospital per year

### Design Choices

1. **Custom Field on Patient**: We add `custom_mrn` as a Custom Field on the Healthcare Patient doctype rather than modifying the core doctype. This ensures:
   - Compatibility with Healthcare module updates
   - Clean separation of concerns
   - Easy migration and backup
2. **Separate Sequence Table**: The `MRN Sequence` doctype tracks running numbers per hospital per year, allowing:
   - Automatic reset at year boundaries
   - Multi-facility support
   - Audit trail of sequence usage
3. **Server-side Hook (before_insert)**: MRN generation happens server-side before the patient record is saved:
   - Guarantees uniqueness through database-level locking
   - Works in concurrent environments
   - Cannot be bypassed by client-side code
4. **Database-level Locking**: Uses `SELECT ... FOR UPDATE` for thread-safe sequence generation:
   - Prevents duplicate MRNs in high-concurrency scenarios
   - Ensures atomic increment operations

### Configuration

1. **Create Hospital Records**: Before registering patients, create at least one Hospital with a unique code:
   ```
   Hospital Name: Karbala General Hospital
   Hospital Code: KRBHOSP
   ```
2. **Optional Default Hospital**: Set a default hospital in Mofeed HIS Settings (if the doctype exists) for facilities with a single hospital.

### Indexing

The `custom_mrn` field is configured with:
- `unique: 1` - Ensures no duplicate MRNs
- `search_index: 1` - Enables fast MRN lookups

### Hooks Configuration

See `hooks.py` for the complete hook configuration:

```python
doc_events = {
    "Patient": {
        "before_insert": "mofeed_his.mofeed_his.utils.mrn.generate_patient_mrn",
        "validate": "mofeed_his.mofeed_his.utils.mrn.validate_mrn_unique",
    }
}
```

## Doctypes

### Hospital

Master data for hospitals/facilities. Key fields:
- `hospital_name`: Name of the hospital
- `code`: Unique code for MRN prefix (e.g., "KRBHOSP")

### MRN Sequence

Tracks running MRN sequence per hospital per year:
- `hospital_code`: Hospital code prefix
- `year`: Year for the sequence
- `current_value`: Current running number

## License

MIT
