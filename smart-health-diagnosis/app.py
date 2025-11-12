from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Medical database
MEDICAL_CONDITIONS = {
    'common_cold': {
        'name': 'Common Cold',
        'symptoms': ['runny_nose', 'sneezing', 'sore_throat', 'cough', 'congestion'],
        'treatment': ['Rest and hydration', 'Over-the-counter cold medication'],
        'severity': 'Mild',
        'icon': '🤧'
    },
    'flu': {
        'name': 'Influenza (Flu)',
        'symptoms': ['fever', 'body_aches', 'fatigue', 'cough', 'headache'],
        'treatment': ['Rest', 'Hydration', 'Antiviral medication if early'],
        'severity': 'Moderate',
        'icon': '🤒'
    },
    'allergies': {
        'name': 'Allergies',
        'symptoms': ['sneezing', 'itchy_eyes', 'runny_nose', 'congestion'],
        'treatment': ['Antihistamines', 'Avoid allergens'],
        'severity': 'Mild',
        'icon': '🌸'
    }
}

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MediScan Pro - Health Diagnosis</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: white;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 40px 20px;
                text-align: center;
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
            }
            p {
                font-size: 1.2rem;
                margin-bottom: 2rem;
                opacity: 0.9;
            }
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
    # Get all symptoms
    all_symptoms = set()
    for condition in MEDICAL_CONDITIONS.values():
        all_symptoms.update(condition['symptoms'])
    symptoms_list = sorted(list(all_symptoms))
    
    symptoms_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Symptom Assessment - MediScan Pro</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: Arial, sans-serif;
                background: #f5f5f5;
                color: #333;
                line-height: 1.6;
                padding: 20px;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #2563eb;
                margin-bottom: 20px;
                text-align: center;
            }
            .symptoms-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 10px;
                margin: 20px 0;
            }
            .symptom {
                padding: 15px;
                border: 2px solid #ddd;
                border-radius: 8px;
                cursor: pointer;
                text-align: center;
                transition: all 0.3s ease;
            }
            .symptom:hover {
                border-color: #2563eb;
                transform: translateY(-2px);
            }
            .symptom.selected {
                background: #e3f2fd;
                border-color: #2196F3;
            }
            .button {
                background: #4CAF50;
                color: white;
                padding: 15px 30px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin: 10px;
                transition: background 0.3s;
            }
            .button:hover {
                background: #45a049;
            }
            .button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            .button.clear {
                background: #ff9800;
            }
            .button.clear:hover {
                background: #e68900;
            }
            #result {
                margin-top: 30px;
                padding: 20px;
                border-radius: 8px;
            }
            .success {
                background: #e8f5e8;
                border-left: 4px solid #4CAF50;
            }
            .error {
                background: #ffebee;
                border-left: 4px solid #f44336;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Select Your Symptoms</h1>
            <p style="text-align: center; margin-bottom: 20px; color: #666;">
                Choose all symptoms you're currently experiencing
            </p>
            
            <div class="symptoms-grid" id="symptomsGrid">
    '''
    
    # Add symptoms to grid
    for symptom in symptoms_list:
        display_name = symptom.replace('_', ' ').title()
        symptoms_html += f'''
                <div class="symptom" onclick="toggleSymptom(this)" data-symptom="{symptom}">
                    {display_name}
                </div>
        '''
    
    symptoms_html += '''
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <button class="button" onclick="diagnose()" id="diagnoseBtn" disabled>
                    Get Diagnosis
                </button>
                <button class="button clear" onclick="clearSelection()">
                    Clear All
                </button>
            </div>
            
            <div id="result"></div>
            
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
                    
                    // Update button state
                    document.getElementById('diagnoseBtn').disabled = selectedSymptoms.length === 0;
                }
                
                function clearSelection() {
                    selectedSymptoms = [];
                    // Remove selected class from all symptoms
                    document.querySelectorAll('.symptom').forEach(item => {
                        item.classList.remove('selected');
                    });
                    // Disable diagnose button
                    document.getElementById('diagnoseBtn').disabled = true;
                    // Clear results
                    document.getElementById('result').innerHTML = '';
                }
                
                async function diagnose() {
                    if (selectedSymptoms.length === 0) {
                        alert('Please select at least one symptom');
                        return;
                    }
                    
                    const btn = document.getElementById('diagnoseBtn');
                    const resultDiv = document.getElementById('result');
                    
                    // Show loading state
                    btn.disabled = true;
                    btn.textContent = 'Analyzing...';
                    resultDiv.innerHTML = '<p>Analyzing your symptoms...</p>';
                    
                    try {
                        const response = await fetch('/diagnose', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                symptoms: selectedSymptoms
                            })
                        });
                        
                        if (!response.ok) {
                            throw new Error('Server responded with error: ' + response.status);
                        }
                        
                        const result = await response.json();
                        
                        // Display results
                        resultDiv.className = 'success';
                        resultDiv.innerHTML = `
                            <h2>Diagnosis Result</h2>
                            <p><strong>Condition:</strong> ${result.condition}</p>
                            <p><strong>Confidence:</strong> ${result.confidence}%</p>
                            <p><strong>Severity:</strong> ${result.severity}</p>
                            <h3>Recommended Treatment:</h3>
                            <ul>
                                ${result.treatment.map(treatment => `<li>${treatment}</li>`).join('')}
                            </ul>
                            ${result.icon ? `<p style="font-size: 2rem; text-align: center; margin-top: 20px;">${result.icon}</p>` : ''}
                        `;
                        
                    } catch (error) {
                        resultDiv.className = 'error';
                        resultDiv.innerHTML = `
                            <h3>Error</h3>
                            <p>${error.message}</p>
                            <p>Please try again or check your connection.</p>
                        `;
                    } finally {
                        // Reset button
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
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
            
        user_symptoms = data.get('symptoms', [])
        
        if not user_symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        print(f"Received symptoms: {user_symptoms}")  # For debugging
        
        # Find best matching condition
        best_match = None
        best_score = 0
        
        for condition_id, condition in MEDICAL_CONDITIONS.items():
            # Calculate match score
            matches = len(set(user_symptoms) & set(condition['symptoms']))
            total_symptoms = len(condition['symptoms'])
            score = (matches / total_symptoms) * 100
            
            if score > best_score:
                best_score = score
                best_match = condition_id
        
        if best_match:
            condition = MEDICAL_CONDITIONS[best_match]
            result = {
                'condition': condition['name'],
                'confidence': round(best_score, 2),
                'treatment': condition['treatment'],
                'severity': condition['severity'],
                'icon': condition['icon'],
                'matched_symptoms': len(set(user_symptoms) & set(condition['symptoms']))
            }
        else:
            result = {
                'condition': 'General Illness',
                'confidence': 50,
                'treatment': [
                    'Rest and hydration',
                    'Monitor symptoms',
                    'Consult healthcare provider if symptoms worsen'
                ],
                'severity': 'Mild',
                'icon': '🤔',
                'matched_symptoms': 0
            }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in diagnosis: {str(e)}")  # For debugging
        return jsonify({'error': f'Diagnosis error: {str(e)}'}), 500

# Add a catch-all route for 404 errors
@app.route('/<path:path>')
def catch_all(path):
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Page Not Found - MediScan Pro</title>
        <style>
            body {{ font-family: Arial; margin: 40px; text-align: center; }}
            .container {{ max-width: 600px; margin: 0 auto; }}
            h1 {{ color: #f44336; }}
            .button {{ background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>404 - Page Not Found</h1>
            <p>The page you're looking for doesn't exist.</p>
            <a href="/" class="button">Return to Home</a>
        </div>
    </body>
    </html>
    ''', 404

# Production configuration
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
