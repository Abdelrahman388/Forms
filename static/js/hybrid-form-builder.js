/**
 * Hybrid Form Builder - Uses server endpoints with client-side data management
 * Combines server requests with local data synchronization
 */

class HybridFormBuilder {
    constructor() {
        this.formId = null;
        this.formData = {
            name: '',
            title: '',
            restrictToOne: false,
            questions: []
        };
        this.isInitialized = false;
    }    /**
     * Create a form on the server to get a form_id
     */
    async createServerForm() {
        const csrfToken = getCSRFToken();
        console.log('CSRF Token:', csrfToken ? 'Present' : 'Missing');
        
        if (!csrfToken) {
            throw new Error('CSRF token not available. Please refresh the page.');
        }
        
        const formData = new FormData();
        formData.append('name', 'Untitled Form');
        formData.append('title', 'Untitled Form');

        try {
            console.log('Making request to /create-temp-form...');
            const response = await fetch('/create-temp-form', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', Object.fromEntries(response.headers.entries()));

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Server response error:', {
                    status: response.status,
                    statusText: response.statusText,
                    body: errorText
                });
                
                if (response.status === 403) {
                    throw new Error('Authentication required. Please log in and try again.');
                } else if (response.status === 500) {
                    throw new Error('Server error. This may be a database constraint issue. Please try refreshing the page or contact support.');
                } else {
                    throw new Error(`Server error (${response.status}): ${errorText || response.statusText}`);
                }
            }

            let result;
            try {
                result = await response.json();
                console.log('Parsed server response:', result);
            } catch (parseError) {
                console.error('Failed to parse JSON response:', parseError);
                throw new Error('Invalid server response format');
            }
            
