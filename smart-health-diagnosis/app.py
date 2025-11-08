from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

# Comprehensive medical database
MEDICAL_CONDITIONS = {
    'common_cold': {
        'name': 'Common Cold (Viral Rhinitis)',
        'symptoms': ['runny_nose', 'sneezing', 'sore_throat', 'cough', 'congestion', 'mild_fever', 'headache', 'body_aches', 'fatigue'],
        'key_symptoms': ['runny_nose', 'sneezing', 'congestion'],
        'treatment': [
            'Rest and increased fluid intake (8-10 glasses water daily)',
            'Saline nasal spray 2-3 times daily for congestion',
            'Acetaminophen 500-1000mg every 6 hours as needed for pain/fever',
            'Ibuprofen 200-400mg every 6-8 hours for inflammation',
            'Warm salt water gargles (1/2 tsp salt in 8oz warm water) 3-4 times daily',
            'Use humidifier in bedroom at night'
        ],
        'severity': 'Mild',
        'icon': '🤧'
    },
    'flu': {
        'name': 'Influenza (Flu)',
        'symptoms': ['fever', 'chills', 'body_aches', 'fatigue', 'cough', 'headache', 'sore_throat', 'nasal_congestion', 'muscle_pain', 'weakness'],
        'key_symptoms': ['fever', 'body_aches', 'fatigue'],
        'treatment': [
            'Bed rest and strict hydration (electrolyte solutions if dehydrated)',
            'Acetaminophen 650mg every 6 hours for fever and myalgia',
            'Ibuprofen 400-600mg every 6-8 hours for inflammation',
            'Dextromethorphan 15-30mg every 6-8 hours for cough',
            'Monitor for complications: pneumonia, bronchitis',
            'Isolate to prevent spread (contagious for 5-7 days after symptoms)'
        ],
        'severity': 'Moderate to Severe',
        'icon': '🤒'
    },
    'allergies': {
        'name': 'Allergic Rhinitis (Hay Fever)',
        'symptoms': ['sneezing', 'itchy_eyes', 'runny_nose', 'nasal_itching', 'watery_eyes', 'congestion', 'postnasal_drip', 'itchy_throat'],
        'key_symptoms': ['sneezing', 'itchy_eyes', 'nasal_itching'],
        'treatment': [
            'Cetirizine 10mg daily or Loratadine 10mg daily (non-drowsy antihistamines)',
            'Fluticasone nasal spray 1-2 sprays per nostril daily',
            'Saline nasal irrigation twice daily with neti pot',
            'Avoid known allergens: pollen, dust mites, pet dander',
            'Use HEPA air filters in living spaces'
        ],
        'severity': 'Mild to Moderate',
        'icon': '🌸'
    },
    'migraine': {
        'name': 'Migraine Headache',
        'symptoms': ['headache', 'nausea', 'sensitivity_light', 'sensitivity_sound', 'throbbing_pain', 'vision_changes', 'dizziness'],
        'key_symptoms': ['headache', 'sensitivity_light', 'throbbing_pain'],
        'treatment': [
            'Rest in dark, quiet room immediately when symptoms begin',
            'Ibuprofen 600mg or Naproxen 500mg for mild episodes',
            'Cold compress to forehead and back of neck',
            'Hydration with electrolyte solutions',
            'Identify and avoid triggers: stress, certain foods, hormonal changes'
        ],
        'severity': 'Moderate to Severe',
        'icon': '😵'
    }
}

