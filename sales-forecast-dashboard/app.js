// AI-Powered Sales Forecasting Dashboard
class SalesForecastingDashboard {
    constructor() {
        this.data = {
            kpi_data: {
                total_historical_sales: 3225905.41,
                average_daily_sales: 1235.67,
                total_90_day_forecast: 125250.45,
                model_accuracy: "92%"
            },
            monthly_forecast: [
                {"month": "Jan", "forecast": 1330.69, "lower": -1400.38, "upper": 4056.45},
                {"month": "Feb", "forecast": 1254.99, "lower": -1459.07, "upper": 3975.84},
                {"month": "Mar", "forecast": 1553.28, "lower": -1154.73, "upper": 4234.54}
            ],
            category_data: [
                {"category": "Furniture", "sales": 1013436.73, "profit": 103773.95},
                {"category": "Office Supplies", "sales": 1120798.83, "profit": 115069.41},
                {"category": "Technology", "sales": 1091669.85, "profit": 114191.48}
            ],
            insights: [
                "Technology category shows highest profit margins at 10.5%",
                "Office Supplies maintains most consistent sales volume",
                "Q1 2025 forecast indicates 12% growth potential",
                "Seasonal patterns suggest inventory buildup needed for Q4",
                "Model confidence is highest for Technology and Office Supplies categories"
            ],
            business_recommendations: [
                "Increase Technology inventory by 15% for Q2 2025",
                "Focus marketing efforts on Office Supplies during low seasons",
                "Implement dynamic pricing for Furniture category",
                "Monitor forecast confidence intervals for risk management",
                "Plan promotional campaigns around predicted peak periods"
            ]
        };
        
        this.init();
    }

    init() {
        this.displayCurrentDate();
        this.populateInsights();
        this.setupEventListeners();
        this.animateElements();
        this.addInteractiveEffects();
    }

    displayCurrentDate() {
        const currentDate = new Date();
        const options = {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        
        const formattedDate = currentDate.toLocaleDateString('en-US', options);
        document.getElementById('current-date').textContent = formattedDate;
    }

    populateInsights() {
        // Populate insights list
        const insightsList = document.getElementById('insights-list');
        if (insightsList) {
            insightsList.innerHTML = '';
            this.data.insights.forEach(insight => {
                const li = document.createElement('li');
                li.textContent = insight;
                insightsList.appendChild(li);
            });
        }

        // Populate recommendations list
        const recommendationsList = document.getElementById('recommendations-list');
        if (recommendationsList) {
            recommendationsList.innerHTML = '';
            this.data.business_recommendations.forEach(recommendation => {
                const li = document.createElement('li');
                li.textContent = recommendation;
                recommendationsList.appendChild(li);
            });
        }
    }

    setupEventListeners() {
        // Download forecast button
        const downloadBtn = document.getElementById('download-forecast');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => {
                this.downloadForecastChart();
            });
        }

