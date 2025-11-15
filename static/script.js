// DOM Elements
const form = document.getElementById('investment-form');
const formSection = document.getElementById('form-section');
const resultsSection = document.getElementById('results-section');
const resultsContent = document.getElementById('results-content');
const submitBtn = document.getElementById('submit-btn');
const submitText = document.getElementById('submit-text');
const loadingSpinner = document.getElementById('loading-spinner');
const addGoalBtn = document.getElementById('add-goal-btn');
const backBtn = document.getElementById('back-btn');
const goalsContainer = document.getElementById('goals-container');

// Add goal functionality
addGoalBtn.addEventListener('click', () => {
    const goalItem = document.createElement('div');
    goalItem.className = 'goal-item';
    goalItem.innerHTML = `
        <div class="form-row">
            <div class="form-field">
                <label>Goal Name *</label>
                <input type="text" class="goal-name" required placeholder="e.g., Retirement">
            </div>
            <div class="form-field">
                <label>Target Amount ($) *</label>
                <input type="number" class="goal-amount" required min="0" placeholder="2000000">
            </div>
        </div>
        <div class="form-row">
            <div class="form-field">
                <label>Timeline *</label>
                <input type="text" class="goal-timeline" required placeholder="e.g., 15 years">
            </div>
            <div class="form-field">
                <label>Priority</label>
                <select class="goal-priority">
                    <option value="high">High</option>
                    <option value="medium" selected>Medium</option>
                    <option value="low">Low</option>
                </select>
            </div>
        </div>
        <button type="button" class="remove-goal-btn btn-secondary" style="margin-top: 10px;">Remove Goal</button>
    `;
    goalsContainer.appendChild(goalItem);
    
    // Add remove functionality
    goalItem.querySelector('.remove-goal-btn').addEventListener('click', () => {
        goalItem.remove();
    });
});

// Form submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Validate form
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    
    // Collect form data
    const formData = collectFormData();
    
    // Show loading state
    setLoadingState(true);
    
    try {
        // Call API
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }
        
        const data = await response.json();
        
        // Display results
        displayResults(data);
        
        // Show results section
        formSection.style.display = 'none';
        resultsSection.style.display = 'block';
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message);
    } finally {
        setLoadingState(false);
    }
});

