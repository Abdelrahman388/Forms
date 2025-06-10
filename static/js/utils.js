function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
}

function createToastContainer() {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            max-width: 500px;
            width: 90%;
            pointer-events: none;
        `;
        document.body.appendChild(container);
    }
    return container;
}

function createAlert(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show shadow-lg mb-3`;
    alert.style.cssText = `
        pointer-events: auto;
        border: none;
        border-radius: 8px;
        backdrop-filter: blur(10px);
        animation: slideInFromTop 0.4s ease-out;
    `;
    
    alert.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="bi bi-${type === 'danger' ? 'exclamation-triangle' : 'check-circle'} me-2"></i>
            <div class="flex-grow-1">${message}</div>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert" style="filter: invert(1);"></button>
        </div>
    `;
    
    // Add CSS animation if not already added
    if (!document.getElementById('toast-animations')) {
        const style = document.createElement('style');
        style.id = 'toast-animations';
        style.textContent = `
            @keyframes slideInFromTop {
                from {
                    transform: translateY(-100%);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOutToTop {
                from {
                    transform: translateY(0);
                    opacity: 1;
                }
                to {
                    transform: translateY(-100%);
                    opacity: 0;
                }
            }
            
            .alert-slide-out {
                animation: slideOutToTop 0.3s ease-in;
            }
            
            /* Dark mode support for alerts */
            body.dark-mode .alert-danger {
                background-color: rgba(220, 53, 69, 0.9);
                border-color: rgba(220, 53, 69, 0.5);
                color: white;
            }
            
            body.dark-mode .alert-success {
                background-color: rgba(25, 135, 84, 0.9);
                border-color: rgba(25, 135, 84, 0.5);
                color: white;
            }
            
            /* Mobile responsiveness */
            @media (max-width: 576px) {
                #toast-container {
                    width: 95%;
                    max-width: none;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    return alert;
}

function showError(message) {
    const container = createToastContainer();
    const alert = createAlert(message, 'danger');
    
    container.appendChild(alert);
    
    // Auto-dismiss after 5 seconds with animation
    setTimeout(() => {
        if (alert.parentNode) {
            alert.classList.add('alert-slide-out');
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 300);
        }
    }, 5000);
    
    // Handle manual close button
    const closeBtn = alert.querySelector('.btn-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            alert.classList.add('alert-slide-out');
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 300);
        });
    }
}

function showSuccess(message) {
    const container = createToastContainer();
    const alert = createAlert(message, 'success');
    
    container.appendChild(alert);
    
    // Auto-dismiss after 3 seconds with animation
    setTimeout(() => {
        if (alert.parentNode) {
            alert.classList.add('alert-slide-out');
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 300);
        }
    }, 3000);
    
    // Handle manual close button
    const closeBtn = alert.querySelector('.btn-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            alert.classList.add('alert-slide-out');
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 300);
        });
    }
}


async function makeRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        }
    };
    
    const mergedOptions = { ...defaultOptions, ...options };
    if (options.headers) {
        mergedOptions.headers = { ...defaultOptions.headers, ...options.headers };
    }
    
    return fetch(url, mergedOptions);
}

// Export functions for use in other modules
window.FormsUtils = {
    getCSRFToken,
    showError,
    showSuccess,
    makeRequest
};
