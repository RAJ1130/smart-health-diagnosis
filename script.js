// Medical Database
const MEDICAL_CONDITIONS = {
    'common_cold': {
        name: 'Common Cold (Viral Rhinitis)',
        symptoms: ['runny_nose', 'sneezing', 'sore_throat', 'cough', 'congestion', 'mild_fever', 'headache'],
        key_symptoms: ['runny_nose', 'sneezing', 'congestion'],
        severity: 'Mild',
        icon: '🤧',
        recovery_time: '7-10 days',
        treatment: [
            "NASAL CONGESTION: Oxymetazoline 0.05% nasal spray",
            "RUNNY NOSE: Brompheniramine 4mg every 4-6 hours",
            "SORE THROAT: Warm salt water gargles",
            "COUGH: Dextromethorphan 30mg every 6-8 hours",
            "FEVER: Acetaminophen 650mg every 6 hours",
            "IMMUNE SUPPORT: Zinc gluconate lozenges"
        ]
    },
    'influenza': {
        name: 'Influenza (Seasonal Flu)',
        symptoms: ['fever', 'chills', 'body_aches', 'fatigue', 'cough', 'headache', 'sore_throat'],
        key_symptoms: ['fever', 'body_aches', 'fatigue', 'cough'],
        severity: 'Moderate to Severe',
        icon: '🤒',
        recovery_time: '1-2 weeks',
        treatment: [
            "ANTIVIRAL: Oseltamivir 75mg twice daily × 5 days",
            "FEVER: Acetaminophen + Ibuprofen staggered",
            "ACHES: Naproxen 500mg twice daily",
            "COUGH: Benzonatate 100mg three times daily",
            "HYDRATION: Oral rehydration solution"
        ]
    },
    'migraine': {
        name: 'Migraine Headache',
        symptoms: ['headache', 'nausea', 'sensitivity_light', 'sensitivity_sound', 'throbbing_pain'],
        key_symptoms: ['headache', 'sensitivity_light', 'throbbing_pain', 'nausea'],
        severity: 'Moderate to Severe',
        icon: '😵',
        recovery_time: '4-72 hours',
        treatment: [
            "ACUTE: Sumatriptan 50-100mg at onset",
            "NAUSEA: Metoclopramide 10mg + Ibuprofen 600mg",
            "AURA: Dark quiet room + Cold compress",
            "PREVENTIVE: Propranolol LA 60mg daily"
        ]
    }
};

// All available symptoms
const ALL_SYMPTOMS = [
    'runny_nose', 'sneezing', 'sore_throat', 'cough', 'congestion', 'mild_fever', 'headache',
    'fever', 'chills', 'body_aches', 'fatigue', 'nasal_congestion', 'muscle_pain',
    'nausea', 'sensitivity_light', 'sensitivity_sound', 'throbbing_pain', 'vision_changes'
];

// Emergency symptoms
const EMERGENCY_SYMPTOMS = ['chest_pain', 'difficulty_breathing', 'severe_headache', 'high_fever'];

// User data storage
let userProfile = null;
let selectedSymptoms = new Set();
let diagnosisHistory = JSON.parse(localStorage.getItem('diagnosisHistory')) || [];

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Check which page we're on
    const path = window.location.pathname;
    
    if (path.includes('assessment.html')) {
        initAssessmentPage();
    } else if (path.includes('dashboard.html')) {
        initDashboardPage();
    }
    
    // Load existing profile
    loadUserProfile();
});

// Assessment Page Functions
function initAssessmentPage() {
    loadSymptoms();
    setupEventListeners();
    updateSelectedList();
}

function loadSymptoms() {
    const symptomsGrid = document.getElementById('symptomsGrid');
    if (!symptomsGrid) return;
    
    symptomsGrid.innerHTML = '';
    
    ALL_SYMPTOMS.forEach(symptom => {
        const isEmergency = EMERGENCY_SYMPTOMS.includes(symptom);
        const displayName = symptom.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
        
        const symptomCard = document.createElement('div');
        symptomCard.className = 'symptom-card';
        if (isEmergency) symptomCard.classList.add('emergency');
        symptomCard.innerHTML = `
            ${displayName}
            ${isEmergency ? '<span class="emergency-badge">ER</span>' : ''}
        `;
        
        symptomCard.addEventListener('click', () => toggleSymptom(symptom));
        
        symptomsGrid.appendChild(symptomCard);
    });
}

