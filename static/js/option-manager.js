/**
 * Option management functionality
 * Handles adding, editing, deleting, and saving options for questions
 */

/**
 * Initialize option management functionality
 */
function initializeOptionManagement() {
    // Initialize save option buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('save-option-btn')) {
            e.preventDefault();
            const optionId = e.target.dataset.optionId;
            const questionId = e.target.dataset.questionId;
            const optionInput = document.querySelector(`input[data-option-id="${optionId}"]`);
            
            if (optionInput && optionInput.value.trim()) {
                saveOptionText(optionId, questionId, optionInput.value.trim());
            } else {
                FormsUtils.showError('Please enter option text');
            }
        }
        
        if (e.target.classList.contains('delete-option-btn')) {
            e.preventDefault();
            const optionId = e.target.dataset.optionId;
            const questionId = e.target.dataset.questionId;
            deleteOption(optionId, questionId);
        }
    });
    
    // Auto-save options on Enter key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.hasAttribute('data-option-id')) {
            e.preventDefault();
            const optionId = e.target.dataset.optionId;
            const saveBtn = document.querySelector(`button[data-option-id="${optionId}"].save-option-btn`);
            if (saveBtn) {
                saveBtn.click();
            }
        }
    });
}

/**
 * Add a new option to a question
 */
async function addOption(questionId, formId, answerType) {
    try {
        const response = await FormsUtils.makeRequest('/addoption', {
            method: 'POST',
            body: JSON.stringify({
                qid: questionId,
                form_id: formId,
                type: answerType
            })
        });
        
        const data = await response.json();
        if (data.success) {
            window.location.reload();
        } else {
            FormsUtils.showError(data.error || 'Failed to add option');
        }
    } catch (error) {
        console.error('Error adding option:', error);
        FormsUtils.showError('Failed to add option');
    }
}

/**
 * Save option text (legacy method for backward compatibility)
 */
async function saveOption(optionId, questionId) {
    const optionInput = document.querySelector(`input[data-option-id="${optionId}"]`);
    if (!optionInput || !optionInput.value) {
        FormsUtils.showError('Please enter option text');
        return;
    }
    
    await saveOptionText(optionId, questionId, optionInput.value);
}

/**
 * Save option text with specified value
 */
async function saveOptionText(optionId, questionId, optionText) {
    try {
        const response = await FormsUtils.makeRequest('/saveoption', {
            method: 'POST',
            body: JSON.stringify({
                oid: optionId,
                qid: questionId,
                option: optionText
            })
        });
        
        const data = await response.json();
        if (data.success) {
            window.location.reload();
        } else {
            FormsUtils.showError(data.error || 'Failed to save option');
        }
    } catch (error) {
        console.error('Error saving option:', error);
        FormsUtils.showError('Failed to save option');
    }
}

/**
 * Delete an option
 */
async function deleteOption(optionId, questionId) {
    if (!confirm('Are you sure you want to delete this option?')) {
        return;
    }
    
    try {
        const response = await FormsUtils.makeRequest('/deleteoption', {
            method: 'POST',
            body: JSON.stringify({
                oid: optionId,
                qid: questionId
            })
        });
        
        const data = await response.json();
        if (data.success) {
            window.location.reload();
        } else {
            FormsUtils.showError(data.error || 'Failed to delete option');
        }
    } catch (error) {
        console.error('Error deleting option:', error);
        FormsUtils.showError('Failed to delete option');
    }
}

// Export for global access
window.OptionManager = {
    initializeOptionManagement,
    addOption,
    saveOption,
    saveOptionText,
    deleteOption
};
