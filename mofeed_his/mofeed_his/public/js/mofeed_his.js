/**
 * Al-Mofeed HIS - Main JavaScript
 * Hospital Information System
 * 
 * This file contains global JavaScript for the mofeed_his app.
 * Page-specific scripts are in their respective page directories.
 */

// Register global namespace
window.mofeed_his = window.mofeed_his || {};

/**
 * Initialize mofeed_his app
 */
mofeed_his.init = function() {
    console.log('Al-Mofeed HIS initialized');
};

/**
 * Utility function to format dates in a consistent way
 * @param {string|Date} date - Date to format
 * @returns {string} Formatted date string
 */
mofeed_his.format_date = function(date) {
    if (!date) return '';
    return frappe.datetime.str_to_user(date);
};

/**
 * Utility function to format time
 * @param {string} time - Time string (HH:MM:SS)
 * @returns {string} Formatted time (HH:MM)
 */
mofeed_his.format_time = function(time) {
    if (!time) return '';
    return time.substring(0, 5);
};

/**
 * Show a notification with mofeed_his styling
 * @param {string} message - Notification message
 * @param {string} type - 'success', 'warning', 'error', 'info'
 */
mofeed_his.notify = function(message, type) {
    let indicator = 'blue';
    switch(type) {
        case 'success': indicator = 'green'; break;
        case 'warning': indicator = 'orange'; break;
        case 'error': indicator = 'red'; break;
        default: indicator = 'blue';
    }
    
    frappe.show_alert({
        message: message,
        indicator: indicator
    }, 5);
};

// Initialize on DOM ready
$(document).ready(function() {
    mofeed_his.init();
});