function setupEventListeners() {
    const searchInput = document.getElementById('symptomSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const symptoms = document.querySelectorAll('.symptom-card');
            symptoms.forEach(symptom => {
                const symptomText = symptom.textContent.toLowerCase();
                symptom.style.display = symptomText.includes(searchTerm) ? 'block' : 'none';
            });
        });
    }
}

function toggleSymptom(symptom) {
    if (selectedSymptoms.has(symptom)) {
        selectedSymptoms.delete(symptom);
    } else {
        selectedSymptoms.add(symptom);
    }
    updateSelectedList();
}

function updateSelectedList() {
    const selectedList = document.getElementById('selectedList');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    if (selectedList) {
        if (selectedSymptoms.size === 0) {
            selectedList.innerHTML = 'No symptoms selected yet';
        } else {
            let html = '';
            Array.from(selectedSymptoms).forEach(symptom => {
                const displayName = symptom.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase());
                const isEmergency = EMERGENCY_SYMPTOMS.includes(symptom);
                html += `<div class="selected-item ${isEmergency ? 'emergency' : ''}">
                    <span>${displayName}</span>
                    <button onclick="removeSymptom('${symptom}')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>`;
            });
            selectedList.innerHTML = html;
        }
    }
    
    if (analyzeBtn) {
        analyzeBtn.disabled = selectedSymptoms.size === 0;
    }
}

function removeSymptom(symptom) {
    selectedSymptoms.delete(symptom);
    updateSelectedList();
}

// Profile Functions
function saveProfile() {
    const age = document.getElementById('userAge').value;
    const gender = document.getElementById('userGender').value;
    const conditions = Array.from(document.querySelectorAll('input[name="conditions"]:checked'))
        .map(cb => cb.value);
    
    userProfile = {
        age: parseInt(age),
        gender,
        conditions,
        created: new Date().toISOString()
    };
    
    localStorage.setItem('userProfile', JSON.stringify(userProfile));
    
    // Show symptom section
    document.getElementById('userProfileSection').style.display = 'none';
    document.getElementById('symptomSection').style.display = 'block';
    
    alert('Profile saved successfully!');
}

function loadUserProfile() {
    const saved = localStorage.getItem('userProfile');
    if (saved) {
        userProfile = JSON.parse(saved);
    }
}

// Diagnosis Functions
function analyzeSymptoms() {
    const symptomsArray = Array.from(selectedSymptoms);
    
    // Check for emergency
    const emergencySymptoms = symptomsArray.filter(s => EMERGENCY_SYMPTOMS.includes(s));
    if (emergencySymptoms.length > 0) {
        showEmergencyAlert(emergencySymptoms);
        return;
    }
    
    // Find best matching condition
    let bestMatch = null;
    let bestScore = 0;
    
    for (const [conditionId, condition] of Object.entries(MEDICAL_CONDITIONS)) {
        const keyMatches = symptomsArray.filter(s => condition.key_symptoms.includes(s)).length;
        const totalMatches = symptomsArray.filter(s => condition.symptoms.includes(s)).length;
        
        if (totalMatches === 0) continue;
        
        const score = (keyMatches * 2) + totalMatches;
        
        if (score > bestScore) {
            bestScore = score;
            bestMatch = conditionId;
        }
    }
    
    if (bestMatch) {
        const condition = MEDICAL_CONDITIONS[bestMatch];
        showDiagnosisResult(condition);
        saveToHistory(condition, symptomsArray);
    } else {
        showGeneralAdvice(symptomsArray);
    }
}

function showEmergencyAlert(symptoms) {
    const resultCard = document.getElementById('resultCard');
    if (!resultCard) return;
    
    const symptomList = symptoms.map(s => 
        s.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase())
    ).join(', ');
    
    resultCard.innerHTML = `
        <div class="emergency-alert">
            <h3><i class="fas fa-ambulance"></i> EMERGENCY ATTENTION REQUIRED</h3>
            <p>Your symptoms (${symptomList}) indicate a potential medical emergency.</p>
            <div class="emergency-instructions">
                <p><strong>Immediate Actions:</strong></p>
                <ul>
                    <li>Call emergency services (911 or local emergency number)</li>
                    <li>Do not drive yourself to the hospital</li>
                    <li>Stay calm and provide clear information to responders</li>
                    <li>Have someone stay with you until help arrives</li>
                </ul>
            </div>
        </div>
    `;
    
    document.getElementById('symptomSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
}

