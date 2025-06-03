/**
 * Charts functionality
 * Handles data visualization for form responses
 */

/**
 * Initialize charts if on responses page
 */
function initializeCharts() {
    if (typeof Chart === 'undefined') {
        console.error('Chart.js not loaded');
        return;
    }
    
    const options = window.optionAnswerCount || [];
    const questions = window.questions || [];
    
    renderCharts(questions, options);
}

/**
 * Render charts for form response data
 */
function renderCharts(questions, optionCounts) {
    questions.forEach(function(question) {
        if (question.answer_type !== "text") {
            const filteredOptions = optionCounts.filter(option => option.question_id === question.question_id);
            
            if (filteredOptions.length > 0) {
                const labels = filteredOptions.map(option => option.option);
                const data = filteredOptions.map(option => option.count);
                const backgroundColors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'];
                
                const container = document.getElementById(`chartsContainer-${question.question_id}`);
                if (container) {
                    // Clear existing canvas
                    container.innerHTML = '';
                    
                    const canvas = document.createElement('canvas');
                    container.appendChild(canvas);
                    
                    new Chart(canvas.getContext('2d'), {
                        type: 'pie',
                        data: {
                            labels: labels,
                            datasets: [{
                                data: data,
                                backgroundColor: backgroundColors.slice(0, labels.length)
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                title: {
                                    display: true,
                                    text: `${question.question} - Response Distribution`
                                },
                                legend: {
                                    position: 'bottom'
                                }
                            }
                        }
                    });
                }
            }
        }
    });
}

/**
 * Create a chart for a specific question
 */
function createChart(containerId, question, optionData) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.error(`Chart container ${containerId} not found`);
        return;
    }
    
    // Clear existing content
    container.innerHTML = '';
    
    const canvas = document.createElement('canvas');
    container.appendChild(canvas);
    
    const labels = optionData.map(item => item.option);
    const data = optionData.map(item => item.count);
    const backgroundColors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];
    
    new Chart(canvas.getContext('2d'), {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors.slice(0, labels.length),
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `${question.question} - Response Distribution`,
                    font: {
                        size: 16
                    }
                },
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        }
    });
}

// Export for global access
window.ChartsManager = {
    initializeCharts,
    renderCharts,
    createChart
};
