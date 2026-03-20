const UkarimuApp = {
    init: function() {
        this.initSidebar();
        this.initAlerts();
        this.Gamification.init();
    },

    initSidebar: function() {
        const sidebarToggle = document.body.querySelector('#sidebarToggle');
        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', event => {
                event.preventDefault();
                document.body.classList.toggle('sb-sidenav-toggled');
            });
        }
    },

    initAlerts: function() {
        // Auto-dismiss alerts after 5 seconds
        setTimeout(function() {
            let alerts = document.querySelectorAll('.alert');
            alerts.forEach(function(alert) {
                // Check if bootstrap is available to close nicely, otherwise just hide
                if (window.bootstrap) {
                    var bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                } else {
                    alert.style.display = 'none';
                }
            });
        }, 5000);
    },

    Gamification: {
        xpKey: 'ukarimu_xp',

        init: function() {
            this.updateXPDisplay(this.getXP());
            this.bindEvents();
        },

        getXP: function() {
            return parseInt(localStorage.getItem(this.xpKey) || '0');
        },

        addXP: function(points) {
            let newXp = this.getXP() + points;
            localStorage.setItem(this.xpKey, newXp);
            this.updateXPDisplay(newXp);
            this.showReward(`+${points} XP! Great Job!`);
        },

        updateXPDisplay: function(amount) {
            const badge = document.getElementById('xp-badge');
            if (badge) {
                badge.innerText = `✨ ${amount} XP`;
                // Simple pulse animation
                badge.style.transform = "scale(1.2)";
                setTimeout(() => badge.style.transform = "scale(1)", 200);
            }
        },

        showReward: function(text) {
            // Create popup element
            let popup = document.createElement('div');
            popup.className = 'reward-popup show';
            popup.innerText = text;
            document.body.appendChild(popup);
            
            // Remove after 1.5s
            setTimeout(() => {
                popup.classList.remove('show');
                setTimeout(() => popup.remove(), 300);
            }, 1500);
        },

        bindEvents: function() {
            document.body.addEventListener('click', (e) => {
                // Handle XP Trigger (Download/View Links)
                if (e.target.closest('.learning-link')) {
                    this.addXP(10);
                }

                // Handle Heart/Like Buttons
                const favBtn = e.target.closest('.favorite-btn');
                if (favBtn) {
                    e.preventDefault(); // Prevent any default button action
                    
                    // Use trim() to safely compare text content
                    const currentText = favBtn.textContent.trim();
                    if (currentText === '🤍') {
                        favBtn.textContent = '❤️';
                        favBtn.classList.remove('btn-outline-secondary');
                        favBtn.classList.add('btn-outline-danger'); // Make border red
                    } else {
                        favBtn.textContent = '🤍';
                        favBtn.classList.add('btn-outline-secondary');
                        favBtn.classList.remove('btn-outline-danger');
                    }
                    
                    // Pop animation
                    favBtn.style.transform = "scale(1.2)";
                    setTimeout(() => favBtn.style.transform = "scale(1)", 200);
                }
            });
        }
    }
};

document.addEventListener('DOMContentLoaded', function() {
    UkarimuApp.init();
});