            if (result.success) {
                this.formId = result.form_id;
                console.log('Server form created successfully with ID:', this.formId);
            } else {
                const errorMessage = result.error || 'Unknown server error';
                console.error('Server returned error:', errorMessage);
                
                if (errorMessage.includes('FOREIGN KEY') || errorMessage.includes('constraint')) {
                    throw new Error('Database constraint error. Please ensure you are logged in and try again.');
                } else {
                    throw new Error(errorMessage);
                }
            }
        } catch (error) {
            console.error('Network or server error:', error);
            
            if (error instanceof TypeError && error.message.includes('fetch')) {
                throw new Error('Network connection error. Please check your internet connection.');
            } else if (error.message.includes('FOREIGN KEY') || error.message.includes('constraint')) {
                throw new Error('Database constraint error. Please ensure you are logged in with a valid account.');
            }
            throw error;
        }
    }/**
     * Initialize the form builder
     */
    async init() {
        if (this.isInitialized) return;
        
        console.log('Initializing Hybrid Form Builder...');
        console.log('CSRF Token available:', getCSRFToken() ? 'Yes' : 'No');
        console.log('Current URL:', window.location.href);
        
        try {
            // Create a form on the server to get a form_id
            console.log('Creating server form...');
            await this.createServerForm();
            console.log('Server form created with ID:', this.formId);
            
            // Fetch initial form data
            console.log('Fetching initial form data...');
            await this.fetchFormData();
            console.log('Form data fetched:', this.formData);
            
            // Set up event listeners
            console.log('Setting up event listeners...');
            this.setupEventListeners();
            
            // Initialize UI
            console.log('Updating UI...');
            this.updateUI();
            
            this.isInitialized = true;
            console.log('Hybrid Form Builder initialized successfully with form ID:', this.formId);
        } catch (error) {
            console.error('Failed to initialize Hybrid Form Builder:', error);
            
            // Provide more specific error messages
            let errorMessage = 'Failed to initialize form builder';
            if (error.message.includes('CSRF')) {
                errorMessage += ': Authentication token issue. Please refresh the page and try again.';
            } else if (error.message.includes('FOREIGN KEY') || error.message.includes('constraint')) {
                errorMessage += ': Database constraint error. Please ensure you are logged in and try again.';
            } else if (error.message.includes('403') || error.message.includes('Authentication')) {
                errorMessage += ': Please log in to access the form builder.';
                // Optionally redirect to login
                setTimeout(() => {
                    window.location.href = '/login';
                }, 3000);
            } else if (error.message.includes('Network')) {
                errorMessage += ': Network connection issue. Please check your connection and try again.';
            } else {
                errorMessage += ': ' + error.message;
            }
            
            this.showError(errorMessage);
            
            // If it's an authentication issue, suggest login
            if (error.message.includes('403') || error.message.includes('Authentication')) {
                setTimeout(() => {
                    if (confirm('You need to be logged in to create forms. Would you like to go to the login page?')) {
                        window.location.href = '/login';
                    }
                }, 2000);
            }
        }
    }/**
     * Create a form on the server to get a form_id
     */
    async createServerForm() {
        const csrfToken = getCSRFToken();
        console.log('CSRF Token:', csrfToken ? 'Present' : 'Missing');
        
        if (!csrfToken) {
            throw new Error('CSRF token not available. Please refresh the page.');
        }
        
        const formData = new FormData();
        formData.append('name', 'Untitled Form');
        formData.append('title', 'Untitled Form');

        try {
            console.log('Making request to /create-temp-form...');
            const response = await fetch('/create-temp-form', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: formData
            });

            console.log('Response status:', response.status);
            console.log('Response headers:', Object.fromEntries(response.headers.entries()));

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Server response error:', {
                    status: response.status,
                    statusText: response.statusText,
                    body: errorText
                });
                
                if (response.status === 403) {
                    throw new Error('Authentication required. Please log in and try again.');
                } else if (response.status === 500) {
                    throw new Error('Server error. This may be a database constraint issue. Please try refreshing the page or contact support.');
                } else {
                    throw new Error(`Server error (${response.status}): ${errorText || response.statusText}`);
                }
            }

            let result;
            try {
                result = await response.json();
                console.log('Parsed server response:', result);
            } catch (parseError) {
                console.error('Failed to parse JSON response:', parseError);
                throw new Error('Invalid server response format');
            }
            
            if (result.success) {
                this.formId = result.form_id;
                console.log('Server form created successfully with ID:', this.formId);
            } else {
                const errorMessage = result.error || 'Unknown server error';
                console.error('Server returned error:', errorMessage);
                
                if (errorMessage.includes('FOREIGN KEY') || errorMessage.includes('constraint')) {
                    throw new Error('Database constraint error. Please ensure you are logged in and try again.');
                } else {
                    throw new Error(errorMessage);
                }
            }
        } catch (error) {
            console.error('Network or server error:', error);
            
            if (error instanceof TypeError && error.message.includes('fetch')) {
                throw new Error('Network connection error. Please check your internet connection.');
            } else if (error.message.includes('FOREIGN KEY') || error.message.includes('constraint')) {
                throw new Error('Database constraint error. Please ensure you are logged in with a valid account.');
            }
            throw error;
        }
    }

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Form basic info auto-save
        document.getElementById('form-name').addEventListener('input', (e) => {
            this.formData.name = e.target.value;
        });

        document.getElementById('form-title').addEventListener('input', (e) => {
            this.formData.title = e.target.value;
        });

        document.getElementById('form-restrict').addEventListener('change', (e) => {
            this.formData.restrictToOne = e.target.checked;
        });

        // Add question button
        document.getElementById('add-question-btn').addEventListener('click', (e) => {
            e.preventDefault();
            this.addQuestion();
        });

        // Create form button
        document.getElementById('create-form-btn').addEventListener('click', (e) => {
            e.preventDefault();
            this.createForm();
        });

        // Event delegation for dynamic question controls
        document.addEventListener('click', (e) => {
            if (e.target.matches('.save-question-btn')) {
                e.preventDefault();
                this.saveQuestion(e.target);
            } else if (e.target.matches('.edit-question-btn')) {
                e.preventDefault();
                this.editQuestion(e.target);
            } else if (e.target.matches('.delete-question-btn')) {
                e.preventDefault();
                this.deleteQuestion(e.target);
            } else if (e.target.matches('.add-option-btn')) {
                e.preventDefault();
                this.addOption(e.target);
            } else if (e.target.matches('.save-option-btn')) {
                e.preventDefault();
                this.saveOption(e.target);
            } else if (e.target.matches('.delete-option-btn')) {
                e.preventDefault();
                this.deleteOption(e.target);
            }
        });

        // Event delegation for answer type changes
        document.addEventListener('change', (e) => {
            if (e.target.matches('.answer-type-select')) {
                this.handleAnswerTypeChange(e.target);
            }
        });
    }    /**
     * Add a new question via server endpoint
     */
    async addQuestion() {
        try {
            const response = await fetch('/addquestion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    form_id: this.formId
                })
            });

            const result = await response.json();
            if (result.success) {
                // Fetch updated form data from server
                await this.fetchFormData();
                this.updateUI();
            } else {
                throw new Error(result.error || 'Failed to add question');
            }
        } catch (error) {
            console.error('Error adding question:', error);
            this.showError('Failed to add question');
        }
    }    /**
     * Fetch current form data from server
     */
    async fetchFormData() {
        try {
            console.log('Fetching form data for form ID:', this.formId);
            const response = await fetch(`/get-form-data/${this.formId}`);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('Server response:', data);
            
            if (data.success) {
                // Update local data with server data
                this.syncWithServerData(data.form_data);
                console.log('Form data synced successfully');
            } else {
                throw new Error(data.error || 'Failed to fetch form data');
            }
        } catch (error) {
            console.error('Error fetching form data:', error);
            // Don't throw error here as this might happen during initial setup
        }
    }

    /**
     * Sync local form data with server data
     */
    syncWithServerData(serverData) {
        // Update questions array
        this.formData.questions = serverData.questions || [];
        
        // Update form basic info if needed
        if (serverData.name && serverData.name !== 'Untitled Form') {
            this.formData.name = serverData.name;
            document.getElementById('form-name').value = serverData.name;
        }
        if (serverData.title && serverData.title !== 'Untitled Form') {
            this.formData.title = serverData.title;
            document.getElementById('form-title').value = serverData.title;
        }
    }

    /**
     * Save a question via server endpoint
     */
    async saveQuestion(button) {
        const questionCard = button.closest('.question-card');
        const questionId = questionCard.dataset.questionId;
        const questionText = questionCard.querySelector('.question-input').value;
        const answerType = questionCard.querySelector('.answer-type-select').value;

        if (!questionText.trim()) {
            this.showError('Please enter a question');
            return;
        }        try {
            const response = await fetch('/writequestion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    qid: questionId,
                    question: questionText,
                    answer_type: answerType
                })
            });

            const result = await response.json();
            if (result.success) {
                await this.fetchFormData();
                this.updateUI();
            } else {
                throw new Error(result.error || 'Failed to save question');
            }
        } catch (error) {
            console.error('Error saving question:', error);
            this.showError('Failed to save question');
        }
    }

    /**
     * Edit a question via server endpoint
     */
    async editQuestion(button) {
        const questionCard = button.closest('.question-card');
        const questionId = questionCard.dataset.questionId;        try {
            const response = await fetch('/editquestion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    qid: questionId
                })
            });

            const result = await response.json();
            if (result.success) {
                await this.fetchFormData();
                this.updateUI();
            } else {
                throw new Error(result.error || 'Failed to edit question');
            }
        } catch (error) {
            console.error('Error editing question:', error);
            this.showError('Failed to edit question');
        }
    }

    /**
     * Delete a question via server endpoint
     */
    async deleteQuestion(button) {
        const questionCard = button.closest('.question-card');
        const questionId = questionCard.dataset.questionId;

        if (!confirm('Are you sure you want to delete this question?')) {
            return;
        }        try {
            const response = await fetch('/deletequestion', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    qid: questionId,
                    form_id: this.formId
                })
            });

            const result = await response.json();
            if (result.success) {
                await this.fetchFormData();
                this.updateUI();
            } else {
                throw new Error(result.error || 'Failed to delete question');
            }
        } catch (error) {
            console.error('Error deleting question:', error);
            this.showError('Failed to delete question');
        }
    }

    /**
     * Add option to a question
     */
    async addOption(button) {
        const questionCard = button.closest('.question-card');
        const questionId = questionCard.dataset.questionId;
        const answerType = questionCard.querySelector('.answer-type-select').value;        try {
            const response = await fetch('/addoption', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    qid: questionId,
                    form_id: this.formId,
                    type: answerType
                })
            });

            const result = await response.json();
            if (result.success) {
                await this.fetchFormData();
                this.updateUI();
            } else {
                throw new Error(result.error || 'Failed to add option');
            }
        } catch (error) {
            console.error('Error adding option:', error);
            this.showError('Failed to add option');
        }
    }

    /**
     * Save an option
     */
    async saveOption(button) {
        const optionElement = button.closest('.option-item');
        const optionId = optionElement.dataset.optionId;
        const optionText = optionElement.querySelector('.option-input').value;

        if (!optionText.trim()) {
            this.showError('Please enter an option text');
            return;
        }        try {
            const response = await fetch('/saveoption', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    oid: optionId,
                    option: optionText
                })
            });

            const result = await response.json();
            if (result.success) {
                await this.fetchFormData();
                this.updateUI();
            } else {
                throw new Error(result.error || 'Failed to save option');
            }
        } catch (error) {
            console.error('Error saving option:', error);
            this.showError('Failed to save option');
        }
    }

    /**
     * Delete an option
     */
    async deleteOption(button) {
        const optionElement = button.closest('.option-item');
        const optionId = optionElement.dataset.optionId;
        const questionCard = button.closest('.question-card');
        const questionId = questionCard.dataset.questionId;        try {
            const response = await fetch('/deleteoption', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    oid: optionId,
                    qid: questionId
                })
            });

            const result = await response.json();
            if (result.success) {
                await this.fetchFormData();
                this.updateUI();
            } else {
                throw new Error(result.error || 'Failed to delete option');
            }
        } catch (error) {
            console.error('Error deleting option:', error);
            this.showError('Failed to delete option');
        }
    }

    /**
     * Handle answer type change
     */
    handleAnswerTypeChange(select) {
        const questionCard = select.closest('.question-card');
        const answerType = select.value;
        const optionsContainer = questionCard.querySelector('.options-container');
        
        if (answerType === 'text') {
            optionsContainer.style.display = 'none';
        } else {
            optionsContainer.style.display = 'block';
        }
    }

    /**
     * Update the entire UI based on current form data
     */
    updateUI() {
        this.renderQuestions();
        this.toggleNoQuestionsMessage();
    }

    /**
     * Render all questions
     */
    renderQuestions() {
        const container = document.getElementById('questions-container');
        container.innerHTML = '';

        this.formData.questions.forEach((question, index) => {
            const questionElement = this.createQuestionElement(question, index);
            container.appendChild(questionElement);
        });
    }

    /**
     * Create a question element
     */
    createQuestionElement(question, index) {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'row mb-4';
        questionDiv.innerHTML = `
            <div class="col-12">
                <div class="card shadow-sm question-card" data-question-id="${question.question_id}">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="mb-0">Question ${index + 1}</h6>
                        <div class="btn-group btn-group-sm">
                            ${question.saved ? 
                                `<button class="btn btn-outline-primary edit-question-btn">
                                    <i class="bi bi-pencil"></i> Edit
                                </button>` :
                                `<button class="btn btn-success save-question-btn">
                                    <i class="bi bi-check"></i> Save
                                </button>`
                            }
                            <button class="btn btn-outline-danger delete-question-btn">
                                <i class="bi bi-trash"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <div class="form-floating mb-3">
                                    <input class="form-control question-input" 
                                           type="text" 
                                           value="${question.question_text || ''}"
                                           placeholder="Enter your question"
                                           ${question.saved ? 'readonly' : ''}>
                                    <label>Question Text</label>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-floating mb-3">
                                    <select class="form-select answer-type-select" ${question.saved ? 'disabled' : ''}>
                                        <option value="text" ${question.answer_type === 'text' ? 'selected' : ''}>Text</option>
                                        <option value="radio" ${question.answer_type === 'radio' ? 'selected' : ''}>Single Choice</option>
                                        <option value="checkbox" ${question.answer_type === 'checkbox' ? 'selected' : ''}>Multiple Choice</option>
                                    </select>
                                    <label>Answer Type</label>
                                </div>
                            </div>
                        </div>
                        
                        <div class="options-container" style="display: ${question.answer_type === 'text' ? 'none' : 'block'}">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h6 class="mb-0">Options</h6>
                                <button class="btn btn-sm btn-outline-primary add-option-btn">
                                    <i class="bi bi-plus"></i> Add Option
                                </button>
                            </div>
                            <div class="options-list">
                                ${this.renderOptions(question.options || [])}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        return questionDiv;
    }

    /**
     * Render options for a question
     */
    renderOptions(options) {
        if (!options || options.length === 0) {
            return '<p class="text-muted">No options yet. Click "Add Option" to create options for this question.</p>';
        }

        return options.map((option, index) => `
            <div class="option-item mb-2 p-3 border rounded" data-option-id="${option.option_id}">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <div class="input-group">
                            <span class="input-group-text">${index + 1}.</span>
                            <input class="form-control option-input" 
                                   type="text" 
                                   value="${option.option_text || ''}"
                                   placeholder="Enter option text"
                                   ${option.saved ? 'readonly' : ''}>
                        </div>
                    </div>
                    <div class="col-md-4 text-end">
                        ${option.saved ? 
                            `<span class="badge bg-success me-2">Saved</span>` :
                            `<button class="btn btn-sm btn-success save-option-btn me-2">
                                <i class="bi bi-check"></i> Save
                            </button>`
                        }
                        <button class="btn btn-sm btn-outline-danger delete-option-btn">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }    /**
     * Toggle the "No questions yet" message
     */
    toggleNoQuestionsMessage() {
        const noQuestionsMessage = document.getElementById('no-questions-message');
        console.log('Toggling no questions message. Questions count:', this.formData.questions.length);
        
        if (this.formData.questions.length === 0) {
            console.log('Showing no questions message');
            noQuestionsMessage.classList.remove('d-none');
        } else {
            console.log('Hiding no questions message');
            noQuestionsMessage.classList.add('d-none');
        }
    }

    /**
     * Create the final form
     */
    async createForm() {
        // Validate form
        if (!this.formData.name.trim() || !this.formData.title.trim()) {
            this.showError('Please enter form name and title');
            return;
        }

        if (this.formData.questions.length === 0) {
            this.showError('Please add at least one question');
            return;
        }

        // Check if all questions are saved
        const unsavedQuestions = this.formData.questions.filter(q => !q.saved);
        if (unsavedQuestions.length > 0) {
            this.showError('Please save all questions before creating the form');
            return;
        }        try {
            const response = await fetch('/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({
                    form_id: this.formId,
                    name: this.formData.name,
                    title: this.formData.title
                })
            });

            const result = await response.json();
            if (result.success) {
                window.location.href = result.redirect;
            } else {
                throw new Error(result.error || 'Failed to create form');
            }
        } catch (error) {
            console.error('Error creating form:', error);
            this.showError('Failed to create form');
        }
    }    /**
     * Show error message
     */
    showError(message) {
        console.error('Form Builder Error:', message);
        
        // Create a simple error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger alert-dismissible fade show position-fixed';
        errorDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 400px;';
        errorDiv.innerHTML = `
            <strong>Error:</strong> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(errorDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
}

// Make HybridFormBuilder available globally
window.HybridFormBuilder = HybridFormBuilder;
