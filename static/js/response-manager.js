/**
 * Response form functionality
 * Handles form submission for end users responding to forms
 */

/**
 * Initialize response form functionality
 */
function initializeResponseForm() {
    const responseForm = document.getElementById('response-form');
    if (responseForm) {
        responseForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitResponse();
        });
    }
}

/**
 * Submit a form response
 */
async function submitResponse() {
    const form = document.getElementById('response-form');
    const formData = new FormData(form);
    const formId = document.querySelector('input[name="form_id"]').value;
    
    // Convert FormData to JSON
    const data = {};
    for (let [key, value] of formData.entries()) {
        if (data[key]) {
            // Handle multiple values (checkboxes)
            if (Array.isArray(data[key])) {
                data[key].push(value);
            } else {
                data[key] = [data[key], value];
            }
        } else {
            data[key] = value;
        }
    }
    
    try {
        const response = await FormsUtils.makeRequest(`/respond/${formId}`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (result.success) {
            FormsUtils.showSuccess(result.message || 'Form submitted successfully!');
            form.reset();
        } else {
            if (result.errors) {
                FormsUtils.showError(result.errors.join('\\n'));
            } else {
                FormsUtils.showError(result.error || 'Failed to submit form');
            }
        }
    } catch (error) {
        console.error('Error submitting response:', error);
        FormsUtils.showError('Failed to submit form');
    }
}

// Export for global access
window.ResponseManager = {
    initializeResponseForm,
    submitResponse
};
