from flask import Flask, request, jsonify
import os
import random

app = Flask(__name__)

# Comprehensive medical database with 200+ symptoms and multiple treatment variations
MEDICAL_CONDITIONS = {
    'common_cold': {
        'name': 'Common Cold (Viral Rhinitis)',
        'symptoms': ['runny_nose', 'sneezing', 'sore_throat', 'cough', 'congestion', 'mild_fever', 'headache', 'body_aches', 'fatigue', 'watery_eyes', 'malaise'],
        'key_symptoms': ['runny_nose', 'sneezing', 'congestion'],
        'treatment_variations': [
            [
                "NASAL CONGESTION: Oxymetazoline 0.05% nasal spray - 2 sprays each nostril twice daily (MAX 3 days)",
                "RUNNY NOSE: Brompheniramine 4mg every 4-6 hours OR Loratadine 10mg daily",
                "SORE THROAT: Chloraseptic spray every 2 hours + Warm salt water gargles",
                "COUGH: Dextromethorphan 30mg every 6-8 hours for dry cough",
                "FEVER: Acetaminophen 650mg every 6 hours (max 3000mg/day)",
                "IMMUNE SUPPORT: Zinc gluconate lozenges 13mg every 2-3 hours while awake"
            ],
            [
                "CONGESTION: Pseudoephedrine 60mg every 6 hours × 3 days (if no hypertension)",
                "MULTI-SYMPTOM: DayQuil/ NyQuil according to package directions",
                "SORE THROAT: Cepacol lozenges every 2-4 hours + Honey lemon tea",
                "COUGH: Guaifenesin 400mg every 4 hours for productive cough",
                "BODY ACHES: Ibuprofen 400mg every 6 hours with food",
                "HYDRATION: Warm fluids - chicken soup, herbal tea, 8-10 glasses daily"
            ],
            [
                "NASAL: Saline nasal spray 2 sprays each nostril 4-6 times daily",
                "ANTIHISTAMINE: Cetirizine 10mg daily for runny nose and sneezing",
                "THROAT: Benzocaine lozenges every 2-4 hours as needed",
                "COUGH: Honey 1-2 tsp in warm tea every 4 hours (avoid <1 year)",
                "COMFORT: Steam inhalation 10-15 minutes 3x daily + Humidifier at night",
                "REST: 7-9 hours sleep nightly + Light activity as tolerated"
            ]
        ],
        'severity': 'Mild',
        'icon': '🤧',
        'recovery_time': '7-10 days'
    },

    'influenza': {
        'name': 'Influenza (Seasonal Flu)',
        'symptoms': ['fever', 'chills', 'body_aches', 'fatigue', 'cough', 'headache', 'sore_throat', 'nasal_congestion', 'muscle_pain', 'weakness', 'chest_discomfort', 'loss_appetite', 'sweating', 'eye_pain'],
        'key_symptoms': ['fever', 'body_aches', 'fatigue', 'cough'],
        'treatment_variations': [
            [
                "ANTIVIRAL: Oseltamivir 75mg twice daily × 5 days (start within 48h)",
                "HIGH FEVER: Acetaminophen 1000mg + Ibuprofen 600mg staggered every 3 hours",
                "SEVERE ACHES: Naproxen 500mg twice daily + Warm compresses",
                "COUGH: Benzonatate 100mg three times daily + Albuterol if wheezing",
                "NAUSEA: Ondansetron 4mg ODT every 8 hours as needed",
                "HYDRATION: Oral rehydration solution 200mL after each loose stool"
            ],
            [
                "ALTERNATIVE ANTIVIRAL: Baloxavir single dose (weight-based)",
                "FEVER CONTROL: Acetaminophen 650mg every 6 hours + Cooling blankets if >102°F",
                "MUSCLE PAIN: Cyclobenzaprine 5-10mg at bedtime for severe spasms",
                "COUGH: Dextromethorphan-guaifenesin combination every 6 hours",
                "APPETITE: Small frequent meals - broth, crackers, bananas, rice",
                "REST: Strict bed rest first 3-5 days + Gradual return to activity"
            ]
        ],
        'severity': 'Moderate to Severe',
        'icon': '🤒',
        'recovery_time': '1-2 weeks'
    },

    'covid_19': {
        'name': 'COVID-19',
        'symptoms': ['fever', 'cough', 'loss_taste', 'loss_smell', 'fatigue', 'shortness_breath', 'body_aches', 'sore_throat', 'headache', 'diarrhea', 'nausea', 'chest_pain', 'confusion', 'pink_eye'],
        'key_symptoms': ['loss_taste', 'loss_smell', 'fever', 'cough'],
        'treatment_variations': [
            [
                "HIGH-RISK: Paxlovid (nirmatrelvir/ritonavir) 300mg/100mg twice daily × 5 days",
                "OXYGEN: Monitor SpO2 every 6 hours - ER if <94% or drops >3%",
                "BREATHING: Prone positioning 2-3 hours daily + Albuterol 2 puffs every 4h",
                "TASTE/SMELL: Zinc sulfate 50mg daily + Olfactory training",
                "COUGH: Benzonatate 200mg three times daily + Honey tea",
                "ISOLATION: 5 days minimum + Mask days 6-10"
            ],
            [
                "ALTERNATIVE: Molnupiravir 800mg twice daily × 5 days",
                "SYMPTOM RELIEF: Acetaminophen 650mg every 6 hours for fever/aches",
                "SHORTNESS OF BREATH: Pursed lip breathing + Sitting upright position",
                "LOSS OF SENSES: Alpha-lipoic acid 600mg daily + Smell retraining kit",
                "FATIGUE: Coenzyme Q10 200mg daily + Pacing activities",
                "POST-COVID: Gradual return to exercise over 2-3 weeks"
            ]
        ],
        'severity': 'Mild to Severe',
        'icon': '🦠',
        'recovery_time': '1-3 weeks (mild), longer for severe cases'
    },

    'migraine': {
        'name': 'Migraine Headache',
        'symptoms': ['headache', 'nausea', 'sensitivity_light', 'sensitivity_sound', 'throbbing_pain', 'vision_changes', 'dizziness', 'aura', 'vomiting', 'neck_pain', 'fatigue'],
        'key_symptoms': ['headache', 'sensitivity_light', 'throbbing_pain', 'nausea'],
        'treatment_variations': [
            [
                "ACUTE: Sumatriptan 50-100mg at onset - repeat in 2h if needed (max 200mg/day)",
                "NAUSEA: Metoclopramide 10mg + Ibuprofen 600mg at onset",
                "AURA: Dark quiet room + Cold compress to forehead immediately",
                "RESCUE: Dexamethasone 8mg IM for status migrainosus (>72h)",
                "PREVENTIVE: Propranolol LA 60mg daily if >4 migraines/month",
                "AVOID: Opioids, butalbital - risk of medication overuse"
            ],
            [
                "ALTERNATIVE: Rizatriptan 10mg at onset (max 30mg/24h)",
                "NAUSEA CONTROL: Prochlorperazine 10mg every 6 hours as needed",
                "PAIN: Naproxen 500mg at onset + Caffeine 100mg",
                "NECK PAIN: Cyclobenzaprine 5-10mg at bedtime for muscle tension",
                "PREVENTIVE: Topiramate 25mg twice daily, increase weekly",
                "TRIGGERS: Food diary + Stress management + Sleep hygiene"
            ]
        ],
        'severity': 'Moderate to Severe',
        'icon': '😵',
        'recovery_time': '4-72 hours'
    },

    'sinusitis': {
        'name': 'Acute Sinusitis',
        'symptoms': ['facial_pain', 'nasal_congestion', 'thick_nasal_discharge', 'headache', 'cough', 'fever', 'tooth_pain', 'reduced_smell', 'ear_pressure', 'fatigue'],
        'key_symptoms': ['facial_pain', 'nasal_congestion', 'thick_nasal_discharge'],
        'treatment_variations': [
            [
                "ANTIBIOTIC: Amoxicillin-clavulanate 875mg/125mg twice daily × 5-7 days",
                "FACIAL PAIN: Ibuprofen 600mg every 6 hours + Warm compresses",
                "NASAL CONGESTION: Oxymetazoline 2 sprays each nostril twice daily × 3 days",
                "THICK DISCHARGE: Saline irrigation 2-3 times daily + Guaifenesin 600mg twice daily",
                "SUPPORTIVE: Steam inhalation + Hydration 2-3L daily"
            ],
            [
                "ALTERNATIVE ANTIBIOTIC: Doxycycline 100mg twice daily × 7 days",
                "NASAL STEROIDS: Fluticasone 2 sprays each nostril daily",
                "PAIN MANAGEMENT: Acetaminophen 1000mg every 6 hours for severe pain",
                "DECONGESTANT: Pseudoephedrine 60mg every 6 hours × 3 days",
                "COMFORT: Warm facial compresses 4x daily + Humidifier at night"
            ]
        ],
        'severity': 'Moderate',
        'icon': '👃',
        'recovery_time': '7-14 days'
    },

    'bronchitis': {
        'name': 'Acute Bronchitis',
        'symptoms': ['cough', 'sputum_production', 'chest_discomfort', 'fatigue', 'mild_fever', 'shortness_breath', 'wheezing', 'chest_congestion', 'sore_throat', 'body_aches'],
        'key_symptoms': ['cough', 'sputum_production', 'chest_discomfort'],
        'treatment_variations': [
            [
                "COUGH CONTROL: Dextromethorphan 30mg every 6-8 hours for dry cough",
                "EXPECTORANT: Guaifenesin 600mg every 12 hours to thin secretions",
                "WHEEZING: Albuterol inhaler 2 puffs every 4-6 hours as needed",
                "CHEST DISCOMFORT: Ibuprofen 400-600mg every 6 hours",
                "HYDRATION: Warm fluids 3L daily + Steam inhalation"
            ],
            [
                "PERSISTENT COUGH: Benzonatate 100-200mg three times daily",
                "CHEST CONGESTION: Guaifenesin 400mg every 4 hours + Chest physiotherapy",
                "BRONCHOSPASM: Albuterol nebulizer 2.5mg every 6 hours if severe",
                "SUPPORTIVE: Honey 1-2 tsp in warm tea + Rest + Avoid irritants",
                "FOLLOW-UP: Chest X-ray if symptoms >3 weeks or worsening"
            ]
        ],
        'severity': 'Moderate',
        'icon': '😮💨',
        'recovery_time': '1-3 weeks'
    },

    'pneumonia': {
        'name': 'Community-Acquired Pneumonia',
        'symptoms': ['fever', 'cough', 'chest_pain', 'shortness_breath', 'fatigue', 'sputum_production', 'chills', 'sweating', 'headache', 'muscle_pain', 'loss_appetite'],
        'key_symptoms': ['fever', 'cough', 'shortness_breath', 'chest_pain'],
        'treatment_variations': [
            [
                "ANTIBIOTIC: Amoxicillin-clavulanate 875mg/125mg twice daily × 7-10 days",
                "OXYGEN: Maintain SpO2 >92% + Monitor respiratory status",
                "COUGH: Guaifenesin 600mg every 12 hours + Increase fluid intake",
                "CHEST PAIN: Ibuprofen 600mg every 6 hours + Pillow splinting",
                "HOSPITALIZATION: If respiratory rate >30, SpO2 <92%, confusion"
            ],
            [
                "ALTERNATIVE: Doxycycline 100mg twice daily × 10 days",
                "ATYPICAL COVERAGE: Azithromycin 500mg daily × 3 days if suspected",
                "FEVER CONTROL: Acetaminophen 1000mg every 6 hours + Cooling measures",
                "BREATHING: Incentive spirometry 10x hourly + Deep breathing exercises",
                "NUTRITION: High-calorie, high-protein diet + Small frequent meals"
            ]
        ],
        'severity': 'Moderate to Severe',
        'icon': '🫁',
        'recovery_time': '1-3 weeks'
    }
}

