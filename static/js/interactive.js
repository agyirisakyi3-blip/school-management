// Interactive features for SchoolMS

document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Live Search with AJAX
    initLiveSearch();
    
    // 2. Interactive Charts
    initCharts();
    
    // 3. Real-time Notifications
    initNotifications();
    
    // 4. Dynamic Table Sorting
    initTableSort();
    
    // 5. Auto-save Forms
    initAutoSave();
    
    // 6. Inline Editing
    initInlineEdit();
});

// Live Search
function initLiveSearch() {
    const searchInput = document.getElementById('globalSearchInput');
    if (!searchInput) return;
    
    let debounceTimer;
    searchInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        const query = this.value;
        
        if (query.length < 2) {
            document.getElementById('searchResults').innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-search fs-1 d-block mb-2"></i>
                    <p class="mb-0">Start typing to search...</p>
                </div>`;
            return;
        }
        
        debounceTimer = setTimeout(() => {
            fetch(`/api/search/?q=${encodeURIComponent(query)}`)
                .then(res => res.json())
                .then(data => displaySearchResults(data))
                .catch(() => {});
        }, 300);
    });
}

function displaySearchResults(results) {
    const container = document.getElementById('searchResults');
    if (!results.length) {
        container.innerHTML = `
            <div class="text-center text-muted py-4">
                <i class="bi bi-search fs-1 d-block mb-2"></i>
                <p class="mb-0">No results found</p>
            </div>`;
        return;
    }
    
    container.innerHTML = results.map(r => `
        <a href="${r.url}" class="search-result-item d-flex align-items-center p-2 text-decoration-none">
            <div class="bg-primary-subtle rounded p-2 me-3">
                <i class="bi bi-${r.icon || 'person'}"></i>
            </div>
            <div>
                <strong>${r.name}</strong>
                <small class="d-block text-muted">${r.type}</small>
            </div>
        </a>
    `).join('');
}

// Interactive Charts (using Chart.js)
function initCharts() {
    if (typeof Chart === 'undefined') return;
    
    // Attendance Chart
    const attCtx = document.getElementById('attendanceChart');
    if (attCtx) {
        new Chart(attCtx, {
            type: 'doughnut',
            data: {
                labels: ['Present', 'Absent', 'Late'],
                datasets: [{
                    data: [
                        parseInt(attCtx.dataset.present || 0),
                        parseInt(attCtx.dataset.absent || 0),
                        parseInt(attCtx.dataset.late || 0)
                    ],
                    backgroundColor: ['#198754', '#dc3545', '#ffc107']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }
    
    // Fee Collection Chart
    const feeCtx = document.getElementById('feeChart');
    if (feeCtx) {
        new Chart(feeCtx, {
            type: 'bar',
            data: {
                labels: ['Collected', 'Pending'],
                datasets: [{
                    label: 'Amount',
                    data: [
                        parseInt(feeCtx.dataset.collected || 0),
                        parseInt(feeCtx.dataset.pending || 0)
                    ],
                    backgroundColor: ['#198754', '#ffc107']
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }
}

// Real-time Notifications
function initNotifications() {
    // Poll for new notifications every 30 seconds
    setInterval(checkNotifications, 30000);
    
    function checkNotifications() {
        fetch('/api/notifications/unread/')
            .then(res => res.json())
            .then(data => {
                if (data.count > 0) {
                    updateNotificationBadge(data.count);
                    if (data.notifications) {
                        showToastNotifications(data.notifications);
                    }
                }
            })
            .catch(() => {});
    }
}

function updateNotificationBadge(count) {
    const badge = document.querySelector('.notification-badge');
    if (badge) {
        badge.textContent = count;
        badge.classList.remove('d-none');
    }
}

function showToastNotifications(notifications) {
    notifications.forEach(n => {
        if (!Notification.permission || Notification.permission === 'granted') {
            new Notification(n.title, {
                body: n.message,
                icon: '/static/icons/icon.svg'
            });
        }
    });
}

// Table Sorting
function initTableSort() {
    document.querySelectorAll('.table-sortable th').forEach(th => {
        th.addEventListener('click', () => {
            const table = th.closest('table');
            const index = Array.from(th.parentNode.children).indexOf(th);
            const asc = !th.classList.contains('sort-asc');
            
            table.querySelectorAll('th').forEach(h => {
                h.classList.remove('sort-asc', 'sort-desc');
            });
            th.classList.add(asc ? 'sort-asc' : 'sort-desc');
            
            const rows = Array.from(table.querySelectorAll('tbody tr'));
            rows.sort((a, b) => {
                const aVal = a.children[index].textContent.trim();
                const bVal = b.children[index].textContent.trim();
                return asc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
            });
            
            table.querySelector('tbody').append(...rows);
        });
    });
}

// Auto-save Forms
function initAutoSave() {
    document.querySelectorAll('[data-autosave]').forEach(form => {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                const data = new FormData(form);
                fetch(form.dataset.autosave, {
                    method: 'POST',
                    body: data,
                    headers: { 'X-CSRFToken': getCookie('csrftoken') }
                }).then(() => {
                    showToast('Saved!', 'success');
                });
            });
        });
    });
}

// Inline Editing
function initInlineEdit() {
    document.querySelectorAll('[data-inline-edit]').forEach(el => {
        el.style.cursor = 'pointer';
        el.addEventListener('click', function() {
            const current = this.textContent.trim();
            const input = document.createElement('input');
            input.type = 'text';
            input.value = current;
            input.className = 'form-control form-control-sm';
            
            this.textContent = '';
            this.appendChild(input);
            input.focus();
            
            const save = () => {
                const value = input.value;
                this.textContent = value;
                // Save via AJAX
                fetch(this.dataset.inlineEdit, {
                    method: 'POST',
                    body: JSON.stringify({ value }),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
            };
            
            input.addEventListener('blur', save);
            input.addEventListener('keypress', e => {
                if (e.key === 'Enter') { e.preventDefault(); input.blur(); }
            });
        });
    });
}

// Helper: Get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(c => {
            let cookie = c.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}

// Helper: Show Toast
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}