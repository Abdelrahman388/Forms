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
async function toggleTheme() {
    try {
        const response = await FormsUtils.makeRequest('/toggle_theme', {
            method: 'POST'
        });
        
        const data = await response.json();
        if (data.success) {
            const body = document.body;
            if (data.mode === 'dark') {
                body.classList.add('dark-mode');
                document.getElementById('theme-toggle').textContent = '☀️';
            } else {
                body.classList.remove('dark-mode');
                document.getElementById('theme-toggle').textContent = '🌙';
            }
        }
    } catch (error) {
        console.error('Error toggling theme:', error);
        FormsUtils.showError('Failed to toggle theme');
    }
}

// Export for global access
window.ThemeManager = {
    initializeThemeToggle,
    toggleTheme
};
