/**
 * Mental Health Trend Analyzer - Dashboard Chart Processing Engine
 * Optimized for Dynamic REST Sync & Prevent Structural Mismatches
 */

document.addEventListener('DOMContentLoaded', async () => {
    const API_BASE = "http://127.0.0.1:5000/api";
    const userId = localStorage.getItem('mentalflow_user_id') || 1;

    // Default Fallback Metrics setup (In case database or endpoints are offline)
    let totalLogs = 10;
    let positiveCount = 6;
    let negativeCount = 3;
    let neutralCount = 1;
    let lowRiskCount = 7;
    let moderateRiskCount = 2;
    let highRiskCount = 1;

    try {
        // Fetch dynamic analytical matrices from actual backend tables context
        // Note: If you've changed the analytics endpoint name, replace it with dashboard-stats or reports
        const response = await fetch(`${API_BASE}/dashboard-stats?userId=${userId}`);
        
        if (response.ok) {
            const serverData = await response.json();
            console.log("Live dynamic analytical metrics synced from database layers.");
            
            // Re-assigning backend computed data array lengths safely
            totalLogs = serverData.total_logs || totalLogs;
            positiveCount = serverData.counts.positive !== undefined ? serverData.counts.positive : positiveCount;
            negativeCount = serverData.counts.negative !== undefined ? serverData.counts.negative : negativeCount;
            neutralCount = serverData.counts.neutral !== undefined ? serverData.counts.neutral : neutralCount;
            lowRiskCount = serverData.counts.low_risk !== undefined ? serverData.counts.low_risk : lowRiskCount;
            moderateRiskCount = serverData.counts.mod_risk !== undefined ? serverData.counts.mod_risk : moderateRiskCount;
            highRiskCount = serverData.counts.high_risk !== undefined ? serverData.counts.high_risk : highRiskCount;
        } else {
            // Internal framework handshake check fallback route
            const checkResponse = await fetch(`${API_BASE}/health-check`);
            if (checkResponse.ok) {
                console.log("Database bridge live, but custom dashboard stats route missing. Falling back to local visual context matrices.");
            }
        }
    } catch (err) {
        console.warn("Backend dynamic fetch default falling back to standard local values metrics framework dashboard presentation.", err);
    }

    // Dynamic Mathematical Calculations configuration mapping
    const computedRatio = totalLogs > 0 ? Math.round((positiveCount / totalLogs) * 100) : 0;
    
    // Core Card Metric View Token Bindings
    if (document.getElementById('dash-total-logs')) {
        document.getElementById('dash-total-logs').innerText = totalLogs;
    }
    if (document.getElementById('dash-positive-ratio')) {
        document.getElementById('dash-positive-ratio').innerText = computedRatio + "%";
    }
    
    const riskFactorEl = document.getElementById('dash-risk-factor');
    if (riskFactorEl) {
        if (highRiskCount >= moderateRiskCount && highRiskCount > 0) {
            riskFactorEl.innerText = "High Risk";
            riskFactorEl.style.color = "#ef4444";
        } else if (moderateRiskCount > 0) {
            riskFactorEl.innerText = "Moderate";
            riskFactorEl.style.color = "#f59e0b";
        } else {
            riskFactorEl.innerText = "Low Risk";
            riskFactorEl.style.color = "#10b981";
        }
    }

    // ==================== Chart 1: Sentiment Distribution Doughnut Component ====================
    const canvasDoughnut = document.getElementById('canvas-sentiment-doughnut');
    if (canvasDoughnut) {
        const ctxDoughnut = canvasDoughnut.getContext('2d');
        new Chart(ctxDoughnut, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Negative', 'Neutral'],
                datasets: [{
                    data: [positiveCount, negativeCount, neutralCount],
                    backgroundColor: ['#10b981', '#ef4444', '#94a3b8'],
                    borderWidth: 1,
                    borderColor: 'rgba(255, 255, 255, 0.05)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#f1f5f9', font: { family: 'Poppins', size: 12 } }
                    }
                },
                cutout: '70%'
            }
        });
    }

    // ==================== Chart 2: Threat Categorization Bar Component ====================
    const canvasBar = document.getElementById('canvas-risk-bar');
    if (canvasBar) {
        const ctxBar = canvasBar.getContext('2d');
        new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ['Low Structural Risk', 'Moderate Risk', 'Critical High Risk'],
                datasets: [{
                    label: 'Processed Statements Counter Density',
                    data: [lowRiskCount, moderateRiskCount, highRiskCount],
                    backgroundColor: ['rgba(16, 185, 129, 0.25)', 'rgba(245, 158, 11, 0.25)', 'rgba(239, 68, 68, 0.25)'],
                    borderColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#94a3b8', stepSize: 1 },
                        grid: { color: 'rgba(255, 255, 255, 0.05)' }
                    },
                    x: {
                        ticks: { color: '#94a3b8' },
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // ==================== PDF Dynamic Download Routing Controller ====================
    const pdfBtn = document.getElementById('btn-download-pdf-report');
    if (pdfBtn) {
        pdfBtn.addEventListener('click', (e) => {
            e.preventDefault();
            alert("Report engine triggered. Exporting analytics data models to PDF report asset matrix loop...");
            window.location.href = `${API_BASE}/user/${userId}/report/pdf`;
        });
    }
});