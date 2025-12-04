/**
 * Reception Console Page
 * Al-Mofeed Hospital Information System
 * 
 * This page provides a unified workspace for receptionists to:
 * - Search patients
 * - View today's appointments
 * - Manage waiting queues
 * - Check-in patients
 */

frappe.pages['reception-console'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: __('Reception Console'),
        single_column: true
    });

    // Store page reference
    wrapper.reception_console = new ReceptionConsole(page);
};

frappe.pages['reception-console'].on_page_show = function(wrapper) {
    // Refresh data when page is shown
    if (wrapper.reception_console) {
        wrapper.reception_console.refresh();
    }
};

/**
 * ReceptionConsole Class
 * Main controller for the Reception Console page
 */
class ReceptionConsole {
    constructor(page) {
        this.page = page;
        this.wrapper = $(page.body);
        
        // Placeholder data for appointments
        this.appointments = [
            {
                id: 'APT-001',
                time: '09:00',
                patient_name: 'Ali Hassan',
                patient_id: 'PAT-001',
                doctor: 'Dr. Ahmed',
                department: 'Dermatology',
                status: 'Booked'
            },
            {
                id: 'APT-002',
                time: '09:15',
                patient_name: 'Zainab Ahmed',
                patient_id: 'PAT-002',
                doctor: 'Dr. Ahmed',
                department: 'Dermatology',
                status: 'Arrived'
            },
            {
                id: 'APT-003',
                time: '09:30',
                patient_name: 'Ahmad Saeed',
                patient_id: 'PAT-003',
                doctor: 'Dr. Fatima',
                department: 'General',
                status: 'Booked'
            }
        ];

        // Placeholder data for waiting queue
        this.queue = [
            {
                position: 1,
                patient_name: 'Zainab Ahmed',
                patient_id: 'PAT-002',
                arrival_time: '09:10',
                wait_time: '5 min'
            },
            {
                position: 2,
                patient_name: 'Ali Hassan',
                patient_id: 'PAT-001',
                arrival_time: '09:05',
                wait_time: '10 min'
            }
        ];

        // Selected patient placeholder
        this.selected_patient = {
            name: 'Zainab Ahmed',
            mrn: '2025-KRB-00123',
            insurance: 'Al-Waha',
            coverage: '90%',
            outstanding: 0,
            phone: '0770 XXX XXX',
            visit_type: 'Follow-up'
        };

        this.init();
    }

    /**
     * Initialize the Reception Console
     */
    init() {
        this.make();
        this.bind_events();
        this.setup_keyboard_shortcuts();
    }

    /**
     * Render the page content
     */
    make() {
        this.wrapper.html(frappe.render_template('reception_console', {
            appointments: this.appointments,
            queue: this.queue,
            selected_patient: this.selected_patient
        }));
    }

    /**
     * Bind event handlers
     */
    bind_events() {
        let me = this;

        // Search input handler
        this.wrapper.find('#patient-search').on('keyup', frappe.utils.debounce(function(e) {
            let search_term = $(this).val();
            if (search_term.length >= 2) {
                me.search_patient(search_term);
            }
        }, 300));

        // New Patient button
        this.wrapper.find('.btn-new-patient').on('click', function() {
            me.new_patient();
        });

        // New Appointment button
        this.wrapper.find('.btn-new-appointment').on('click', function() {
            me.new_appointment();
        });

        // Today's Appointments button
        this.wrapper.find('.btn-today-appointments').on('click', function() {
            me.show_today_appointments();
        });

        // Appointment row selection
        this.wrapper.find('.appointment-row').on('click', function() {
            me.select_appointment($(this));
        });

        // Queue row selection
        this.wrapper.find('.queue-row').on('click', function() {
            me.select_queue_patient($(this));
        });

        // Check-in buttons
        this.wrapper.find('.btn-check-in, #btn-check-in').on('click', function() {
            me.check_in_patient();
        });

        // View File button
        this.wrapper.find('.btn-view-file, #btn-view-file').on('click', function() {
            me.view_patient_file();
        });

        // Billing button
        this.wrapper.find('#btn-billing').on('click', function() {
            me.open_billing();
        });

        // Doctor queue filter
        this.wrapper.find('#doctor-queue-filter').on('change', function() {
            me.filter_queue($(this).val());
        });
    }

