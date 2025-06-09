/**
 * Theme management functionality
 * Handles dark/light mode toggle
 */

/**
 * Initialize theme toggle functionality
 */
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function(e) {
            e.preventDefault();
            toggleTheme();
        });
    }
}

/**
 * Toggle between light and dark themes
 */
function toggleTheme() {
    try {
        const currentTheme = localStorage.getItem('theme') || 'light';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        localStorage.setItem('theme', newTheme);
        
        const body = document.body;
        const themeToggle = document.getElementById('theme-toggle');
        
        if (newTheme === 'dark') {
            body.classList.add('dark-mode');
            if (themeToggle) themeToggle.textContent = '☀️';
        } else {
            body.classList.remove('dark-mode');
            if (themeToggle) themeToggle.textContent = '🌙';
        }
        
        // Show success message if available
        if (window.showSuccess) {
            showSuccess(`Switched to ${newTheme} mode`);
        }
    } catch (error) {
        console.error('Error toggling theme:', error);
        if (window.showError) {
            showError('Failed to toggle theme');
        }
    }
}

// Export for global access
window.ThemeManager = {
    initializeThemeToggle,
    toggleTheme
};