EMERGENCY_SYMPTOMS = ['chest_pain', 'difficulty_breathing', 'severe_bleeding', 'loss_consciousness']

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MediScan Pro - Health Diagnosis</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh; color: white; line-height: 1.6;
                padding: 20px;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                text-align: center;
                padding: 40px 20px;
            }
            h1 { 
                font-size: 3rem; 
                margin-bottom: 1rem;
                background: linear-gradient(45deg, #fff, #e0f2fe);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            p { font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9; }
            .cta-button {
                display: inline-block;
                background: linear-gradient(45deg, #2563eb, #8b5cf6);
                color: white;
                padding: 15px 30px;
                border-radius: 50px;
                text-decoration: none;
                font-weight: bold;
                font-size: 1.1rem;
                transition: transform 0.3s;
                margin-top: 20px;
            }
            .cta-button:hover {
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 MediScan Pro</h1>
            <p>AI-powered health diagnosis with comprehensive symptom analysis</p>
            <a href="/symptoms" class="cta-button">Start Health Assessment</a>
        </div>
    </body>
    </html>
    '''

@app.route('/symptoms')
def symptoms():
    all_symptoms = set()
    for condition in MEDICAL_CONDITIONS.values():
        all_symptoms.update(condition['symptoms'])
    symptoms_list = sorted(list(all_symptoms))
    
    symptoms_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Symptom Assessment</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f5f5f5; }
            .container { max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .symptoms-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 20px 0; }
            .symptom { padding: 15px; border: 2px solid #ddd; border-radius: 8px; cursor: pointer; text-align: center; }
            .symptom.selected { background: #e3f2fd; border-color: #2196F3; }
            .symptom.emergency { border-color: #f44336; background: #ffebee; }
            .button { background: #4CAF50; color: white; padding: 15px 30px; border: none; border-radius: 5px; cursor: pointer; margin: 10px; }
            .button:disabled { background: #ccc; cursor: not-allowed; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Select Your Symptoms</h1>
            <div class="symptoms-grid" id="symptomsGrid">
    '''
    
    for symptom in symptoms_list:
        is_emergency = symptom in EMERGENCY_SYMPTOMS
        display_name = symptom.replace('_', ' ').title()
        symptom_class = "symptom"
        if is_emergency:
            symptom_class += " emergency"
        
        symptoms_html += f'<div class="{symptom_class}" onclick="toggleSymptom(this)" data-symptom="{symptom}">{display_name}</div>'
    
    symptoms_html += '''
            </div>
            <button class="button" onclick="diagnose()" id="diagnoseBtn" disabled>Get Diagnosis</button>
            <button class="button" onclick="clearSelection()" style="background: #ff9800;">Clear All</button>
            <div id="result" style="margin-top: 30px;"></div>
            
            <script>
                let selectedSymptoms = [];
                
                function toggleSymptom(element) {
                    const symptom = element.getAttribute('data-symptom');
                    const index = selectedSymptoms.indexOf(symptom);
                    
                    if (index === -1) {
                        selectedSymptoms.push(symptom);
                        element.classList.add('selected');
                    } else {
                        selectedSymptoms.splice(index, 1);
                        element.classList.remove('selected');
                    }
                    
                    document.getElementById('diagnoseBtn').disabled = selectedSymptoms.length === 0;
                }
                
                function clearSelection() {
                    selectedSymptoms = [];
                    document.querySelectorAll('.symptom').forEach(item => {
                        item.classList.remove('selected');
                    });
                    document.getElementById('diagnoseBtn').disabled = true;
                    document.getElementById('result').innerHTML = '';
                }
                
                async function diagnose() {
                    if (selectedSymptoms.length === 0) return;
                    
                    const btn = document.getElementById('diagnoseBtn');
                    btn.disabled = true;
                    btn.textContent = 'Analyzing...';
                    
                    try {
                        const response = await fetch('/diagnose', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ symptoms: selectedSymptoms })
                        });
                        
                        if (!response.ok) {
                            throw new Error('Server error: ' + response.status);
                        }
                        
                        const result = await response.json();
                        
                        document.getElementById('result').innerHTML = `
                            <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; border-left: 4px solid #4CAF50;">
                                <h2>Diagnosis Result</h2>
                                <p><strong>Condition:</strong> ${result.condition}</p>
                                <p><strong>Confidence:</strong> ${result.confidence}%</p>
                                <p><strong>Severity:</strong> ${result.severity}</p>
                                <h3>Recommendations:</h3>
                                <ul>
                                    ${result.treatment.map(t => `<li>${t}</li>`).join('')}
                                </ul>
                            </div>
                        `;
                    } catch (error) {
                        document.getElementById('result').innerHTML = `
                            <div style="background: #ffebee; padding: 20px; border-radius: 8px; border-left: 4px solid #f44336;">
                                <h3>Error</h3>
                                <p>${error.message}</p>
                            </div>
                        `;
                    } finally {
                        btn.disabled = false;
                        btn.textContent = 'Get Diagnosis';
                    }
                }
            </script>
        </div>
    </body>
    </html>
    '''
    
    return symptoms_html

@app.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        user_symptoms = data.get('symptoms', [])
        
        if not user_symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Check for emergency symptoms
        emergency_symptoms = [s for s in user_symptoms if s in EMERGENCY_SYMPTOMS]
        if emergency_symptoms:
            return jsonify({
                'condition': '🚨 EMERGENCY - Immediate Medical Attention Required',
                'severity': 'Critical',
                'confidence': 100,
                'treatment': [
                    'Seek immediate medical attention',
                    'Call emergency services or visit nearest ER',
                    'Do not delay care for these symptoms'
                ],
                'matched_symptoms': len(emergency_symptoms),
                'icon': '🚑'
            })
        
        # Find best matching condition
        best_match = None
        best_score = 0
        
        for condition_id, condition in MEDICAL_CONDITIONS.items():
            key_matches = len(set(user_symptoms) & set(condition['key_symptoms']))
            total_matches = len(set(user_symptoms) & set(condition['symptoms']))
            total_possible = len(condition['symptoms'])
            
            base_score = (total_matches / total_possible) * 70
            key_bonus = (key_matches / len(condition['key_symptoms'])) * 30
            final_score = base_score + key_bonus
            
            if final_score > best_score:
                best_score = final_score
                best_match = condition_id
        
        if best_match and best_score >= 40:
            condition = MEDICAL_CONDITIONS[best_match]
            return jsonify({
                'condition': condition['name'],
                'severity': condition['severity'],
                'confidence': round(best_score, 2),
                'treatment': condition['treatment'],
                'matched_symptoms': len(set(user_symptoms) & set(condition['symptoms'])),
                'icon': condition['icon']
            })
        else:
            return jsonify({
                'condition': 'General Medical Condition',
                'severity': 'Mild to Moderate',
                'confidence': 60,
                'treatment': [
                    'Rest and adequate hydration',
                    'Over-the-counter symptom relief as needed',
                    'Monitor for worsening symptoms',
                    'Consult healthcare provider if no improvement in 48-72 hours'
                ],
                'matched_symptoms': len(user_symptoms),
                'icon': '🤔'
            })
            
    except Exception as e:
        return jsonify({'error': f'Diagnosis error: {str(e)}'}), 500

# Production configuration
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
