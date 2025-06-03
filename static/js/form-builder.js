/**
 * Form builder functionality
 * Handles question and option management
 */

/**
 * Initialize form builder functionality
 */
function initializeFormBuilder() {
    // Add question button
    const addQuestionBtn = document.getElementById('add-question-btn');
    if (addQuestionBtn) {
        addQuestionBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const formId = document.querySelector('input[name="form_id"]').value;
            addQuestion(formId);
        });
    }
    
    // Create form button
    const createFormBtn = document.getElementById('create_button');
    if (createFormBtn) {
        createFormBtn.addEventListener('click', function(e) {
            e.preventDefault();
            submitForm();
        });
    }
    
    // Initialize question type change handlers
    initializeQuestionTypeHandlers();
    
    // Initialize delete buttons
    initializeDeleteButtons();
    
    // Initialize edit buttons
    initializeEditButtons();
    
    // Initialize option management
    initializeOptionManagement();
}

/**
 * Initialize question type change handlers
 */
function initializeQuestionTypeHandlers() {
    const emptyQuestions = window.emptyQuestions || [];
    
    emptyQuestions.forEach(function(emptyQuestion) {
        const answerTypeSelect = document.getElementById(`answer-type${emptyQuestion.question_id}`);
        const answerDiv = document.getElementById(`answer${emptyQuestion.question_id}`);
        const updateForm = document.getElementById(`update${emptyQuestion.question_id}`);
        
        if (answerTypeSelect && answerDiv) {
            answerTypeSelect.addEventListener('change', function() {
                updateQuestionType(emptyQuestion, answerTypeSelect.value);
            });
            
            // Set initial state
            if (answerTypeSelect.value) {
                updateQuestionType(emptyQuestion, answerTypeSelect.value);
            }
        }
    });
}

/**
 * Update question type and UI
 */
function updateQuestionType(question, answerType) {
    const answerDiv = document.getElementById(`answer${question.question_id}`);
    
    if (answerType === "text") {
        answerDiv.innerHTML = `
            <form>
                <input disabled class="form-control mx-auto w-auto d-inline-block" type="text" placeholder="Answer">
            </form>`;
    } else if (answerType === "radio" || answerType === "checkbox") {
        answerDiv.innerHTML = `
            <button type="button" class="btn btn-sm btn-primary" onclick="FormBuilder.addOption('${question.question_id}', '${question.form_id}', '${answerType}')">
                Add Option
            </button>`;
    }
    
    // Update question with new type
    updateQuestion(question.question_id, answerType);
}

/**
 * Add a new question to the form
 */
async function addQuestion(formId) {
    try {
        const response = await FormsUtils.makeRequest('/addquestion', {
            method: 'POST',
            body: JSON.stringify({ form_id: formId })
        });
        
        const data = await response.json();
        if (data.success) {
            // Reload the page to show new question
            window.location.reload();
        } else {
            FormsUtils.showError(data.error || 'Failed to add question');
        }
    } catch (error) {
        console.error('Error adding question:', error);
        FormsUtils.showError('Failed to add question');
    }
}

/**
 * Delete a question
 */
async function deleteQuestion(questionId, formId) {
    if (!confirm('Are you sure you want to delete this question?')) {
        return;
    }
    
    try {
        const response = await FormsUtils.makeRequest('/deletequestion', {
            method: 'POST',
            body: JSON.stringify({ 
                qid: questionId,
                form_id: formId
            })
        });
        
        const data = await response.json();
        if (data.success) {
            window.location.reload();
        } else {
            FormsUtils.showError(data.error || 'Failed to delete question');
        }
    } catch (error) {
        console.error('Error deleting question:', error);
        FormsUtils.showError('Failed to delete question');
    }
}

/**
 * Edit a question
 */
async function editQuestion(questionId, formId) {
    try {
        const response = await FormsUtils.makeRequest('/editquestion', {
            method: 'POST',
            body: JSON.stringify({ 
                qid: questionId,
                form_id: formId
            })
        });
        
        const data = await response.json();
        if (data.success) {
            window.location.reload();
        } else {
            FormsUtils.showError(data.error || 'Failed to edit question');
        }
    } catch (error) {
        console.error('Error editing question:', error);
        FormsUtils.showError('Failed to edit question');
    }
}

/**
 * Update question properties
 */
