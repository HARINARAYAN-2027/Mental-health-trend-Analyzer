/**
 * Mental Health Trend Analyzer - Timeline Trend Waveform Visualizer Engine
 */

document.addEventListener('DOMContentLoaded', async () => {
    const API_BASE = "http://127.0.0.1:5000/api";
    const userId = localStorage.getItem('mentalflow_user_id') || 1;
    const canvasTrends = document.getElementById('canvas-trends-timeline');

    // Default structural fallback curves arrays
    let trendLabels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'];
    let anxietyData = [20, 28, 35, 30, 25];
    let stressData = [30, 35, 45, 40, 35];
    let keywordCounts = { exams: 42, stress: 28, lonely: 14 };

    try {
        // Fetch raw time-series matrices dataset from SQLite endpoints
        const response = await fetch(`${API_BASE}/trend-series?userId=${userId}`);
        
        if (response.ok) {
            const data = await response.json();
            console.log("Timeline time-series metrics sync completed.");
            
            trendLabels = data.labels || trendLabels;
            anxietyData = data.anxiety_series || anxietyData;
            stressData = data.stress_series || stressData;
            keywordCounts = data.keywords || keywordCounts;
        }
    } catch (err) {
        console.warn("Backend metrics offline. Falling back to local visual simulation context.", err);
    }

    // ==================== 1. Render Dynamic High Frequency Keyword Densities ====================
    const maxHits = Math.max(keywordCounts.exams, keywordCounts.stress, keywordCounts.lonely, 1);
    
    if(document.getElementById('kw-exams-hits')) {
        document.getElementById('kw-exams-hits').innerText = `${keywordCounts.exams} Hits`;
        document.getElementById('kw-exams-bar').style.width = `${(keywordCounts.exams / maxHits) * 100}%`;
    }
    if(document.getElementById('kw-stress-hits')) {
        document.getElementById('kw-stress-hits').innerText = `${keywordCounts.stress} Hits`;
        document.getElementById('kw-stress-bar').style.width = `${(keywordCounts.stress / maxHits) * 100}%`;
    }
    if(document.getElementById('kw-lonely-hits')) {
        document.getElementById('kw-lonely-hits').innerText = `${keywordCounts.lonely} Hits`;
        document.getElementById('kw-lonely-bar').style.width = `${(keywordCounts.lonely / maxHits) * 100}%`;
    }

    // ==================== 2. Initialize Chart.js Line Progression Waveform ====================
    if (canvasTrends) {
        const ctxTrends = canvasTrends.getContext('2d');
        new Chart(ctxTrends, {
            type: 'line',
            data: {
                labels: trendLabels,
                datasets: [
                    {
                        label: 'Anxiety Density Indicator',
                        data: anxietyData,
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.04)',
                        fill: true,
                        tension: 0.38,
                        borderWidth: 2,
                        pointRadius: 3,
                        pointBackgroundColor: '#8b5cf6'
                    },
                    {
                        label: 'Stress Density Indicator',
                        data: stressData,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.04)',
                        fill: true,
                        tension: 0.38,
                        borderWidth: 2,
                        pointRadius: 3,
                        pointBackgroundColor: '#3b82f6'
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { color: '#94a3b8', font: { family: 'Poppins' } },
                        grid: { color: 'rgba(255, 255, 255, 0.04)' }
                    },
                    x: {
                        ticks: { color: '#94a3b8', font: { family: 'Poppins', size: 11 } },
                        grid: { display: false }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: { color: '#f1f5f9', font: { family: 'Poppins', size: 12 } }
                    }
                }
            }
        });
    }
});