        // Refresh data button
        const refreshBtn = document.getElementById('refresh-data');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshDashboard();
            });
        }

        // Export report button
        const exportBtn = document.getElementById('export-report');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => {
                this.exportReport();
            });
        }

        // KPI card interactions
        const kpiCards = document.querySelectorAll('.kpi-card');
        kpiCards.forEach(card => {
            card.addEventListener('click', () => {
                this.showKpiDetails(card.dataset.kpi);
            });
        });

        // Window resize handler
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    downloadForecastChart() {
        // Simulate download
        this.showNotification('Forecast chart download started...', 'success');
        
        // Create a temporary link to simulate download
        const link = document.createElement('a');
        link.href = 'https://ppl-ai-code-interpreter-files.s3.amazonaws.com/web/direct-files/08914a9a4f080294ddcfb29ce1942b09/ada3727c-b6cb-48e9-a709-15487e6f8fd9/789de56a.png';
        link.download = 'daily-sales-forecast.png';
        link.target = '_blank';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    refreshDashboard() {
        this.showNotification('Refreshing dashboard data...', 'info');
        
        // Simulate data refresh with loading state
        const loadingElement = this.createLoadingElement();
        const mainContent = document.querySelector('.charts-section');
        
        if (mainContent) {
            mainContent.style.opacity = '0.5';
            mainContent.style.pointerEvents = 'none';
        }

        setTimeout(() => {
            this.displayCurrentDate();
            this.animateElements();
            
            if (mainContent) {
                mainContent.style.opacity = '1';
                mainContent.style.pointerEvents = 'auto';
            }
            
            this.showNotification('Dashboard refreshed successfully!', 'success');
        }, 2000);
    }

    exportReport() {
        this.showNotification('Generating comprehensive sales report...', 'info');
        
        // Simulate report generation
        setTimeout(() => {
            const reportData = this.generateReportData();
            this.downloadReport(reportData);
            this.showNotification('Sales report exported successfully!', 'success');
        }, 1500);
    }

    generateReportData() {
        return {
            title: 'AI-Powered Sales Forecasting Report',
            date: new Date().toLocaleDateString(),
            kpis: this.data.kpi_data,
            insights: this.data.insights,
            recommendations: this.data.business_recommendations,
            categories: this.data.category_data,
            forecast: this.data.monthly_forecast
        };
    }

    downloadReport(data) {
        const reportContent = `
AI-POWERED SALES FORECASTING REPORT
Generated: ${data.date}

KEY PERFORMANCE INDICATORS:
- Total Historical Sales: $${(data.kpis.total_historical_sales / 1000000).toFixed(2)}M
- Average Daily Sales: $${data.kpis.average_daily_sales.toFixed(0)}
- 90-Day Forecast: $${(data.kpis.total_90_day_forecast / 1000).toFixed(0)}K
- Model Accuracy: ${data.kpis.model_accuracy}

KEY INSIGHTS:
${data.insights.map(insight => `- ${insight}`).join('\n')}

BUSINESS RECOMMENDATIONS:
${data.recommendations.map(rec => `- ${rec}`).join('\n')}

CATEGORY PERFORMANCE:
${data.categories.map(cat => 
    `- ${cat.category}: $${(cat.sales / 1000000).toFixed(2)}M sales, $${(cat.profit / 1000).toFixed(0)}K profit`
).join('\n')}

QUARTERLY FORECAST (Q1 2025):
${data.forecast.map(month => 
    `- ${month.month}: $${month.forecast.toFixed(0)} (Range: $${month.lower.toFixed(0)} - $${month.upper.toFixed(0)})`
).join('\n')}
        `;

        const blob = new Blob([reportContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `sales-forecast-report-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    showKpiDetails(kpiType) {
        const details = {
            'total-sales': {
                title: 'Total Historical Sales',
                description: 'Cumulative sales across all categories and time periods in our dataset.',
                trend: '+8.2% compared to previous period',
                insight: 'Strong overall performance with consistent growth trajectory.'
            },
            'avg-daily': {
                title: 'Average Daily Sales',
                description: 'Mean daily sales calculated from historical transaction data.',
                trend: '+3.1% upward trend',
                insight: 'Steady daily performance indicates stable business operations.'
            },
            'forecast': {
                title: '90-Day Forecast',
                description: 'AI-predicted sales for the next 90 days based on historical patterns.',
                trend: 'Q1 2025 projection',
                insight: '12% growth potential identified for the forecast period.'
            },
            'accuracy': {
                title: 'Model Accuracy',
                description: 'Mean Absolute Percentage Error (MAPE) of our forecasting model.',
                trend: '92% confidence level',
                insight: 'High accuracy indicates reliable predictions for business planning.'
            }
        };

        const detail = details[kpiType];
        if (detail) {
            this.showModal(detail);
        }
    }

    showModal(detail) {
        // Create modal
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${detail.title}</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body">
                    <p class="modal-description">${detail.description}</p>
                    <div class="modal-trend">${detail.trend}</div>
                    <div class="modal-insight">${detail.insight}</div>
                </div>
            </div>
        `;

        // Add modal styles
        const style = document.createElement('style');
        style.textContent = `
            .modal-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.5);
                display: flex;
                align-items: center;
                justify-content: center;
                z-index: 1000;
                animation: fadeIn 0.3s ease-out;
            }
            .modal-content {
                background: var(--color-surface);
                border-radius: var(--radius-lg);
                max-width: 500px;
                width: 90%;
                box-shadow: var(--shadow-lg);
                animation: slideIn 0.3s ease-out;
            }
            .modal-header {
                padding: var(--space-20) var(--space-24);
                border-bottom: 1px solid var(--color-border);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .modal-header h3 {
                margin: 0;
                color: var(--color-text);
                font-size: var(--font-size-xl);
            }
            .modal-close {
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                color: var(--color-text-secondary);
                padding: var(--space-4);
            }
            .modal-close:hover {
                color: var(--color-text);
            }
            .modal-body {
                padding: var(--space-24);
            }
            .modal-description {
                margin-bottom: var(--space-16);
                color: var(--color-text-secondary);
                line-height: var(--line-height-normal);
            }
            .modal-trend {
                padding: var(--space-8) var(--space-12);
                background: var(--color-bg-3);
                color: var(--color-success);
                border-radius: var(--radius-base);
                font-weight: var(--font-weight-semibold);
                margin-bottom: var(--space-12);
                display: inline-block;
            }
            .modal-insight {
                color: var(--color-text);
                font-style: italic;
                font-size: var(--font-size-sm);
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(modal);

        // Close modal functionality
        const closeBtn = modal.querySelector('.modal-close');
        const closeModal = () => {
            modal.remove();
            style.remove();
        };

        closeBtn.addEventListener('click', closeModal);
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });

        // Close on Escape key
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                closeModal();
                document.removeEventListener('keydown', handleEscape);
            }
        };
        document.addEventListener('keydown', handleEscape);
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification--${type}`;
        notification.textContent = message;

        // Add notification styles
        const style = document.createElement('style');
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: var(--space-16) var(--space-20);
                border-radius: var(--radius-base);
                color: white;
                font-weight: var(--font-weight-medium);
                z-index: 1000;
                animation: slideInRight 0.3s ease-out;
                max-width: 400px;
            }
            .notification--success {
                background: var(--color-success);
            }
            .notification--info {
                background: var(--color-info);
            }
            .notification--error {
                background: var(--color-error);
            }
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;

        document.head.appendChild(style);
        document.body.appendChild(notification);

        // Remove notification after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideInRight 0.3s ease-out reverse';
            setTimeout(() => {
                notification.remove();
                style.remove();
            }, 300);
        }, 3000);
    }

    createLoadingElement() {
        const loading = document.createElement('div');
        loading.className = 'loading';
        loading.innerHTML = `
            <div class="loading-spinner"></div>
            <span>Loading...</span>
        `;
        return loading;
    }

    animateElements() {
        // Animate KPI cards
        const kpiCards = document.querySelectorAll('.kpi-card');
        kpiCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease-out';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 200);
        });

        // Animate chart cards
        const chartCards = document.querySelectorAll('.chart-card');
        chartCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateX(-30px)';
            setTimeout(() => {
                card.style.transition = 'all 0.5s ease-out';
                card.style.opacity = '1';
                card.style.transform = 'translateX(0)';
            }, 800 + index * 300);
        });
    }

    addInteractiveEffects() {
        // Enhanced hover effects for KPI cards
        const kpiCards = document.querySelectorAll('.kpi-card');
        kpiCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px) scale(1.02)';
                card.style.transition = 'all 0.3s ease-out';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Chart card hover effects
        const chartCards = document.querySelectorAll('.chart-card');
        chartCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-3px)';
                card.style.transition = 'all 0.3s ease-out';
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
            });
        });

        // Button click effects
        const buttons = document.querySelectorAll('.btn');
        buttons.forEach(button => {
            button.addEventListener('click', (e) => {
                // Create ripple effect
                const rect = button.getBoundingClientRect();
                const ripple = document.createElement('span');
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;

                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.style.position = 'absolute';
                ripple.style.borderRadius = '50%';
                ripple.style.background = 'rgba(255, 255, 255, 0.5)';
                ripple.style.pointerEvents = 'none';
                ripple.style.animation = 'ripple 0.6s ease-out';

                button.appendChild(ripple);

                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });

        // Add ripple animation
        const rippleStyle = document.createElement('style');
        rippleStyle.textContent = `
            @keyframes ripple {
                0% {
                    transform: scale(0);
                    opacity: 1;
                }
                100% {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(rippleStyle);
    }

    handleResize() {
        // Handle responsive behavior
        const screenWidth = window.innerWidth;
        
        if (screenWidth < 768) {
            this.adjustMobileLayout();
        } else {
            this.adjustDesktopLayout();
        }
    }

    adjustMobileLayout() {
        const chartsGrid = document.querySelector('.charts-grid');
        if (chartsGrid) {
            chartsGrid.style.gridTemplateColumns = '1fr';
        }

        const analysisGrid = document.querySelector('.analysis-grid');
        if (analysisGrid) {
            analysisGrid.style.gridTemplateColumns = '1fr';
        }
    }

    adjustDesktopLayout() {
        const chartsGrid = document.querySelector('.charts-grid');
        if (chartsGrid) {
            chartsGrid.style.gridTemplateColumns = '2fr 1fr';
        }

        const analysisGrid = document.querySelector('.analysis-grid');
        if (analysisGrid) {
            analysisGrid.style.gridTemplateColumns = '1fr 1fr';
        }
    }

    // Utility methods
    formatCurrency(value) {
        if (value >= 1000000) {
            return `$${(value / 1000000).toFixed(2)}M`;
        } else if (value >= 1000) {
            return `$${(value / 1000).toFixed(0)}K`;
        } else {
            return `$${value.toFixed(0)}`;
        }
    }

    formatPercentage(value) {
        return `${(value * 100).toFixed(1)}%`;
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize the dashboard
    const dashboard = new SalesForecastingDashboard();

    // Add loading completion indicator
    setTimeout(() => {
        document.body.classList.add('dashboard-loaded');
    }, 1000);

    // Global error handling
    window.addEventListener('error', (e) => {
        console.error('Dashboard error:', e.error);
        
        // Show user-friendly error message
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--color-error);
            color: white;
            padding: 16px 20px;
            border-radius: 8px;
            z-index: 1000;
            max-width: 400px;
        `;
        notification.textContent = 'An error occurred. Please refresh the page.';
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    });

    // Performance monitoring
    if ('performance' in window) {
        window.addEventListener('load', () => {
            const loadTime = performance.now();
            console.log(`Dashboard loaded in ${loadTime.toFixed(2)}ms`);
        });
    }
});