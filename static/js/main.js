/**
 * Main JavaScript file for Forms application
 * Coordinates all functionality modules
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all modules
    initializeApplication();
});

/**
 * Initialize the complete application
 */
function initializeApplication() {
    console.log('Initializing Forms application...');
    
    // Initialize theme functionality
    if (window.ThemeManager) {
        ThemeManager.initializeThemeToggle();
    }
    
    // Initialize form builder functionality
    if (window.FormBuilder) {
        FormBuilder.initializeFormBuilder();
    }
    
    // Initialize response form functionality
    if (window.ResponseManager) {
        ResponseManager.initializeResponseForm();
    }
    
    // Initialize option management
    if (window.OptionManager) {
        OptionManager.initializeOptionManagement();
    }
    
    // Initialize charts if on responses page
    if (window.location.pathname.includes('/responses_statistics/') && window.ChartsManager) {
        ChartsManager.initializeCharts();
    }
    
    console.log('Forms application initialized successfully');
}

/**
 * Global functions for backward compatibility with onclick handlers
 * These functions delegate to the appropriate modules
 */

// Form builder functions
window.addQuestion = function(formId) {
    return FormBuilder.addQuestion(formId);
};

window.deleteQuestion = function(questionId, formId) {
    return FormBuilder.deleteQuestion(questionId, formId);
};

window.editQuestion = function(questionId, formId) {
    return FormBuilder.editQuestion(questionId, formId);
};

window.saveQuestion = function(questionId) {
    return FormBuilder.saveQuestion(questionId);
};

window.updateQuestion = function(questionId, answerType, questionText) {
    return FormBuilder.updateQuestion(questionId, answerType, questionText);
};

// Option management functions
window.addOption = function(questionId, formId, answerType) {
    return OptionManager.addOption(questionId, formId, answerType);
};

window.saveOption = function(optionId, questionId) {
    return OptionManager.saveOption(optionId, questionId);
};

window.deleteOption = function(optionId, questionId) {
    return OptionManager.deleteOption(optionId, questionId);
};

// Utility functions
window.getCSRFToken = function() {
    return FormsUtils.getCSRFToken();
};

window.showError = function(message) {
    return FormsUtils.showError(message);
};

window.showSuccess = function(message) {
    return FormsUtils.showSuccess(message);
};