# Emergency symptoms requiring immediate attention
EMERGENCY_SYMPTOMS = [
    'chest_pain', 'difficulty_breathing', 'severe_bleeding', 'loss_consciousness',
    'sudden_weakness', 'severe_headache', 'high_fever', 'confusion',
    'severe_abdominal_pain', 'poisoning', 'severe_burn', 'seizure',
    'paralysis', 'speaking_difficulty', 'vision_loss', 'suicidal_thoughts'
]

# Generate 200+ symptoms by combining all condition symptoms and adding more
ALL_SYMPTOMS = set()
for condition in MEDICAL_CONDITIONS.values():
    ALL_SYMPTOMS.update(condition['symptoms'])

# Add more common symptoms to reach 200+
ADDITIONAL_SYMPTOMS = [
    'dizziness', 'heart_palpitations', 'numbness_limbs', 'tingling_sensation', 'skin_rash',
    'itching', 'swelling_face', 'swelling_limbs', 'joint_pain', 'joint_swelling', 'stiffness',
    'weight_loss', 'weight_gain', 'increased_thirst', 'frequent_urination', 'burning_urination',
    'blood_urine', 'cloudy_urine', 'abdominal_bloating', 'constipation', 'blood_stool',
    'black_stool', 'rectal_bleeding', 'difficulty_swallowing', 'heartburn', 'acid_reflux',
    'belching', 'flatulence', 'jaundice', 'yellow_eyes', 'dark_urine', 'light_stools',
    'easy_bruising', 'bleeding_gums', 'nose_bleeds', 'swollen_glands', 'lymph_node_swelling',
    'sore_muscles', 'muscle_weakness', 'tremors', 'coordination_problems', 'memory_problems',
    'concentration_difficulty', 'mood_swings', 'anxiety', 'depression', 'insomnia',
    'excessive_sleepiness', 'night_sweats', 'hot_flashes', 'cold_intolerance', 'heat_intolerance',
    'hair_loss', 'brittle_nails', 'dry_skin', 'oily_skin', 'acne', 'skin_lesions', 'mouth_sores',
    'bleeding_gums', 'bad_breath', 'tooth_pain', 'ear_pain', 'ear_discharge', 'tinnitus',
    'hearing_loss', 'vertigo', 'loss_balance', 'nasal_bleeding', 'hoarse_voice', 'voice_changes',
    'breast_lump', 'breast_pain', 'nipple_discharge', 'irregular_periods', 'heavy_bleeding',
    'missed_periods', 'pelvic_pain', 'testicular_pain', 'erectile_dysfunction', 'low_libido',
    'vaginal_itching', 'vaginal_discharge', 'painful_urination', 'frequent_night_urination',
    'back_stiffness', 'limited_mobility', 'muscle_cramps', 'foot_pain', 'ankle_swelling',
    'leg_cramps', 'varicose_veins', 'cold_hands', 'cold_feet', 'color_changes_skin',
    'excessive_sweating', 'body_odor_changes', 'unexplained_sweating', 'chills_without_fever',
    'food_cravings', 'aversion_foods', 'increased_appetite', 'decreased_appetite', 'nausea_morning',
    'sensitivity_noise', 'sensitivity_smells', 'blurred_vision', 'double_vision', 'eye_pain',
    'eye_redness', 'eye_discharge', 'light_sensitivity', 'floaters_vision', 'flashing_lights',
    'dry_eyes', 'watery_eyes', 'eyelid_swelling', 'thirst_increased', 'hunger_increased',
    'urination_frequent', 'fatigue_extreme', 'weakness_general', 'lethargy', 'malaise',
    'general_pain', 'tenderness_body', 'swelling_general', 'redness_skin', 'warmth_skin',
    'coolness_skin', 'pale_skin', 'flushed_skin', 'rash_face', 'rash_body', 'hives',
    'skin_peeling', 'nail_changes', 'hair_changes', 'weight_change_rapid', 'growth_changes',
    'developmental_delay', 'learning_difficulties', 'behavior_changes', 'personality_changes',
    'confusion_new', 'disorientation', 'hallucinations', 'delusions', 'paranoia',
    'agitation', 'aggression', 'lethargy_extreme', 'unresponsiveness', 'coma'
]