    /**
     * Setup keyboard shortcuts
     */
    setup_keyboard_shortcuts() {
        let me = this;

        // F1 - New Patient
        frappe.ui.keys.add_shortcut({
            shortcut: 'f1',
            action: () => me.new_patient(),
            description: __('New Patient'),
            page: this.page
        });

        // F2 - Focus Search
        frappe.ui.keys.add_shortcut({
            shortcut: 'f2',
            action: () => me.wrapper.find('#patient-search').focus(),
            description: __('Search Patient'),
            page: this.page
        });

        // F3 - New Appointment
        frappe.ui.keys.add_shortcut({
            shortcut: 'f3',
            action: () => me.new_appointment(),
            description: __('New Appointment'),
            page: this.page
        });

        // F4 - Check-in
        frappe.ui.keys.add_shortcut({
            shortcut: 'f4',
            action: () => me.check_in_patient(),
            description: __('Check-in Patient'),
            page: this.page
        });
    }

    /**
     * Refresh the page data
     */
    refresh() {
        // TODO: Fetch fresh data from server
        // For now, just re-render with placeholder data
        this.make();
        this.bind_events();
        frappe.show_alert({
            message: __('Reception Console refreshed'),
            indicator: 'green'
        }, 3);
    }

    /**
     * Search for a patient
     * @param {string} search_term - Search query
     */
    search_patient(search_term) {
        // TODO: Implement actual patient search via API
        // For now, show placeholder message
        console.log('Searching for patient:', search_term);
        frappe.show_alert({
            message: __('Searching for: {0}', [search_term]),
            indicator: 'blue'
        }, 2);
    }

    /**
     * Open new patient form
     */
    new_patient() {
        // TODO: Connect to actual Patient doctype
        frappe.show_alert({
            message: __('Opening New Patient form...'),
            indicator: 'blue'
        }, 2);
        
        // This will work when connected to ERPNext
        // frappe.new_doc('Patient');
    }

    /**
     * Open new appointment form
     */
    new_appointment() {
        // TODO: Connect to actual Appointment doctype
        frappe.show_alert({
            message: __('Opening New Appointment form...'),
            indicator: 'blue'
        }, 2);
        
        // This will work when connected to ERPNext
        // frappe.new_doc('Patient Appointment');
    }

    /**
     * Show today's appointments
     */
    show_today_appointments() {
        frappe.show_alert({
            message: __('Filtering today\'s appointments...'),
            indicator: 'blue'
        }, 2);
    }

    /**
     * Select an appointment row
     * @param {jQuery} $row - Selected row element
     */
    select_appointment($row) {
        // Remove selection from other rows
        this.wrapper.find('.appointment-row').removeClass('selected');
        // Add selection to clicked row
        $row.addClass('selected');
        
        // Update selected patient details
        let appointment_id = $row.data('appointment-id');
        this.load_patient_details(appointment_id);
    }

    /**
     * Select a patient from queue
     * @param {jQuery} $row - Selected row element
     */
    select_queue_patient($row) {
        let patient_id = $row.data('patient-id');
        this.load_patient_details_by_id(patient_id);
    }

    /**
     * Load patient details for selected appointment
     * @param {string} appointment_id - Appointment ID
     */
    load_patient_details(appointment_id) {
        // TODO: Fetch actual patient details from server
        console.log('Loading patient for appointment:', appointment_id);
        frappe.show_alert({
            message: __('Loading patient details...'),
            indicator: 'blue'
        }, 1);
    }

    /**
     * Load patient details by patient ID
     * @param {string} patient_id - Patient ID
     */
    load_patient_details_by_id(patient_id) {
        // TODO: Fetch actual patient details from server
        console.log('Loading patient:', patient_id);
    }

    /**
     * Check-in the selected patient
     */
    check_in_patient() {
        // TODO: Implement actual check-in functionality
        frappe.confirm(
            __('Check-in {0}?', [this.selected_patient.name]),
            () => {
                frappe.show_alert({
                    message: __('Patient checked in successfully!'),
                    indicator: 'green'
                }, 3);
            }
        );
    }

    /**
     * Open patient medical file
     */
    view_patient_file() {
        // TODO: Navigate to patient medical record
        frappe.show_alert({
            message: __('Opening patient file for: {0}', [this.selected_patient.name]),
            indicator: 'blue'
        }, 2);
        
        // This will work when connected to ERPNext
        // frappe.set_route('Form', 'Patient', this.selected_patient.mrn);
    }

    /**
     * Open billing for selected patient
     */
    open_billing() {
        // TODO: Navigate to billing
        frappe.show_alert({
            message: __('Opening billing for: {0}', [this.selected_patient.name]),
            indicator: 'blue'
        }, 2);
    }

    /**
     * Filter waiting queue by doctor
     * @param {string} doctor_id - Doctor ID to filter by
     */
    filter_queue(doctor_id) {
        // TODO: Implement actual queue filtering
        console.log('Filtering queue for doctor:', doctor_id);
        frappe.show_alert({
            message: __('Filtering queue...'),
            indicator: 'blue'
        }, 1);
    }
}
