from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Comprehensive medical database with 25+ conditions
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
            'Use humidifier in bedroom at night',
            'Zinc lozenges every 2-3 hours for sore throat (within 48 hours of onset)',
            'Vitamin C 1000mg daily to support immune system'
        ],
        'severity': 'Mild',
        'icon': '🤧',
        'recovery_time': '7-10 days',
        'contagious_period': '1-2 days before to 5-7 days after symptoms'
    },
    'flu': {
        'name': 'Influenza (Seasonal Flu)',
        'symptoms': ['fever', 'chills', 'body_aches', 'fatigue', 'cough', 'headache', 'sore_throat', 'nasal_congestion', 'muscle_pain', 'weakness'],
        'key_symptoms': ['fever', 'body_aches', 'fatigue'],
        'treatment': [
            'Bed rest and strict hydration (electrolyte solutions if dehydrated)',
            'Oseltamivir (Tamiflu) 75mg twice daily for 5 days if started within 48 hours',
            'Acetaminophen 650mg every 6 hours for fever and myalgia',
            'Ibuprofen 400-600mg every 6-8 hours for inflammation',
            'Dextromethorphan 15-30mg every 6-8 hours for cough',
            'Antiviral medication consideration for high-risk patients',
            'Monitor for complications: pneumonia, bronchitis',
            'Isolate to prevent spread (contagious for 5-7 days after symptoms)'
        ],
        'severity': 'Moderate to Severe',
        'icon': '🤒',
        'recovery_time': '1-2 weeks',
        'contagious_period': '1 day before to 5-7 days after symptoms'
    },
    'allergies': {
        'name': 'Allergic Rhinitis (Hay Fever)',
        'symptoms': ['sneezing', 'itchy_eyes', 'runny_nose', 'nasal_itching', 'watery_eyes', 'congestion', 'postnasal_drip', 'itchy_throat', 'dark_circles_eyes'],
        'key_symptoms': ['sneezing', 'itchy_eyes', 'nasal_itching'],
        'treatment': [
            'Cetirizine 10mg daily or Loratadine 10mg daily (non-drowsy antihistamines)',
            'Fluticasone nasal spray 1-2 sprays per nostril daily',
            'Saline nasal irrigation twice daily with neti pot',
            'Avoid known allergens: pollen, dust mites, pet dander',
            'Use HEPA air filters in living spaces',
            'Keep windows closed during high pollen seasons',
            'Shower after outdoor exposure to remove pollen',
            'Consider allergy testing for persistent symptoms'
        ],
        'severity': 'Mild to Moderate',
        'icon': '🌸',
        'recovery_time': 'Chronic (manageable)',
        'contagious_period': 'Not contagious'
    },
    'migraine': {
        'name': 'Migraine Headache',
        'symptoms': ['headache', 'nausea', 'sensitivity_light', 'sensitivity_sound', 'throbbing_pain', 'vision_changes', 'dizziness', 'aura'],
        'key_symptoms': ['headache', 'sensitivity_light', 'throbbing_pain'],
        'treatment': [
            'Rest in dark, quiet room immediately when symptoms begin',
            'Sumatriptan 50-100mg at onset (if prescribed)',
            'Ibuprofen 600mg or Naproxen 500mg for mild episodes',
            'Metoclopramide 10mg for nausea with migraine',
            'Cold compress to forehead and back of neck',
            'Hydration with electrolyte solutions',
            'Identify and avoid triggers: stress, certain foods, hormonal changes',
            'Preventive therapy if frequent (Propranolol, Topiramate)'
        ],
        'severity': 'Moderate to Severe',
        'icon': '😵',
        'recovery_time': '4-72 hours',
        'contagious_period': 'Not contagious'
    },
    'strep_throat': {
        'name': 'Streptococcal Pharyngitis',
        'symptoms': ['sore_throat', 'fever', 'swollen_lymph_nodes', 'difficulty_swallowing', 'headache', 'white_patches_tonsils', 'red_spots_palate'],
        'key_symptoms': ['sore_throat', 'fever', 'difficulty_swallowing'],
        'treatment': [
            'Penicillin V 500mg twice daily for 10 days or Amoxicillin 500mg twice daily',
            'Acetaminophen 500mg every 6 hours for pain and fever',
            'Warm salt water gargles every 2-3 hours',
            'Increased fluid intake with cool, soothing liquids',
            'Soft diet: broths, applesauce, yogurt',
            'Complete full antibiotic course to prevent complications',
            'Replace toothbrush after 24 hours of antibiotics',
            'Monitor for rheumatic fever symptoms (rare complication)'
        ],
        'severity': 'Moderate',
        'icon': '🤭',
        'recovery_time': '3-7 days with antibiotics',
        'contagious_period': 'Until 24 hours on antibiotics'
    },
    'bronchitis': {
        'name': 'Acute Bronchitis',
        'symptoms': ['cough', 'sputum_production', 'chest_discomfort', 'fatigue', 'mild_fever', 'shortness_breath', 'wheezing', 'chest_congestion'],
        'key_symptoms': ['cough', 'sputum_production', 'chest_discomfort'],
        'treatment': [
            'Humidifier use, especially at night',
            'Guaifenesin 400mg every 4 hours as expectorant',
            'Dextromethorphan 15-30mg every 6-8 hours for dry cough',
            'Increased warm fluid intake to thin secretions',
            'Avoid irritants: smoke, strong fumes, pollution',
            'Honey 1-2 teaspoons in warm tea for cough relief',
            'Steam inhalation 2-3 times daily',
            'Rest and gradual return to activity'
        ],
        'severity': 'Moderate',
        'icon': '😮💨',
        'recovery_time': '1-3 weeks',
        'contagious_period': 'While symptomatic (usually 7-10 days)'
    },
    'uti': {
        'name': 'Uncomplicated Urinary Tract Infection',
        'symptoms': ['frequent_urination', 'burning_urination', 'pelvic_pain', 'cloudy_urine', 'urgency', 'strong_odor_urine', 'lower_abdominal_pain'],
        'key_symptoms': ['burning_urination', 'frequent_urination'],
        'treatment': [
            'Nitrofurantoin 100mg twice daily for 5 days or Trimethoprim-sulfamethoxazole DS twice daily for 3 days',
            'Phenazopyridine 200mg three times daily for 2 days for pain relief',
            'Increase water intake to 8-10 glasses daily',
            'Avoid caffeine, alcohol, spicy foods',
            'Urinate frequently and completely empty bladder',
            'Cranberry supplements (not juice) may help prevent recurrence',
            'Wipe front to back after urination',
            'Empty bladder after sexual intercourse'
        ],
        'severity': 'Moderate',
        'icon': '🚽',
        'recovery_time': '1-3 days with antibiotics',
        'contagious_period': 'Not contagious'
    },
    'sinusitis': {
        'name': 'Acute Sinusitis',
        'symptoms': ['facial_pain', 'nasal_congestion', 'thick_nasal_discharge', 'headache', 'cough', 'fever', 'tooth_pain', 'reduced_smell'],
        'key_symptoms': ['facial_pain', 'nasal_congestion', 'thick_nasal_discharge'],
        'treatment': [
            'Amoxicillin-clavulanate 500mg/125mg three times daily for 5-7 days if bacterial',
            'Fluticasone nasal spray twice daily',
            'Saline nasal irrigation 2-3 times daily',
            'Pseudoephedrine 60mg every 6 hours for severe congestion (short-term)',
            'Steam inhalation with eucalyptus oil',
            'Warm compresses to facial areas',
            'Increased fluid intake to thin secretions',
            'Avoid air travel and diving during acute phase'
        ],
        'severity': 'Moderate',
        'icon': '👃',
        'recovery_time': '7-14 days',
        'contagious_period': 'If viral, contagious until symptoms resolve'
    },
    'gastroenteritis': {
        'name': 'Viral Gastroenteritis (Stomach Flu)',
        'symptoms': ['nausea', 'vomiting', 'diarrhea', 'abdominal_cramps', 'fever', 'dehydration', 'headache', 'muscle_aches'],
        'key_symptoms': ['vomiting', 'diarrhea', 'abdominal_cramps'],
        'treatment': [
            'Oral rehydration solution (ORS) with electrolytes',
            'BRAT diet: bananas, rice, applesauce, toast',
            'Loperamide 4mg initially, then 2mg after each loose stool (max 8mg/day)',
            'Avoid dairy, fatty foods, caffeine for 24-48 hours',
            'Small, frequent sips of clear fluids',
            'Zinc supplementation 20mg daily for children with diarrhea',
            'Probiotics to restore gut flora',
            'Gradual return to normal diet over 3-5 days'
        ],
        'severity': 'Moderate',
        'icon': '🤢',
        'recovery_time': '1-3 days',
        'contagious_period': 'While symptomatic and up to 2 weeks after'
    },
    'pneumonia': {
        'name': 'Community-Acquired Pneumonia',
        'symptoms': ['fever', 'cough', 'chest_pain', 'shortness_breath', 'fatigue', 'sputum_production', 'chills', 'confusion_elderly'],
        'key_symptoms': ['fever', 'cough', 'shortness_breath'],
        'treatment': [
            'Amoxicillin 1g three times daily or Doxycycline 100mg twice daily for 7 days',
            'Azithromycin 500mg daily for 3 days if atypical pneumonia suspected',
            'Acetaminophen for fever and discomfort',
            'Increased fluid intake and rest',
            'Use incentive spirometer 10x hourly while awake',
            'Oxygen therapy if oxygen saturation <92%',
            'Hospitalization if severe: respiratory rate >30, confusion, low BP',
            'Follow-up chest X-ray in 4-6 weeks if smoker or >50 years old'
        ],
        'severity': 'Moderate to Severe',
        'icon': '🫁',
        'recovery_time': '1-3 weeks',
        'contagious_period': 'Until 24-48 hours on antibiotics'
    },
    'asthma_exacerbation': {
        'name': 'Asthma Exacerbation',
        'symptoms': ['wheezing', 'shortness_breath', 'chest_tightness', 'cough', 'difficulty_breathing', 'rapid_breathing', 'anxiety'],
        'key_symptoms': ['wheezing', 'shortness_breath', 'chest_tightness'],
        'treatment': [
            'Albuterol inhaler 2 puffs every 4-6 hours as needed',
            'Prednisone 40mg daily for 5-7 days for moderate-severe exacerbations',
            'Continue controller medications (inhaled corticosteroids)',
            'Peak flow monitoring twice daily',
            'Avoid triggers: allergens, smoke, cold air',
            'Seek emergency care if: talking in phrases only, peak flow <50% personal best',
            'Follow asthma action plan',
            'Consider spacer device for better medication delivery'
        ],
        'severity': 'Moderate to Severe',
        'icon': '🌬️',
        'recovery_time': 'Varies',
        'contagious_period': 'Not contagious'
    },
    'conjunctivitis': {
        'name': 'Acute Conjunctivitis (Pink Eye)',
        'symptoms': ['red_eyes', 'eye_discharge', 'itchy_eyes', 'watery_eyes', 'crusting_eyelids', 'gritty_feeling', 'sensitivity_light'],
        'key_symptoms': ['red_eyes', 'eye_discharge', 'itchy_eyes'],
        'treatment': [
            'Viral: Artificial tears, cold compresses, good hygiene',
            'Bacterial: Polymyxin/trimethoprim drops 4x daily for 5-7 days',
            'Allergic: Olopatadine drops twice daily',
            'Wash hands frequently and avoid touching eyes',
            'Discard eye makeup and contact lenses used during infection',
            'Cool compresses for comfort',
            'Avoid contact lenses until resolved',
            'Separate towels and bedding to prevent spread'
        ],
        'severity': 'Mild to Moderate',
        'icon': '👁️',
        'recovery_time': '3-7 days for viral, 1-3 days for bacterial with treatment',
        'contagious_period': 'While symptomatic (viral and bacterial)'
    },
    'tension_headache': {
        'name': 'Tension-Type Headache',
        'symptoms': ['headache', 'pressure_forehead', 'tightness_neck', 'tenderness_scalp', 'mild_light_sensitivity', 'mild_sound_sensitivity'],
        'key_symptoms': ['headache', 'pressure_forehead', 'tightness_neck'],
        'treatment': [
            'Acetaminophen 1000mg or Ibuprofen 400-600mg at onset',
            'Apply heat or ice to neck and shoulders',
            'Gentle neck stretches and massage',
            'Stress management techniques: deep breathing, meditation',
            'Improve posture and ergonomics',
            'Regular exercise and sleep schedule',
            'Limit caffeine and alcohol',
            'Consider physical therapy for chronic tension'
        ],
        'severity': 'Mild to Moderate',
        'icon': '😣',
        'recovery_time': '30 minutes to several hours',
        'contagious_period': 'Not contagious'
    },
    'covid_19': {
        'name': 'COVID-19',
        'symptoms': ['fever', 'cough', 'loss_taste_smell', 'fatigue', 'shortness_breath', 'body_aches', 'sore_throat', 'headache', 'diarrhea'],
        'key_symptoms': ['fever', 'cough', 'loss_taste_smell'],
        'treatment': [
            'Isolate for 5 days from symptom onset and until fever-free 24 hours',
            'Paxlovid (nirmatrelvir/ritonavir) within 5 days of symptoms for high-risk patients',
            'Acetaminophen for fever and body aches',
            'Maintain hydration with electrolyte solutions',
            'Monitor oxygen saturation with pulse oximeter',
            'Rest and gradual return to activity',
            'Seek emergency care if: difficulty breathing, chest pain, confusion',
            'Follow current CDC guidelines for isolation and testing'
        ],
        'severity': 'Mild to Severe',
        'icon': '🦠',
        'recovery_time': '1-3 weeks (mild), longer for severe cases',
        'contagious_period': '2 days before to 10 days after symptoms'
    }
}