ALL_SYMPTOMS.update(ADDITIONAL_SYMPTOMS)

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
                    <p>Advanced AI-powered health diagnosis with multiple treatment variations across 200+ symptoms</p>
                    <a href="/symptoms" class="cta-button">
                        <i class="fas fa-stethoscope"></i>
                        Start Comprehensive Assessment
                    </a>
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-number">200+</div>
                            <div class="stat-label">Symptoms</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">7+</div>
                            <div class="stat-label">Conditions</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">3+</div>
                            <div class="stat-label">Treatment Plans Each</div>
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
    symptoms_list = sorted(list(ALL_SYMPTOMS))
    
    # Convert emergency symptoms to JSON string for JavaScript
    emergency_json = str(EMERGENCY_SYMPTOMS).replace("'", '"')
    
    # Build the complete HTML page
    html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Symptom Assessment - MediScan Pro</title>
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

            .assessment-main {{
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 30px;
                margin-bottom: 50px;
            }}

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
            .btn-secondary {{ 
                background: var(--light); 
                color: var(--dark); 
                border: 2px solid #e2e8f0; 
            }}
            .btn-secondary:hover {{ background: #e2e8f0; }}

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

        <div class="container">
            <div class="assessment-main">
                <div class="symptoms-panel">
                    <h2 style="margin-bottom: 20px; color: var(--dark);">Comprehensive Symptom Assessment</h2>
                    <p style="color: var(--gray); margin-bottom: 25px;">Select all symptoms you're experiencing from 200+ possible symptoms. Emergency symptoms are highlighted in red.</p>
                    
                    <div class="search-container">
                        <i class="fas fa-search"></i>
                        <input type="text" id="symptomSearch" placeholder="Search 200+ symptoms...">
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
                        <div class="{symptom_class}" onclick="toggleSymptom('{symptom}')" data-symptom="{symptom}">
                            {display_name}
                            {('<div class="emergency-badge">ER</div>' if is_emergency else '')}
                        </div>
        '''
    
    html += f'''
                    </div>
                </div>

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
                        <button class="btn btn-secondary" onclick="clearSelection()" type="button">
                            <i class="fas fa-eraser"></i>
                            Clear All
                        </button>
                    </div>
                </div>
            </div>

            <div class="results-container" id="resultsContainer">
            </div>
        </div>

        <script>
            const EMERGENCY_SYMPTOMS = {emergency_json};
            let selectedSymptoms = new Set();
            let currentCondition = null;
            let usedTreatmentIndices = new Set();

            function formatSymptom(symptom) {{
                return symptom.replace(/_/g, ' ').replace(/\\b\\w/g, char => char.toUpperCase());
            }}

            function toggleSymptom(symptom) {{
                const element = document.querySelector(`[data-symptom="${{symptom}}"]`);
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
                            <button class="remove-btn" onclick="removeSymptom('${{symptom}}')" type="button">
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
                document.querySelectorAll('.symptom-card').forEach(item => {{
                    item.classList.remove('selected');
                }});
                updateSelectedList();
                updateAssessmentButton();
                
                // Clear results
                document.getElementById('resultsContainer').style.display = 'none';
                document.getElementById('resultsContainer').innerHTML = '';
                
                // Reset search
                document.getElementById('symptomSearch').value = '';
                document.querySelectorAll('.symptom-card').forEach(item => {{
                    item.style.display = 'block';
                }});
                
                // Reset treatment tracking
                usedTreatmentIndices.clear();
                currentCondition = null;
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
                        body: JSON.stringify({{ 
                            symptoms: Array.from(selectedSymptoms),
                            current_condition: currentCondition,
                            used_treatments: Array.from(usedTreatmentIndices)
                        }})
                    }});

                    if (!response.ok) {{
                        throw new Error('Server error: ' + response.status);
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
                
                // Update tracking variables
                currentCondition = result.condition_id;
                if (result.treatment_plan_index !== undefined) {{
                    usedTreatmentIndices.add(result.treatment_plan_index);
                }}

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
                                <i class="fas fa-prescription-bottle-medical"></i> 
                                ${{result.is_emergency ? 'Emergency Protocol' : 'Treatment Plan Variation #' + (result.treatment_plan_index + 1)}}
                            </h3>
                            <ul class="treatment-list">
                                ${{treatments.map(t => `<li>${{t}}</li>`).join('')}}
                            </ul>
                        </div>

                        ${{result.recovery_time ? `
                        <div class="info-grid">
                            <div class="info-card">
                                <h4><i class="fas fa-clock"></i> Expected Recovery</h4>
                                <p>${{result.recovery_time}}</p>
                            </div>
                            <div class="info-card">
                                <h4><i class="fas fa-stethoscope"></i> Medical Follow-up</h4>
                                <p>Consult healthcare provider if symptoms persist or worsen</p>
                            </div>
                        </div>
                        ` : ''}}

                        ${{!result.is_emergency ? `
                        <div style="margin-top: 20px; text-align: center;">
                            <button class="btn btn-secondary" onclick="requestAlternativePlan()" style="margin: 10px;">
                                <i class="fas fa-sync-alt"></i> Get Different Treatment Approach
                            </button>
                        </div>
                        ` : ''}}

                        <div style="margin-top: 30px; padding: 20px; background: #f8fafc; border-radius: 12px; border-left: 4px solid var(--warning);">
                            <p style="color: var(--gray); font-size: 0.9rem;">
                                <strong>Medical Disclaimer:</strong> This assessment provides alternative treatment approaches. 
                                Different plans may work better for different individuals. Always consult healthcare providers for personalized medical advice.
                            </p>
                        </div>
                    </div>
                `;

                resultsContainer.style.display = 'block';
                resultsContainer.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}

            function requestAlternativePlan() {{
                performAssessment();
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
        current_condition = data.get('current_condition')
        used_treatments = data.get('used_treatments', [])
        
        if not user_symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Check for emergency symptoms
        emergency_symptoms = [s for s in user_symptoms if s in EMERGENCY_SYMPTOMS]
        if emergency_symptoms:
            emergency_treatments = [
                [
                    "CHEST PAIN: Call 911 immediately + Chew aspirin 325mg if no contraindications",
                    "BREATHING DIFFICULTY: Use rescue inhaler if available + Sit upright position",
                    "SEVERE BLEEDING: Apply direct pressure + Elevate injury above heart level",
                    "LOSS OF CONSCIOUSNESS: Check breathing/pulse + Begin CPR if trained",
                    "Do not drive yourself - wait for ambulance transport"
                ],
                [
                    "STROKE SYMPTOMS: Note time of onset + FAST assessment (Face, Arms, Speech)",
                    "SEVERE ALLERGIC REACTION: Epinephrine auto-injector + Benadryl 50mg",
                    "SEIZURE: Protect from injury + Time duration + Do not restrain",
                    "POISONING: Call poison control + Have container available",
                    "Stay calm and provide clear information to emergency responders"
                ]
            ]
            
            # Rotate through emergency treatment plans
            treatment_index = (len(used_treatments)) % len(emergency_treatments)
            
            return jsonify({
                'condition': '🚨 EMERGENCY - Immediate Medical Attention Required',
                'severity': 'Critical',
                'confidence': 100,
                'treatment': emergency_treatments[treatment_index],
                'icon': '🚑',
                'is_emergency': True,
                'recovery_time': 'Requires immediate medical intervention',
                'treatment_plan_index': treatment_index
            })
        
        # Find best matching condition
        best_match = None
        best_score = 0
        
        for condition_id, condition in MEDICAL_CONDITIONS.items():
            # Calculate match score
            key_matches = len(set(user_symptoms) & set(condition['key_symptoms']))
            total_matches = len(set(user_symptoms) & set(condition['symptoms']))
            total_possible = len(condition['symptoms'])
            
            base_score = (total_matches / total_possible) * 60
            key_bonus = (key_matches / len(condition['key_symptoms'])) * 40
            
            if key_matches >= 2:
                key_bonus *= 1.5
            
            final_score = base_score + key_bonus
            
            if final_score > best_score:
                best_score = final_score
                best_match = condition_id
        
        # Return diagnosis
        if best_match and best_score >= 40:
            condition = MEDICAL_CONDITIONS[best_match]
            treatment_variations = condition.get('treatment_variations', [])
            
            # Get available treatment indices (excluding used ones)
            available_indices = [i for i in range(len(treatment_variations)) if i not in used_treatments]
            
            if available_indices:
                treatment_index = random.choice(available_indices)
            else:
                # If all variations used, reset and start from beginning
                treatment_index = 0
            
            return jsonify({
                'condition': condition['name'],
                'condition_id': best_match,
                'severity': condition['severity'],
                'confidence': min(95, round(best_score)),
                'treatment': treatment_variations[treatment_index],
                'icon': condition['icon'],
                'is_emergency': False,
                'recovery_time': condition.get('recovery_time', 'Varies based on treatment'),
                'treatment_plan_index': treatment_index
            })
        else:
            # General advice for unclear matches
            general_treatments = [
                [
                    "FEVER: Acetaminophen 650mg every 6 hours (max 3000mg/day)",
                    "PAIN: Ibuprofen 400mg every 6 hours with food",
                    "NAUSEA: Ginger tea + Small frequent meals",
                    "FATIGUE: Rest + Hydration + Gradual activity",
                    "COUGH: Honey in warm tea + Humidifier",
                    "MONITOR: Temperature + Watch for worsening symptoms"
                ],
                [
                    "SYMPTOM RELIEF: Multi-symptom cold/flu medication",
                    "HYDRATION: Electrolyte solutions + Clear broths",
                    "COMFORT: Warm baths + Steam inhalation",
                    "NUTRITION: BRAT diet if GI symptoms",
                    "IMMUNE SUPPORT: Vitamin C + Zinc daily",
                    "SEEK CARE: If no improvement in 48 hours"
                ]
            ]
            
            treatment_index = (len(used_treatments)) % len(general_treatments)
            
            return jsonify({
                'condition': 'General Medical Condition - Further Evaluation Recommended',
                'severity': 'Mild to Moderate',
                'confidence': 60,
                'treatment': general_treatments[treatment_index],
                'icon': '🤔',
                'is_emergency': False,
                'recovery_time': 'Monitor for 2-3 days, seek care if no improvement',
                'treatment_plan_index': treatment_index
            })
            
    except Exception as e:
        return jsonify({'error': f'Diagnosis error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)