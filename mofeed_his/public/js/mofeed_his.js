/**
 * Mofeed HIS - Global JavaScript
 * 
 * This file provides global functionality for the Al-Mofeed HIS app.
 * It is loaded on all Desk pages via hooks.py app_include_js.
 */

// Mofeed HIS namespace
window.mofeed_his = window.mofeed_his || {};

/**
 * Initialize Mofeed HIS when document is ready
 */
frappe.ready(function() {
    console.log('Mofeed HIS initialized');
    mofeed_his.setup_language_detection();
});

/**
 * Setup language detection and RTL support
 */
mofeed_his.setup_language_detection = function() {
    var lang = frappe.boot.lang || 'en';
    
    if (lang === 'ar' || lang === 'ckb') {
        document.body.classList.add('rtl');
        document.documentElement.setAttribute('dir', 'rtl');
    }
    
    document.body.classList.add('lang-' + lang);
};

/**
 * Format MRN for display
 * @param {string} mrn - Medical Record Number
 * @returns {string} Formatted MRN
 */
mofeed_his.format_mrn = function(mrn) {
    if (!mrn) return '';
    return mrn.toUpperCase();
};

/**
 * Get patient extension data
 * @param {string} patient - Patient name
 * @param {function} callback - Callback function
 */
mofeed_his.get_patient_extension = function(patient, callback) {
    frappe.call({
        method: 'mofeed_his.mofeed_his.doctype.patient_extension.patient_extension.get_patient_extension',
        args: { patient: patient },
        callback: function(r) {
            if (callback) callback(r.message);
        }
    });
};
