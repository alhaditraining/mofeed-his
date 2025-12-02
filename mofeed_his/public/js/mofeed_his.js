/**
 * Al-Mofeed HIS - Main Desk JavaScript
 * 
 * Entry point for desk-side JavaScript functionality.
 */

(function() {
  'use strict';

  // Initialize when Frappe is ready
  if (typeof frappe !== 'undefined') {
    frappe.ready(function() {
      console.log('Al-Mofeed HIS: Desk initialized');
    });
  }
})();
