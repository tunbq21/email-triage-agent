document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('runTriageBtn');
    const btnText = runBtn.querySelector('.btn-text');
    const btnLoader = runBtn.querySelector('.btn-loader');
    const statusText = document.getElementById('statusText');
    const emailList = document.getElementById('emailList');
    const processedCount = document.getElementById('processedCount');
    
    // Details View Elements
    const focusEmpty = document.querySelector('.focus-empty');
    const focusContent = document.querySelector('.focus-content');
    const detailTags = document.getElementById('detailTags');
    const detailSubject = document.getElementById('detailSubject');
    const detailSender = document.getElementById('detailSender');
    const detailDate = document.getElementById('detailDate');
    const detailBody = document.getElementById('detailBody');
    const detailActionCard = document.getElementById('detailActionCard');
    const detailActionText = document.getElementById('detailActionText');

    let currentEmails = [];

    runBtn.addEventListener('click', async () => {
        // Set loading state
        btnText.style.opacity = '0';
        btnLoader.style.display = 'block';
        runBtn.disabled = true;
        statusText.textContent = "Scanning inbox and running AI models...";
        
        try {
            const response = await fetch('/api/triage');
            const data = await response.json();
            
            if (response.ok) {
                currentEmails = data.emails;
                renderEmailList(currentEmails);
                statusText.textContent = `Processed ${currentEmails.length} new signals.`;
            } else {
                statusText.textContent = `Error: ${data.error || 'Unknown error occurred.'}`;
            }
        } catch (error) {
            statusText.textContent = `Connection error: ${error.message}`;
        } finally {
            // Reset loading state
            btnText.style.opacity = '1';
            btnLoader.style.display = 'none';
            runBtn.disabled = false;
        }
    });

    function renderEmailList(emails) {
        emailList.innerHTML = '';
        processedCount.textContent = emails.length;

        if (emails.length === 0) {
            emailList.innerHTML = '<div class="empty-state"><p>No new signals found.</p></div>';
            return;
        }

        emails.forEach((email, index) => {
            const card = document.createElement('div');
            card.className = 'email-card';
            card.style.animationDelay = `${index * 0.05}s`;
            
            const pClass = email.classification.priority.toLowerCase();
            const tagClass = pClass === 'p0' ? 'tag-p0' : (pClass === 'p3' ? 'tag-archive' : 'tag-p2');
            
            card.innerHTML = `
                <div class="card-tags">
                    <span class="tag ${tagClass}">${email.classification.priority}</span>
                    <span class="tag tag-category">${email.classification.category}</span>
                </div>
                <h3 class="card-subject">${email.subject}</h3>
                <div class="card-sender">${escapeHTML(email.sender)}</div>
            `;
            
            card.addEventListener('click', () => {
                document.querySelectorAll('.email-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                showDetails(email, tagClass);
            });
            
            emailList.appendChild(card);
        });
    }

    function showDetails(email, priorityTagClass) {
        focusEmpty.style.display = 'none';
        focusContent.style.display = 'block';
        
        detailSubject.textContent = email.subject;
        detailSender.textContent = escapeHTML(email.sender);
        detailDate.textContent = email.date || 'Unknown Date';
        detailBody.textContent = email.body;
        
        detailTags.innerHTML = `
            <span class="tag ${priorityTagClass}">${email.classification.priority}</span>
            <span class="tag tag-category">${email.classification.category}</span>
            <span class="tag tag-category">CONFIDENCE: ${email.classification.confidence * 100}%</span>
        `;
        
        // Action Card styling based on priority
        detailActionCard.className = 'action-card';
        if (email.classification.priority === 'P0') {
            detailActionCard.classList.add('action-p0');
            detailActionText.innerHTML = `<strong>Action:</strong> Auto-replied and escalated.<br><br>The AI has generated a draft response addressing the critical issue.`;
        } else if (email.action === 'archived') {
            detailActionText.innerHTML = `<strong>Action:</strong> Archived.<br><br>Signal classified as noise. Safely ignored.`;
        } else {
            detailActionText.innerHTML = `<strong>Action:</strong> Pending Human Review.<br><br>Signal requires your attention.`;
        }
    }

    function escapeHTML(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }
});
