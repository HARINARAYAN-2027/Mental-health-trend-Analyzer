/**
 * Mental Health Trend Analyzer - API Interaction Controller for Real-Time Analytics
 * Secured with Session Lock to prevent Live Server auto-refresh data loss
 */

const BASE_API_URL = "http://127.0.0.1:5000/api";

document.addEventListener('DOMContentLoaded', () => {
    
    // Core Elements Selection
    const textInput = document.getElementById('analyzer-input-text');
    const submitTextBtn = document.getElementById('btn-submit-text');
    const placeholderState = document.getElementById('placeholder-state');
    const resultState = document.getElementById('analytics-result-state');
    const analyzeNewBtn = document.getElementById('btn-analyze-new');

    const fileInput = document.getElementById('csv-file-input');
    const submitFileBtn = document.getElementById('btn-submit-file');
    const dropZone = document.getElementById('drop-zone');
    const dropZoneText = document.getElementById('drop-zone-text');

    // Active User ID for session tracing
    const userId = localStorage.getItem('mentalflow_user_id') || 1;

    // PROTECTION LAYER: When page loads, if there's any previous result in memory, render it
    const savedResult = localStorage.getItem('recent_analysis_result');
    if (savedResult) {
        const cachedData = JSON.parse(savedResult);
        renderOutputHTML(cachedData);
    }

    // Reuseable UI Rendering function
    function renderOutputHTML(data) {
        if (placeholderState) placeholderState.style.setProperty('display', 'none', 'important');
        if (resultState) resultState.style.setProperty('display', 'block', 'important');

        const metricSentiment = document.getElementById('metric-sentiment');
        const metricConfidence = document.getElementById('metric-confidence');
        const metricEmotion = document.getElementById('metric-emotion');
        const metricRisk = document.getElementById('metric-risk');
        const riskShield = document.getElementById('risk-shield');
        const emojiElement = document.getElementById('metric-sentiment-emoji');

        if (metricSentiment) {
            metricSentiment.innerText = data.sentiment;
            metricSentiment.style.color = data.sentiment_color;
        }
        if (metricConfidence) {
            metricConfidence.innerText = data.confidence + "%";
        }
        if (metricEmotion) {
            metricEmotion.innerText = data.emotion;
        }
        if (metricRisk) {
            metricRisk.innerText = data.risk_level;
            metricRisk.style.color = data.risk_color;
        }
        if (riskShield) {
            riskShield.style.color = data.risk_color;
        }

        if (emojiElement) {
            if (data.sentiment === "Positive") emojiElement.innerText = "😊";
            else if (data.sentiment === "Negative") emojiElement.innerText = "😢";
            else emojiElement.innerText = "😐";
        }
    }

    // Function to clear all results safely
    const clearAnalysis = (e) => {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }
        localStorage.removeItem('recent_analysis_result'); // Clear cache string
        textInput.value = '';
        if (document.getElementById('char-count')) {
            document.getElementById('char-count').innerText = '0';
        }
        if (placeholderState) placeholderState.style.display = 'block';
        if (resultState) resultState.style.display = 'none';
        textInput.focus();
    };

    // ==================== 1. Real-Time Text Parser Implementation ====================
    if (submitTextBtn) {
        submitTextBtn.addEventListener('click', async (e) => {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            const textPayload = textInput.value.trim();
            if (textPayload.length < 5) {
                alert("At least 5 characters are required to trigger analysis!");
                return false;
            }

            // Toggle Buttons UI State to Loading
            const spinner = document.getElementById('text-btn-spinner');
            const normalText = document.getElementById('text-btn-normal');
            if (spinner) spinner.style.display = 'inline';
            if (normalText) normalText.style.display = 'none';
            submitTextBtn.disabled = true;

            try {
                const response = await fetch(`${BASE_API_URL}/analyze`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: textPayload, userId: userId })
                });

                const data = await response.json();

                if (response.ok) {
                    // Save response to local state storage before browser triggers reload
                    localStorage.setItem('recent_analysis_result', JSON.stringify(data));
                    renderOutputHTML(data);
                } else {
                    alert(`Error Message: ${data.error}`);
                }
            } catch (error) {
                console.error("Pipeline failure:", error);
                alert("Backend server connection missing status!");
            } finally {
                if (spinner) spinner.style.display = 'none';
                if (normalText) normalText.style.display = 'inline';
                submitTextBtn.disabled = false;
            }

            return false;
        });
    }

    // ==================== 2. Dataset Processing Pipeline ====================
    if (analyzeNewBtn) {
        analyzeNewBtn.addEventListener('click', clearAnalysis);
    }
    
    if (fileInput) {
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0 && dropZoneText) {
                dropZoneText.innerText = `Selected File: ${fileInput.files[0].name}`;
                if (submitFileBtn) submitFileBtn.disabled = false;
                if (dropZone) dropZone.style.background = 'rgba(16, 185, 129, 0.05)';
            }
        });
    }

    if (submitFileBtn) {
        submitFileBtn.addEventListener('click', async (e) => {
            if (e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            const fileObject = fileInput.files[0];
            if (!fileObject) return false;

            const formData = new FormData();
            formData.append('file', fileObject);
            formData.append('userId', userId);

            submitFileBtn.innerText = "Processing Dataset Row-by-Row...";
            submitFileBtn.disabled = true;

            try {
                const response = await fetch(`${BASE_API_URL}/upload`, {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    alert(`Batch processed completely! Total Rows Evaluated: ${data.total}. Moving to Dashboard View.`);
                    window.location.href = "dashboard.html"; 
                } else {
                    alert(`Upload Error: ${data.error}`);
                }
            } catch (error) {
                console.error("Batch failure:", error);
                alert("File formatting checks fail!");
            } finally {
                submitFileBtn.innerHTML = 'Upload & Analyze Dataset <i class="fa-solid fa-chart-line"></i>';
                submitFileBtn.disabled = false;
            }

            return false;
        });
    }
});