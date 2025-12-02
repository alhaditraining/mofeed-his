# Al-Mofeed HIS

Hospital Information System for clinics, medical centers, and hospitals in Iraq.

Built on top of **ERPNext + Healthcare** as a custom Frappe app.

## Features

- **Multi-language Support**: Arabic (primary), English, Kurdish
- **Patient Management**: Extended patient information with Iraqi healthcare-specific fields
- **Hospital/Clinic Management**: Manage multiple facilities and departments
- **Custom Login Page**: Branded login with language selection and RTL support

## Installation

This app requires the following Frappe apps to be installed:

1. Frappe Framework
2. ERPNext
3. Healthcare

### Install via Bench

```bash
# Add the app to your bench
bench get-app mofeed_his https://github.com/alhaditraining/mofeed-his.git

# Install on your site
bench --site your-site.local install-app mofeed_his

# Run migrations
bench --site your-site.local migrate
```

## Doctypes

### Hospital
Manage hospitals and facilities with unique codes and MRN prefixes.

### Clinic
Manage clinics/departments linked to hospitals with specialty and service configurations.

### Patient Extension
Extends the ERPNext Healthcare Patient with:
- National ID
- Custom MRN with facility prefix
- Insurance information
- Preferred language (ar/en/ku)

## License

MIT