// Back button
backBtn.addEventListener('click', () => {
    resultsSection.style.display = 'none';
    formSection.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Collect form data
function collectFormData() {
    // Profile
    const profile = {
        user_id: document.getElementById('user_id').value,
        name: document.getElementById('name').value,
        age: parseInt(document.getElementById('age').value),
        income: parseFloat(document.getElementById('income').value),
        risk_tolerance: document.getElementById('risk_tolerance').value,
        investment_timeline: document.getElementById('investment_timeline').value
    };
    
    // Portfolio
    const holdings = {};
    const stocks = parseFloat(document.getElementById('stocks').value) || 0;
    const bonds = parseFloat(document.getElementById('bonds').value) || 0;
    const cash = parseFloat(document.getElementById('cash').value) || 0;
    const crypto = parseFloat(document.getElementById('crypto').value) || 0;
    const other = parseFloat(document.getElementById('other_holdings').value) || 0;
    
    if (stocks > 0) holdings.stocks = stocks;
    if (bonds > 0) holdings.bonds = bonds;
    if (cash > 0) holdings.cash = cash;
    if (crypto > 0) holdings.crypto = crypto;
    if (other > 0) holdings.other = other;
    
    const portfolio = {
        user_id: profile.user_id,
        total_value: parseFloat(document.getElementById('total_value').value),
        holdings: holdings
    };
    
    const riskScore = document.getElementById('risk_score').value;
    if (riskScore) {
        portfolio.risk_score = parseFloat(riskScore);
    }
    
    // Tax info
    const taxInfo = {};
    const taxBracket = document.getElementById('tax_bracket').value;
    const state = document.getElementById('state').value;
    const filingStatus = document.getElementById('filing_status').value;
    
    if (taxBracket) taxInfo.tax_bracket = taxBracket;
    if (state) taxInfo.state = state;
    if (filingStatus) taxInfo.filing_status = filingStatus;
    
    // Goals
    const goals = [];
    const goalItems = goalsContainer.querySelectorAll('.goal-item');
    goalItems.forEach(item => {
        const name = item.querySelector('.goal-name').value;
        const amount = item.querySelector('.goal-amount').value;
        const timeline = item.querySelector('.goal-timeline').value;
        const priority = item.querySelector('.goal-priority').value;
        
        if (name && amount && timeline) {
            goals.push({
                name: name,
                target_amount: parseFloat(amount),
                timeline: timeline,
                priority: priority || 'medium'
            });
        }
    });
    
    return {
        profile: profile,
        portfolio: portfolio,
        tax_info: taxInfo,
        goals: goals
    };
}

// Display results
function displayResults(data) {
    const results = data.results;
    let html = '<div class="success-badge">✓ Analysis Complete</div>';
    
    // Risk Assessment
    if (results.risk_assessment) {
        html += `
            <div class="result-section">
                <h3>🛡️ Risk Assessment</h3>
                <div class="result-content">${formatText(results.risk_assessment)}</div>
            </div>
        `;
    }
    
    // Portfolio Analysis
    if (results.portfolio_analysis) {
        html += `
            <div class="result-section">
                <h3>💼 Portfolio Analysis</h3>
                <div class="result-content">${formatText(results.portfolio_analysis)}</div>
            </div>
        `;
    }
    
    // Tax Optimization
    if (results.tax_optimization) {
        html += `
            <div class="result-section">
                <h3>💰 Tax Optimization Opportunities</h3>
                <div class="result-content">${formatText(results.tax_optimization)}</div>
            </div>
        `;
    }
    
    // Market Research
    if (results.market_research) {
        html += `
            <div class="result-section">
                <h3>📊 Market Research & Trends</h3>
                <div class="result-content">${formatText(results.market_research)}</div>
            </div>
        `;
    }
    
    // Financial Planning
    if (results.financial_plan) {
        html += `
            <div class="result-section">
                <h3>🎯 Financial Planning</h3>
                <div class="result-content">${formatText(results.financial_plan)}</div>
            </div>
        `;
    }
    
    // Compliance Review
    if (results.compliance_review) {
        html += `
            <div class="result-section">
                <h3>✅ Compliance Review</h3>
                <div class="result-content">${formatText(results.compliance_review)}</div>
            </div>
        `;
    }
    
    // Disclaimer
    html += `
        <div class="result-section" style="background: #fef3c7; border-left-color: #f59e0b;">
            <h3>⚠️ Important Notice</h3>
            <div class="result-content">
                <p><strong>This report is for informational purposes only and does not constitute financial advice.</strong></p>
                <p>Please consult with licensed financial professionals before making investment decisions.</p>
            </div>
        </div>
    `;
    
    resultsContent.innerHTML = html;
}

// Format text (convert markdown-like formatting to HTML)
function formatText(text) {
    if (!text) return '';
    
    // Convert markdown headers
    text = text.replace(/^### (.*$)/gim, '<h4>$1</h4>');
    text = text.replace(/^## (.*$)/gim, '<h4>$1</h4>');
    text = text.replace(/^# (.*$)/gim, '<h4>$1</h4>');
    
    // Convert bold
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert bullet points
    text = text.replace(/^\* (.*$)/gim, '<li>$1</li>');
    text = text.replace(/^\+ (.*$)/gim, '<li>$1</li>');
    text = text.replace(/^- (.*$)/gim, '<li>$1</li>');
    
    // Wrap consecutive list items in ul tags
    text = text.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
    
    // Convert numbered lists
    text = text.replace(/^\d+\. (.*$)/gim, '<li>$1</li>');
    
    // Convert line breaks to paragraphs
    let paragraphs = text.split(/\n\n+/);
    paragraphs = paragraphs.map(p => {
        p = p.trim();
        if (!p) return '';
        if (p.startsWith('<h4>') || p.startsWith('<ul>') || p.startsWith('<li>')) {
            return p;
        }
        return `<p>${p}</p>`;
    });
    text = paragraphs.join('');
    
    // Clean up empty paragraphs
    text = text.replace(/<p>\s*<\/p>/g, '');
    
    return text;
}

// Set loading state
function setLoadingState(loading) {
    submitBtn.disabled = loading;
    if (loading) {
        submitText.style.display = 'none';
        loadingSpinner.style.display = 'inline-block';
    } else {
        submitText.style.display = 'inline';
        loadingSpinner.style.display = 'none';
    }
}

// Show error
function showError(message) {
    resultsContent.innerHTML = `
        <div class="error">
            <h3>❌ Error</h3>
            <p>${escapeHtml(message)}</p>
            <p style="margin-top: 10px; font-size: 0.9rem; opacity: 0.8;">
                Please check your input and try again. Make sure all required fields are filled correctly.
            </p>
        </div>
    `;
    formSection.style.display = 'none';
    resultsSection.style.display = 'block';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