function showDiagnosisResult(condition) {
    const resultCard = document.getElementById('resultCard');
    if (!resultCard) return;
    
    const riskFactors = userProfile ? 
        `Based on your profile (Age: ${userProfile.age}, Gender: ${userProfile.gender})` : 
        'Based on reported symptoms';
    
    resultCard.innerHTML = `
        <div class="diagnosis-result">
            <div class="condition-header">
                <div class="condition-icon">${condition.icon}</div>
                <div class="condition-info">
                    <h3>${condition.name}</h3>
                    <div class="condition-details">
                        <span class="severity-badge">${condition.severity}</span>
                        <span class="recovery-time">${condition.recovery_time}</span>
                    </div>
                </div>
            </div>
            
            <div class="risk-factors">
                <p><i class="fas fa-info-circle"></i> ${riskFactors}</p>
            </div>
            
            <div class="treatment-plan">
                <h4><i class="fas fa-prescription-bottle-medical"></i> Recommended Treatment</h4>
                <ul>
                    ${condition.treatment.map(item => `<li>${item}</li>`).join('')}
                </ul>
            </div>
            
            <div class="disclaimer">
                <p><strong>Important:</strong> This is AI-generated information. Always consult a healthcare professional for medical diagnosis and treatment.</p>
            </div>
        </div>
    `;
    
    document.getElementById('symptomSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
}

function showGeneralAdvice(symptoms) {
    const resultCard = document.getElementById('resultCard');
    if (!resultCard) return;
    
    resultCard.innerHTML = `
        <div class="general-advice">
            <h3><i class="fas fa-stethoscope"></i> General Medical Advice</h3>
            <p>Our AI couldn't find a specific match for your symptoms. Please consult a healthcare provider for proper evaluation.</p>
            
            <div class="recommendations">
                <h4>General Recommendations:</h4>
                <ul>
                    <li>Rest and adequate hydration (8-10 glasses water daily)</li>
                    <li>Monitor symptoms closely for changes</li>
                    <li>Acetaminophen or Ibuprofen for pain/fever as needed</li>
                    <li>Consult healthcare provider within 24-48 hours</li>
                </ul>
            </div>
        </div>
    `;
    
    document.getElementById('symptomSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
}

function saveToHistory(condition, symptoms) {
    const diagnosis = {
        id: Date.now(),
        date: new Date().toISOString(),
        condition: condition.name,
        symptoms: symptoms,
        severity: condition.severity,
        treatment: condition.treatment
    };
    
    diagnosisHistory.unshift(diagnosis);
    if (diagnosisHistory.length > 10) diagnosisHistory = diagnosisHistory.slice(0, 10);
    
    localStorage.setItem('diagnosisHistory', JSON.stringify(diagnosisHistory));
}

function startNewAssessment() {
    selectedSymptoms.clear();
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('symptomSection').style.display = 'block';
    updateSelectedList();
}

// Dashboard Functions
function initDashboardPage() {
    loadDashboardStats();
    loadDiagnosisHistory();
}

function loadDashboardStats() {
    const statsContainer = document.getElementById('dashboardStats');
    if (!statsContainer) return;
    
    const totalDiagnoses = diagnosisHistory.length;
    const uniqueConditions = [...new Set(diagnosisHistory.map(d => d.condition))].length;
    const recentDiagnosis = diagnosisHistory[0];
    
    statsContainer.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">${totalDiagnoses}</div>
                <div>Total Diagnoses</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${uniqueConditions}</div>
                <div>Unique Conditions</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">${userProfile ? userProfile.age : '--'}</div>
                <div>Your Age</div>
            </div>
        </div>
    `;
}

function loadDiagnosisHistory() {
    const historyContainer = document.getElementById('diagnosisHistory');
    if (!historyContainer) return;
    
    if (diagnosisHistory.length === 0) {
        historyContainer.innerHTML = '<p class="no-history">No diagnosis history yet.</p>';
        return;
    }
    
    let html = '';
    diagnosisHistory.forEach(diagnosis => {
        const date = new Date(diagnosis.date).toLocaleDateString();
        const symptoms = diagnosis.symptoms
            .map(s => s.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase()))
            .join(', ');
        
        html += `
            <div class="history-item">
                <div class="history-header">
                    <h4>${diagnosis.condition}</h4>
                    <span class="history-date">${date}</span>
                </div>
                <div class="history-details">
                    <p><strong>Symptoms:</strong> ${symptoms}</p>
                    <p><strong>Severity:</strong> ${diagnosis.severity}</p>
                </div>
            </div>
        `;
    });
    
    historyContainer.innerHTML = html;
}

function clearHistory() {
    if (confirm('Are you sure you want to clear all diagnosis history?')) {
        diagnosisHistory = [];
        localStorage.removeItem('diagnosisHistory');
        loadDashboardStats();
        loadDiagnosisHistory();
    }
}