async function updateQuestion(questionId, answerType, questionText = null) {
    try {
        const body = { 
            qid: questionId,
            answer_type: answerType
        };
        
        if (questionText) {
            body.question_text = questionText;
        }
        
        const response = await FormsUtils.makeRequest('/updatequestion', {
            method: 'POST',
            body: JSON.stringify(body)
        });
        
        const data = await response.json();
        if (!data.success) {
            FormsUtils.showError(data.error || 'Failed to update question');
        }
    } catch (error) {
        console.error('Error updating question:', error);
    }
}

/**
 * Save question text and type
 */
async function saveQuestion(questionId) {
    const questionInput = document.getElementById(`question${questionId}`);
    const answerTypeSelect = document.getElementById(`answer-type${questionId}`);
    
    if (!questionInput.value || !answerTypeSelect.value) {
        FormsUtils.showError('Please fill in both question text and answer type');
        return;
    }
    
    try {
        const response = await FormsUtils.makeRequest('/writequestion', {
            method: 'POST',
            body: JSON.stringify({
                qid: questionId,
                question: questionInput.value,
                answer_type: answerTypeSelect.value
            })
        });
        
        const data = await response.json();
        if (data.success) {
            window.location.reload();
        } else {
            FormsUtils.showError(data.error || 'Failed to save question');
        }
    } catch (error) {
        console.error('Error saving question:', error);
        FormsUtils.showError('Failed to save question');
    }
}

/**
 * Submit the complete form
 */
async function submitForm() {
    const nameInput = document.getElementById('name');
    const titleInput = document.getElementById('title');
    const formIdInput = document.querySelector('input[name="form_id"]');
    
    if (!nameInput.value || !titleInput.value) {
        FormsUtils.showError('Form name and title are required');
        return;
    }
    
    // Check if form has questions
    const writtenQuestions = window.writtenQuestions || [];
    if (writtenQuestions.length === 0) {
        FormsUtils.showError('Please add at least one question to your form');
        return;
    }
    
    try {
        const response = await FormsUtils.makeRequest('/create', {
            method: 'POST',
            body: JSON.stringify({
                form_id: formIdInput.value,
                name: nameInput.value,
                title: titleInput.value
            })
        });
        
        const data = await response.json();
        if (data.success) {
            window.location.href = data.redirect || '/';
        } else {
            FormsUtils.showError(data.error || 'Failed to create form');
        }
    } catch (error) {
        console.error('Error creating form:', error);
        FormsUtils.showError('Failed to create form');
    }
}

/**
 * Delete a form
 */
async function deleteForm(formId) {
    try {
        const response = await FormsUtils.makeRequest('/delete', {
            method: 'POST',
            body: JSON.stringify({ form_id: formId })
        });
        
        const data = await response.json();
        if (data.success) {
            window.location.href = '/';
        } else {
            FormsUtils.showError(data.error || 'Failed to delete form');
        }
    } catch (error) {
        console.error('Error deleting form:', error);
        FormsUtils.showError('Failed to delete form');
    }
}

/**
 * Initialize delete button handlers
 */
function initializeDeleteButtons() {
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('delete-question-btn')) {
            e.preventDefault();
            const questionId = e.target.dataset.questionId;
            const formId = e.target.dataset.formId;
            deleteQuestion(questionId, formId);
        }
        
        if (e.target.classList.contains('delete-form-btn')) {
            e.preventDefault();
            if (confirm('Are you sure you want to delete this form? This action cannot be undone.')) {
                const formId = e.target.dataset.formId;
                deleteForm(formId);
            }
        }
    });
}

/**
 * Initialize edit button handlers
 */
function initializeEditButtons() {
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('edit-question-btn')) {
            e.preventDefault();
            const questionId = e.target.dataset.questionId;
            const formId = e.target.dataset.formId;
            editQuestion(questionId, formId);
        }
        
        if (e.target.classList.contains('save-question-btn')) {
            e.preventDefault();
            const questionId = e.target.dataset.questionId;
            saveQuestion(questionId);
        }
    });
}

// Export for global access
window.FormBuilder = {
    initializeFormBuilder,
    addQuestion,
    deleteQuestion,
    editQuestion,
    saveQuestion,
    updateQuestion,
    updateQuestionType,
    submitForm,
    deleteForm
};