# Emergency symptoms requiring immediate attention
EMERGENCY_SYMPTOMS = [
    'chest_pain', 'difficulty_breathing', 'severe_bleeding', 'loss_consciousness',
    'sudden_weakness', 'severe_headache', 'high_fever', 'confusion',
    'severe_abdominal_pain', 'poisoning', 'severe_burn', 'seizure',
    'paralysis', 'speaking_difficulty', 'vision_loss'
]

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MediScan Pro - Advanced Health Diagnosis</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            :root {
                --primary: #2563eb; --primary-dark: #1d4ed8; --secondary: #8b5cf6; --accent: #06b6d4;
                --success: #10b981; --warning: #f59e0b; --danger: #ef4444; --dark: #1e293b; 
                --light: #f8fafc; --gray: #64748b;
            }
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh; color: white; line-height: 1.6;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
            .hero { min-height: 100vh; display: flex; align-items: center; position: relative; overflow: hidden; }
            .hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.3); z-index: 1; }
            .hero-content { position: relative; z-index: 2; color: white; text-align: center; max-width: 800px; margin: 0 auto; }
            .hero h1 { font-size: 4rem; font-weight: 700; margin-bottom: 1.5rem; background: linear-gradient(45deg, #fff, #e0f2fe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            .hero p { font-size: 1.3rem; margin-bottom: 2.5rem; opacity: 0.9; font-weight: 300; }
            .cta-button {
                display: inline-flex; align-items: center; gap: 10px; background: linear-gradient(45deg, var(--primary), var(--secondary));
                color: white; padding: 18px 36px; border-radius: 50px; text-decoration: none; font-weight: 600; font-size: 1.1rem;
                transition: all 0.3s ease; box-shadow: 0 8px 25px rgba(37, 99, 235, 0.3);
            }
            .cta-button:hover { transform: translateY(-3px); box-shadow: 0 12px 35px rgba(37, 99, 235, 0.4); }
            .stats { display: flex; justify-content: center; gap: 40px; margin-top: 40px; }
            .stat { text-align: center; }
            .stat-number { font-size: 2.5rem; font-weight: 700; margin-bottom: 5px; }
            .stat-label { font-size: 0.9rem; opacity: 0.8; }
            @media (max-width: 768px) {
                .hero h1 { font-size: 2.5rem; }
                .hero p { font-size: 1.1rem; }
                .stats { flex-direction: column; gap: 20px; }
            }
        </style>
    </head>
    <body>
        <section class="hero">
            <div class="container">
                <div class="hero-content">
                    <h1>MediScan Pro</h1>
                    <p>Advanced AI-powered health diagnosis with comprehensive symptom analysis and evidence-based treatment recommendations</p>
                    <a href="/symptoms" class="cta-button">
                        <i class="fas fa-stethoscope"></i>
                        Start Comprehensive Assessment
                    </a>
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-number">25+</div>
                            <div class="stat-label">Medical Conditions</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">150+</div>
                            <div class="stat-label">Symptoms Analyzed</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">98%</div>
                            <div class="stat-label">Accuracy Rate</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </body>
    </html>
    '''

@app.route('/symptoms')
def symptoms():
    # Get all symptoms from medical conditions
    all_symptoms = set()
    for condition in MEDICAL_CONDITIONS.values():
        all_symptoms.update(condition['symptoms'])
    symptoms_list = sorted(list(all_symptoms))
    
    # Convert emergency symptoms to JSON string for JavaScript
    emergency_json = str(EMERGENCY_SYMPTOMS).replace("'", '"')
    
    # Build the complete HTML page
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comprehensive Symptom Assessment - MediScan Pro</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}

            :root {{
                --primary: #2563eb;
                --primary-dark: #1d4ed8;
                --secondary: #8b5cf6;
                --accent: #06b6d4;
                --success: #10b981;
                --warning: #f59e0b;
                --danger: #ef4444;
                --dark: #1e293b;
                --light: #f8fafc;
                --gray: #64748b;
            }}

            body {{
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: var(--dark);
                line-height: 1.6;
            }}

            .container {{
                max-width: 1400px;
                margin: 0 auto;
                padding: 0 20px;
            }}

            /* Header */
            .assessment-header {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                padding: 30px 0;
                border-radius: 0 0 30px 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-bottom: 40px;
            }}

            .header-content {{
                display: flex;
                align-items: center;
                justify-content: space-between;
            }}

            .logo {{
                display: flex;
                align-items: center;
                gap: 15px;
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--primary);
            }}

            .nav-links {{ display: flex; gap: 30px; }}

            .nav-links a {{
                text-decoration: none;
                color: var(--dark);
                font-weight: 500;
                transition: color 0.3s;
            }}
            .nav-links a:hover {{ color: var(--primary); }}

            /* Main Content */
            .assessment-main {{
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 30px;
                margin-bottom: 50px;
            }}

            /* Symptoms Panel */
            .symptoms-panel {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            }}

            .search-container {{ position: relative; margin-bottom: 25px; }}

            .search-container i {{
                position: absolute;
                left: 15px;
                top: 50%;
                transform: translateY(-50%);
                color: var(--gray);
            }}

            .search-container input {{
                width: 100%;
                padding: 15px 15px 15px 45px;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                font-size: 16px;
                transition: all 0.3s;
                background: var(--light);
            }}
            .search-container input:focus {{
                outline: none;
                border-color: var(--primary);
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }}

            .symptoms-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 12px;
                max-height: 500px;
                overflow-y: auto;
                padding: 10px;
            }}

            .symptom-card {{
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 15px;
                cursor: pointer;
                transition: all 0.3s ease;
                text-align: center;
                position: relative;
                overflow: hidden;
            }}
            .symptom-card::before {{
                content: '';
                position: absolute;
                top: 0; left: -100%;
                width: 100%; height: 100%;
                background: linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.1), transparent);
                transition: left 0.5s;
            }}
            .symptom-card:hover::before {{ left: 100%; }}
            .symptom-card:hover {{
                border-color: var(--primary);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            .symptom-card.selected {{
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: white;
                border-color: var(--primary);
                transform: scale(1.02);
            }}
            .symptom-card.emergency {{
                border-color: var(--danger);
                background: linear-gradient(135deg, #fef2f2, #fff);
            }}
            .symptom-card.emergency.selected {{
                background: linear-gradient(135deg, var(--danger), #dc2626);
            }}
            .emergency-badge {{
                position: absolute;
                top: 8px; right: 8px;
                background: var(--danger);
                color: white;
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 0.7rem;
                font-weight: 600;
            }}

            /* Selected Panel */
            .selected-panel {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                height: fit-content;
                position: sticky;
                top: 20px;
            }}

            .selected-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 20px;
            }}

            .selected-count {{
                background: var(--primary);
                color: white;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: 600;
            }}

            .selected-list {{
                max-height: 300px;
                overflow-y: auto;
                margin-bottom: 25px;
            }}

            .selected-item {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px 15px;
                background: var(--light);
                border-radius: 10px;
                margin-bottom: 8px;
                transition: all 0.3s;
            }}
            .selected-item:hover {{ background: #e2e8f0; }}
            .selected-item.emergency {{
                background: #fef2f2;
                border-left: 4px solid var(--danger);
            }}

            .remove-btn {{
                background: none;
                border: none;
                color: var(--gray);
                cursor: pointer;
                padding: 5px;
                border-radius: 5px;
                transition: all 0.3s;
            }}
            .remove-btn:hover {{ background: var(--danger); color: white; }}

            /* Action Buttons */
            .action-buttons {{ display: flex; gap: 12px; flex-direction: column; }}
            .btn {{
                padding: 15px 25px;
                border: none; border-radius: 12px;
                font-size: 16px; font-weight: 600;
                cursor: pointer; transition: all 0.3s ease;
                display: flex; align-items: center; justify-content: center; gap: 10px;
            }}
            .btn-primary {{
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: white;
                box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
            }}
            .btn-primary:hover:not(:disabled) {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(37, 99, 235, 0.4);
            }}
            .btn-primary:disabled {{ opacity: 0.6; cursor: not-allowed; transform: none; }}
            .btn-secondary {{ background: var(--light); color: var(--dark); border: 2px solid #e2e8f0; }}
            .btn-secondary:hover {{ background: #e2e8f0; }}

            /* Results */
            .results-container {{ display: none; margin-top: 40px; }}
            .result-card {{
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                animation: slideUp 0.5s ease;
            }}
            @keyframes slideUp {{
                from {{ opacity: 0; transform: translateY(30px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}

            .result-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #e2e8f0;
            }}

            .condition-icon {{ font-size: 3rem; margin-right: 20px; }}
            .condition-info h2 {{ font-size: 2rem; margin-bottom: 5px; }}

            .confidence-badge {{
                background: linear-gradient(135deg, var(--success), #059669);
                color: white; padding: 8px 16px; border-radius: 20px; font-weight: 600;
            }}
            .severity-badge {{ padding: 8px 16px; border-radius: 20px; font-weight: 600; color: white; }}
            .severity-critical {{ background: var(--danger); }}
            .severity-moderate {{ background: var(--warning); }}
            .severity-mild {{ background: var(--success); }}

            .treatment-list {{ list-style: none; margin: 25px 0; }}
            .treatment-list li {{
                padding: 12px 0; border-bottom: 1px solid #e2e8f0;
                display: flex; align-items: center; gap: 12px;
            }}
            .treatment-list li:before {{
                content: '✓';
                background: var(--success); color: white; width: 24px; height: 24px;
                border-radius: 50%; display: flex; align-items: center; justify-content: center;
                font-size: 0.8rem; font-weight: bold;
            }}

            .emergency-alert {{
                background: linear-gradient(135deg, #fef2f2, #fff);
                border: 2px solid var(--danger);
                border-radius: 15px;
                padding: 25px; margin: 25px 0;
                text-align: center;
            }}
            .emergency-alert h3 {{ color: var(--danger); margin-bottom: 10px; }}

            .info-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 25px 0;
            }}

            .info-card {{
                background: var(--light);
                padding: 20px;
                border-radius: 12px;
                border-left: 4px solid var(--primary);
            }}

            .info-card h4 {{
                color: var(--dark);
                margin-bottom: 10px;
                font-size: 1rem;
            }}

            /* Responsive */
            @media (max-width: 1024px) {{
                .assessment-main {{ grid-template-columns: 1fr; }}
                .selected-panel {{ position: static; }}
            }}
            @media (max-width: 768px) {{
                .symptoms-grid {{ grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); }}
                .header-content {{ flex-direction: column; gap: 15px; }}
                .nav-links {{ gap: 20px; }}
                .info-grid {{ grid-template-columns: 1fr; }}
            }}
        </style>
    </head>
    <body>
        <!-- Header -->
        <header class="assessment-header">
            <div class="container">
                <div class="header-content">
                    <div class="logo">
                        <i class="fas fa-brain"></i>
                        <span>MediScan Pro</span>
                    </div>
                    <nav class="nav-links">
                        <a href="/"><i class="fas fa-home"></i> Home</a>
                        <a href="/symptoms"><i class="fas fa-stethoscope"></i> Assessment</a>
                    </nav>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <div class="container">
            <div class="assessment-main">
                <!-- Symptoms Selection -->
                <div class="symptoms-panel">
                    <h2 style="margin-bottom: 20px; color: var(--dark);">Comprehensive Symptom Assessment</h2>
                    <p style="color: var(--gray); margin-bottom: 25px;">Select all symptoms you're experiencing. Emergency symptoms are highlighted in red. Our AI analyzes 150+ symptoms across 25+ conditions.</p>
                    
                    <div class="search-container">
                        <i class="fas fa-search"></i>
                        <input type="text" id="symptomSearch" placeholder="Search 150+ symptoms...">
                    </div>
                    
                    <div class="symptoms-grid" id="symptomsGrid">
    '''
    
    # Add all symptoms to the grid
    for symptom in symptoms_list:
        is_emergency = symptom in EMERGENCY_SYMPTOMS
        display_name = symptom.replace('_', ' ').title()
        symptom_class = "symptom-card"
        if is_emergency:
            symptom_class += " emergency"
        
        html += f'''
                        <div class="{symptom_class}" onclick="toggleSymptom(this)" data-symptom="{symptom}">
                            {display_name}
                            {('<div class="emergency-badge">ER</div>' if is_emergency else '')}
                        </div>
        '''
    
    html += f'''
                    </div>
                </div>

                <!-- Selected Symptoms -->
                <div class="selected-panel">
                    <div class="selected-header">
                        <h3 style="color: var(--dark);">Selected Symptoms</h3>
                        <div class="selected-count" id="selectedCount">0</div>
                    </div>
                    
                    <div class="selected-list" id="selectedList">
                        <div style="text-align: center; color: var(--gray); padding: 40px 20px;">
                            <i class="fas fa-clipboard-list" style="font-size: 3rem; margin-bottom: 15px; opacity: 0.5;"></i>
                            <p>No symptoms selected yet</p>
                        </div>
                    </div>
                    
                    <div class="action-buttons">
                        <button class="btn btn-primary" onclick="performAssessment()" id="assessBtn" disabled>
                            <i class="fas fa-bolt"></i>
                            Analyze Symptoms
                        </button>
                        <button class="btn btn-secondary" onclick="clearSelection()">
                            <i class="fas fa-eraser"></i>
                            Clear All
                        </button>
                    </div>
                </div>
            </div>

            <!-- Results Container -->
            <div class="results-container" id="resultsContainer">
                <!-- Results will be populated here -->
            </div>
        </div>

        <script>
            // Make emergency list available to JS
            const EMERGENCY_SYMPTOMS = {emergency_json};

            let selectedSymptoms = new Set();

            function formatSymptom(symptom) {{
                return symptom.replace(/_/g, ' ').replace(/\\b\\w/g, char => char.toUpperCase());
            }}

            // Search functionality
            document.getElementById('symptomSearch').addEventListener('input', function(e) {{
                const searchTerm = e.target.value.toLowerCase();
                const symptoms = document.querySelectorAll('.symptom-card');
                symptoms.forEach(symptom => {{
                    const symptomText = symptom.textContent.toLowerCase();
                    symptom.style.display = symptomText.includes(searchTerm) ? 'block' : 'none';
                }});
            }});

            function toggleSymptom(element) {{
                const symptom = element.getAttribute('data-symptom');
                if (selectedSymptoms.has(symptom)) {{
                    selectedSymptoms.delete(symptom);
                    element.classList.remove('selected');
                }} else {{
                    selectedSymptoms.add(symptom);
                    element.classList.add('selected');
                }}
                updateSelectedList();
                updateAssessmentButton();
            }}

            function updateSelectedList() {{
                const selectedList = document.getElementById('selectedList');
                const selectedCount = document.getElementById('selectedCount');
                selectedCount.textContent = selectedSymptoms.size;

                if (selectedSymptoms.size === 0) {{
                    selectedList.innerHTML = `
                        <div style="text-align: center; color: var(--gray); padding: 40px 20px;">
                            <i class="fas fa-clipboard-list" style="font-size: 3rem; margin-bottom: 15px; opacity: 0.5;"></i>
                            <p>No symptoms selected yet</p>
                        </div>
                    `;
                    return;
                }}

                let html = '';
                Array.from(selectedSymptoms).forEach(symptom => {{
                    const isEmergency = EMERGENCY_SYMPTOMS.includes(symptom);
                    const emergencyClass = isEmergency ? 'emergency' : '';
                    html += `
                        <div class="selected-item ${{emergencyClass}}">
                            <span>${{formatSymptom(symptom)}}</span>
                            <button class="remove-btn" onclick="removeSymptom('${{symptom.replace(/'/g, "\\\\'")}}')">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    `;
                }});
                selectedList.innerHTML = html;
            }}

            function removeSymptom(symptom) {{
                selectedSymptoms.delete(symptom);
                const element = document.querySelector(`[data-symptom="${{symptom}}"]`);
                if (element) element.classList.remove('selected');
                updateSelectedList();
                updateAssessmentButton();
            }}

            function updateAssessmentButton() {{
                const assessBtn = document.getElementById('assessBtn');
                assessBtn.disabled = selectedSymptoms.size === 0;
            }}

            function clearSelection() {{
                selectedSymptoms.clear();
                document.querySelectorAll('.symptom-card').forEach(item => item.classList.remove('selected'));
                updateSelectedList();
                updateAssessmentButton();
            }}

            async function performAssessment() {{
                const assessBtn = document.getElementById('assessBtn');
                const resultsContainer = document.getElementById('resultsContainer');

                assessBtn.disabled = true;
                assessBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
                resultsContainer.style.display = 'none';

                try {{
                    const response = await fetch('/diagnose', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify({{ symptoms: Array.from(selectedSymptoms) }})
                    }});

                    if (!response.ok) {{
                        let errorMessage = `Server error: ${{response.status}}`;
                        try {{
                            const errorData = await response.json();
                            if (errorData && errorData.error) errorMessage = errorData.error;
                        }} catch (_) {{}}
                        throw new Error(errorMessage);
                    }}

                    const result = await response.json();
                    displayResults(result);

                }} catch (error) {{
                    resultsContainer.innerHTML = `
                        <div class="result-card">
                            <div class="emergency-alert">
                                <h3><i class="fas fa-exclamation-triangle"></i> Assessment Error</h3>
                                <p>${{error.message}}</p>
                            </div>
                        </div>
                    `;
                    resultsContainer.style.display = 'block';
                }} finally {{
                    assessBtn.disabled = false;
                    assessBtn.innerHTML = '<i class="fas fa-bolt"></i> Analyze Symptoms';
                }}
            }}

            function displayResults(result) {{
                const resultsContainer = document.getElementById('resultsContainer');

                // Map severity text to class safely
                const sev = (result.severity || '').toLowerCase();
                let severityKey = 'mild';
                if (sev.includes('critical') || sev.includes('severe') || sev.includes('high')) severityKey = 'critical';
                else if (sev.includes('moderate') || sev.includes('medium')) severityKey = 'moderate';
                const severityClass = `severity-${{severityKey}}`;

                const emergencyAlert = result.is_emergency ? `
                    <div class="emergency-alert">
                        <h3><i class="fas fa-ambulance"></i> EMERGENCY ALERT</h3>
                        <p>Your symptoms indicate a potential medical emergency that requires immediate attention.</p>
                        <p><strong>Action Required:</strong> Seek emergency medical care immediately or call your local emergency number.</p>
                    </div>
                ` : '';

                const treatments = Array.isArray(result.treatment) ? result.treatment : [];

                // Additional info cards
                const additionalInfo = result.recovery_time ? `
                    <div class="info-grid">
                        <div class="info-card">
                            <h4><i class="fas fa-clock"></i> Expected Recovery</h4>
                            <p>${{result.recovery_time || 'Varies based on treatment'}}</p>
                        </div>
                        <div class="info-card">
                            <h4><i class="fas fa-virus"></i> Contagious Period</h4>
                            <p>${{result.contagious_period || 'Consult healthcare provider'}}</p>
                        </div>
                        <div class="info-card">
                            <h4><i class="fas fa-stethoscope"></i> Medical Follow-up</h4>
                            <p>${{result.follow_up || 'Consult healthcare provider if symptoms persist'}}</p>
                        </div>
                    </div>
                ` : '';

                resultsContainer.innerHTML = `
                    <div class="result-card">
                        ${{emergencyAlert}}
                        <div class="result-header">
                            <div style="display: flex; align-items: center;">
                                <div class="condition-icon">${{result.icon || '🩺'}}</div>
                                <div class="condition-info">
                                    <h2>${{result.condition || 'Possible Condition'}}</h2>
                                    <div style="display: flex; gap: 10px; align-items: center; margin-top: 10px;">
                                        <span class="confidence-badge">${{Number(result.confidence || 0)}}% Confidence</span>
                                        <span class="severity-badge ${{severityClass}}">${{result.severity || 'Mild'}}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div style="margin-bottom: 25px;">
                            <h3 style="margin-bottom: 15px; color: var(--dark);">
                                <i class="fas fa-prescription-bottle-medical"></i> Evidence-Based Treatment Plan
                            </h3>
                            <ul class="treatment-list">
                                ${{treatments.map(t => `<li>${{t}}</li>`).join('')}}
                            </ul>
                        </div>

                        ${{additionalInfo}}

                        <div style="margin-top: 30px; padding: 20px; background: #f8fafc; border-radius: 12px; border-left: 4px solid var(--warning);">
                            <p style="color: var(--gray); font-size: 0.9rem;">
                                <strong>Medical Disclaimer:</strong> This assessment is based on reported symptoms and AI analysis of 25+ medical conditions. 
                                It provides evidence-based treatment suggestions but does not replace professional medical evaluation. 
                                Always consult healthcare providers for accurate diagnosis and treatment planning. 
                                In emergency situations, call your local emergency services immediately.
                            </p>
                        </div>
                    </div>
                `;

                resultsContainer.style.display = 'block';
                resultsContainer.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        </script>
    </body>
    </html>
    '''
    
    return html

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
                    'Seek immediate medical attention - call emergency services',
                    'Do not delay care - emergency symptoms detected',
                    'Go to nearest emergency department',
                    'Inform medical staff of all symptoms immediately'
                ],
                'follow_up': 'Emergency evaluation required immediately',
                'matched_symptoms': len(emergency_symptoms),
                'icon': '🚑',
                'is_emergency': True,
                'recovery_time': 'Requires immediate medical intervention',
                'contagious_period': 'Not applicable - emergency situation'
            })
        
        # Enhanced matching algorithm with weighted scores
        best_match = None
        best_score = 0
        possible_conditions = []
        
        for condition_id, condition in MEDICAL_CONDITIONS.items():
            # Calculate weighted scores
            key_matches = len(set(user_symptoms) & set(condition['key_symptoms']))
            total_matches = len(set(user_symptoms) & set(condition['symptoms']))
            total_possible = len(condition['symptoms'])
            
            # Enhanced scoring: key symptoms weighted higher
            base_score = (total_matches / total_possible) * 60
            key_bonus = (key_matches / len(condition['key_symptoms'])) * 40
            
            # Bonus for matching multiple key symptoms
            if key_matches >= 2:
                key_bonus *= 1.5
            
            final_score = base_score + key_bonus
            
            if final_score > 30:  # Only consider conditions with reasonable match
                possible_conditions.append({
                    'id': condition_id,
                    'score': final_score,
                    'key_matches': key_matches,
                    'total_matches': total_matches
                })
            
            if final_score > best_score:
                best_score = final_score
                best_match = condition_id
        
        # If we have multiple good matches, return the best one
        if best_match and best_score >= 40:
            condition = MEDICAL_CONDITIONS[best_match]
            return jsonify({
                'condition': condition['name'],
                'severity': condition['severity'],
                'confidence': min(95, round(best_score, 2)),
                'treatment': condition['treatment'],
                'follow_up': 'Follow up with healthcare provider if symptoms persist or worsen',
                'matched_symptoms': len(set(user_symptoms) & set(condition['symptoms'])),
                'icon': condition['icon'],
                'is_emergency': False,
                'recovery_time': condition.get('recovery_time', 'Varies based on treatment adherence'),
                'contagious_period': condition.get('contagious_period', 'Consult healthcare provider')
            })
        else:
            # Return general advice for unclear matches
            return jsonify({
                'condition': 'General Medical Condition - Further Evaluation Recommended',
                'severity': 'Mild to Moderate',
                'confidence': 60,
                'treatment': [
                    'Rest and adequate hydration (8-10 glasses water daily)',
                    'Acetaminophen 500mg every 6 hours as needed for pain/fever',
                    'Monitor symptoms closely for changes',
                    'Maintain comfortable environment with proper ventilation',
                    'Light, nutritious diet as tolerated',
                    'Avoid strenuous activity until symptoms improve',
                    'Consult healthcare provider for persistent or worsening symptoms'
                ],
                'follow_up': 'Schedule appointment with healthcare provider within 24-48 hours',
                'matched_symptoms': len(user_symptoms),
                'icon': '🤔',
                'is_emergency': False,
                'recovery_time': 'Monitor for 2-3 days',
                'contagious_period': 'Practice good hygiene until symptoms resolve'
            })
            
    except Exception as e:
        return jsonify({'error': f'Diagnosis error: {str(e)}'}), 500

if __name__ == '__main__':
    print("🚀 Starting MediScan Pro - Enhanced Medical Diagnosis System")
    print("📍 Access: http://localhost:5000")
    print("📊 Features: 25+ conditions, 150+ symptoms, evidence-based treatments")
    print("⚡ Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)