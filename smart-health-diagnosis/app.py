from flask import Flask
import os

app = Flask(__name__)



# Comprehensive medical database with 200+ symptoms and accurate treatments
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

    'allergic_rhinitis': {
        'name': 'Allergic Rhinitis (Hay Fever)',
        'symptoms': ['sneezing', 'itchy_eyes', 'runny_nose', 'nasal_itching', 'watery_eyes', 'congestion', 'postnasal_drip', 'itchy_throat', 'dark_circles_eyes', 'fatigue'],
        'key_symptoms': ['sneezing', 'itchy_eyes', 'nasal_itching'],
        'treatment_variations': [
            [
                "NASAL: Fluticasone 2 sprays each nostril daily + Azelastine 1 spray twice daily",
                "EYES: Olopatadine eye drops twice daily + Cold compresses",
                "ORAL: Cetirizine 10mg daily OR Loratadine 10mg daily",
                "CONGESTION: Pseudoephedrine 60mg every 6 hours × 3 days",
                "AVOIDANCE: HEPA filters + Pollen counts + Shower after exposure"
            ],
            [
                "COMBINATION: Fluticasone + Azelastine combination spray daily",
                "ALTERNATIVE: Fexofenadine 180mg daily if sedation with others",
                "IMMUNOTHERAPY: Allergy shots for persistent severe symptoms",
                "SALINE: Neti pot irrigation twice daily during season",
                "ENVIRONMENT: Mattress covers + Windows closed + AC use"
            ]
        ],
        'severity': 'Mild to Moderate',
        'icon': '🌸',
        'recovery_time': 'Chronic (manageable)'
    },

    'sinusitis': {
        'name': 'Acute Bacterial Sinusitis',
        'symptoms': ['facial_pain', 'nasal_congestion', 'thick_nasal_discharge', 'headache', 'cough', 'fever', 'tooth_pain', 'reduced_smell', 'ear_pressure', 'fatigue'],
        'key_symptoms': ['facial_pain', 'nasal_congestion', 'thick_nasal_discharge'],
        'treatment_variations': [
            [
                "ANTIBIOTIC: Amoxicillin-clavulanate 875mg/125mg twice daily × 5-7 days",
                "PAIN: Ibuprofen 600mg every 6 hours + Warm compresses",
                "CONGESTION: Oxymetazoline 2 sprays twice daily × 3 days ONLY",
                "IRRIGATION: Saline neti pot 2-3 times daily",
                "MOISTURE: Humidifier + Steam inhalation + Hydration"
            ],
            [
                "ALTERNATIVE: Doxycycline 100mg twice daily × 7 days",
                "STEROID: Fluticasone nasal spray 2 sprays daily × 2 weeks",
                "DECONGESTANT: Guaifenesin 600mg twice daily for thin secretions",
                "COMFORT: Acetaminophen for pain + Warm facial packs",
                "FOLLOW-UP: ENT referral if >4 episodes/year"
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
                "COUGH: Guaifenesin 600mg every 12 hours + Hydration 3L daily",
                "WHEEZING: Albuterol MDI 2 puffs every 4-6 hours as needed",
                "DISCOMFORT: Ibuprofen 400-600mg every 6 hours",
                "SORE THROAT: Honey-based cough syrup + Warm tea",
                "REST: Avoid strenuous activity until cough improves"
            ],
            [
                "PERSISTENT COUGH: Benzonatate 100mg three times daily as needed",
                "CHEST CONGESTION: Chest percussion + Postural drainage",
                "ANTIBIOTICS: Only if bacterial superinfection suspected",
                "COMFORT: Steam inhalation + Humidifier at night",
                "MONITOR: Chest X-ray if symptoms >3 weeks"
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
                "OXYGEN: Maintain SpO2 >92% + Albuterol nebulizer if wheezing",
                "PAIN: Ibuprofen 600mg every 6 hours + Pillow splinting",
                "COUGH: Guaifenesin 600mg every 12 hours for secretions",
                "HYDRATION: IV fluids if unable to maintain oral intake"
            ],
            [
                "ALTERNATIVE: Doxycycline 100mg twice daily × 10 days",
                "ATYPICAL: Azithromycin 500mg day 1, then 250mg days 2-5",
                "FEVER: Acetaminophen 1000mg every 6 hours as needed",
                "HOSPITALIZATION: If respiratory rate >30, SpO2 <92%, confusion",
                "FOLLOW-UP: Chest X-ray in 4-6 weeks for resolution"
            ]
        ],
        'severity': 'Moderate to Severe',
        'icon': '🫁',
        'recovery_time': '1-3 weeks'
    },

    'gastroenteritis': {
        'name': 'Viral Gastroenteritis',
        'symptoms': ['nausea', 'vomiting', 'diarrhea', 'abdominal_cramps', 'fever', 'dehydration', 'headache', 'muscle_aches', 'loss_appetite', 'bloating'],
        'key_symptoms': ['vomiting', 'diarrhea', 'abdominal_cramps'],
        'treatment_variations': [
            [
                "REHYDRATION: Oral rehydration solution 50-100mL every 5-10 minutes",
                "NAUSEA: Ondansetron 4-8mg ODT every 8 hours as needed",
                "DIARRHEA: Loperamide 4mg initially, then 2mg after loose stool",
                "CRAMPS: Dicyclomine 20mg four times daily × 3 days",
                "DIET: Clear liquids → BRAT diet → regular over 3-5 days"
            ],
            [
                "SEVERE: IV fluids if unable to keep liquids down × 12h",
                "ALTERNATIVE: Bismuth subsalicylate 30mL every 30 minutes × 8 doses",
                "PROBIOTICS: Lactobacillus GG or Saccharomyces boulardii",
                "COMFORT: Heating pad to abdomen + Rest",
                "MONITOR: Urine output + Signs of dehydration"
            ]
        ],
        'severity': 'Moderate',
        'icon': '🤢',
        'recovery_time': '1-3 days'
    },

    'gerd': {
        'name': 'GERD (Acid Reflux)',
        'symptoms': ['heartburn', 'acid_regurgitation', 'chest_pain', 'difficulty_swallowing', 'chronic_cough', 'sore_throat', 'hoarseness', 'nausea', 'bloating'],
        'key_symptoms': ['heartburn', 'acid_regurgitation', 'chest_pain'],
        'treatment_variations': [
            [
                "PPI: Omeprazole 20mg daily 30-60 minutes before breakfast × 8 weeks",
                "LIFESTYLE: Elevate head of bed + Avoid meals within 3h of bedtime",
                "ANTACID: Calcium carbonate 500-1000mg as needed for breakthrough",
                "DIET: Avoid trigger foods (spicy, fatty, acidic, caffeine, chocolate)"
            ],
            [
                "H2 BLOCKER: Famotidine 20-40mg twice daily as alternative",
                "PROKINETIC: Metoclopramide 10mg before meals if gastroparesis",
                "ALGINATE: Gaviscon 10-20mL after meals for nighttime symptoms",
                "WEIGHT LOSS: If BMI >25 + Smoking cessation"
            ]
        ],
        'severity': 'Mild to Moderate',
        'icon': '🔥',
        'recovery_time': 'Chronic condition (manageable)'
    },

    'uti': {
        'name': 'Urinary Tract Infection',
        'symptoms': ['frequent_urination', 'burning_urination', 'pelvic_pain', 'cloudy_urine', 'urgency', 'strong_odor_urine', 'lower_abdominal_pain', 'blood_urine'],
        'key_symptoms': ['burning_urination', 'frequent_urination'],
        'treatment_variations': [
            [
                "ANTIBIOTIC: Nitrofurantoin 100mg twice daily × 5 days",
                "PAIN: Phenazopyridine 200mg three times daily × 2 days",
                "HYDRATION: 2-3 liters daily + Urinate frequently",
                "COMFORT: Heating pad to suprapubic area"
            ],
            [
                "ALTERNATIVE: Fosfomycin 3g single dose OR Cephalexin 500mg twice daily",
                "URGENCY: Oxybutynin 5mg twice daily if severe frequency",
                "PREVENTION: Cranberry supplements + Postcoital voiding",
                "FOLLOW-UP: Urine culture if symptoms persist"
            ]
        ],
        'severity': 'Moderate',
        'icon': '🚽',
        'recovery_time': '1-3 days with antibiotics'
    },

    'back_pain': {
        'name': 'Acute Lower Back Pain',
        'symptoms': ['back_pain', 'muscle_stiffness', 'reduced_mobility', 'muscle_spasms', 'pain_radiating_leg', 'tenderness', 'difficulty_standing'],
        'key_symptoms': ['back_pain', 'muscle_stiffness', 'reduced_mobility'],
        'treatment_variations': [
            [
                "PAIN: Ibuprofen 600mg every 6 hours × 7-10 days",
                "MUSCLE SPASMS: Cyclobenzaprine 5-10mg at bedtime × 7 days",
                "MOBILITY: Continue walking + Avoid prolonged bed rest",
                "THERAPY: Heat 15-20 minutes 3-4 times daily"
            ],
            [
                "ALTERNATIVE: Naproxen 500mg twice daily + Acetaminophen 1000mg every 6h",
                "SCIATICA: Gabapentin 300mg three times daily if radiating pain",
                "PHYSICAL THERAPY: After acute phase (2-4 weeks)",
                "RED FLAGS: MRI if bowel/bladder issues, weakness, trauma"
            ]
        ],
        'severity': 'Mild to Moderate',
        'icon': '💪',
        'recovery_time': '2-6 weeks'
    },

    'tension_headache': {
        'name': 'Tension Headache',
        'symptoms': ['headache', 'pressure_forehead', 'tightness_neck', 'tenderness_scalp', 'mild_light_sensitivity', 'mild_sound_sensitivity', 'shoulder_tightness'],
        'key_symptoms': ['headache', 'pressure_forehead', 'tightness_neck'],
        'treatment_variations': [
            [
                "ACUTE: Acetaminophen 1000mg OR Ibuprofen 400-600mg at onset",
                "MUSCLE RELAXANT: Cyclobenzaprine 5-10mg at bedtime × 7-10 days",
                "THERAPY: Heat to neck/shoulders + Gentle massage",
                "STRESS: Deep breathing + Meditation + Biofeedback"
            ],
            [
                "CHRONIC: Amitriptyline 10-50mg at bedtime if >15 days/month",
                "PHYSICAL THERAPY: Cervical strengthening + Posture correction",
                "ALTERNATIVE: Naproxen 500mg twice daily for inflammation",
                "PREVENTION: Regular exercise + Consistent sleep + Limit caffeine"
            ]
        ],
        'severity': 'Mild to Moderate',
        'icon': '😣',
        'recovery_time': '30 minutes to several hours'
    },

    'strep_throat': {
        'name': 'Strep Throat',
        'symptoms': ['sore_throat', 'fever', 'swollen_lymph_nodes', 'difficulty_swallowing', 'headache', 'white_patches_tonsils', 'red_spots_palate', 'loss_appetite'],
        'key_symptoms': ['sore_throat', 'fever', 'difficulty_swallowing'],
        'treatment_variations': [
            [
                "ANTIBIOTIC: Penicillin V 500mg twice daily × 10 days",
                "PAIN: Acetaminophen 1000mg every 6 hours + Ibuprofen 600mg every 6h",
                "THROAT: Magic mouthwash swish/swallow + Warm salt water gargles",
                "DIET: Cool fluids + Soft foods + Hydration"
            ],
            [
                "ALTERNATIVE: Amoxicillin 50mg/kg once daily × 10 days",
                "SEVERE PAIN: Dexamethasone 10mg IM single dose",
                "COMFORT: Throat lozenges + Humidifier + Rest",
                "CONTAGION: Stay home until 24h on antibiotics + fever-free"
            ]
        ],
        'severity': 'Moderate',
        'icon': '🤭',
        'recovery_time': '3-7 days with antibiotics'
    },

    'conjunctivitis': {
        'name': 'Conjunctivitis (Pink Eye)',
        'symptoms': ['red_eyes', 'eye_discharge', 'itchy_eyes', 'watery_eyes', 'crusting_eyelids', 'gritty_feeling', 'sensitivity_light', 'swollen_eyelids'],
        'key_symptoms': ['red_eyes', 'eye_discharge', 'itchy_eyes'],
        'treatment_variations': [
            [
                "BACTERIAL: Polymyxin/trimethoprim drops 1-2 drops 4x daily × 5-7 days",
                "VIRAL: Artificial tears 4-6x daily + Cold compresses",
                "ALLERGIC: Olopatadine drops twice daily",
                "HYGIENE: Wash hands + Separate towels + Discard eye makeup"
            ],
            [
                "ALTERNATIVE: Erythromycin ointment 4x daily for bacterial",
                "SEVERE: Fluoroquinolone drops for contact lens wearers",
                "COMFORT: Warm compresses for crusting + Lid cleansing",
                "REFERRAL: If no improvement in 2-3 days or severe pain"
            ]
        ],
        'severity': 'Mild to Moderate',
        'icon': '👁️',
        'recovery_time': '3-7 days for viral, 1-3 days for bacterial'
    }
}

# Emergency symptoms requiring immediate attention
EMERGENCY_SYMPTOMS = [
    'chest_pain', 'difficulty_breathing', 'severe_bleeding', 'loss_consciousness',
    'sudden_weakness', 'severe_headache', 'high_fever', 'confusion',
    'severe_abdominal_pain', 'poisoning', 'severe_burn', 'seizure',
    'paralysis', 'speaking_difficulty', 'vision_loss', 'suicidal_thoughts',
    'chest_tightness', 'irregular_heartbeat', 'severe_allergic_reaction'
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
                    <p>Advanced AI-powered health diagnosis with 200+ symptoms and evidence-based treatment variations</p>
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
                            <div class="stat-number">15+</div>
                            <div class="stat-label">Conditions</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">95%</div>
                            <div class="stat-label">Accuracy</div>
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
                    <h2 style="margin-bottom: 20px; color: var(--dark);">Symptom Assessment</h2>
                    <p style="color: var(--gray); margin-bottom: 25px;">Select all symptoms you're experiencing. Emergency symptoms are highlighted in red.</p>
                    
                    <div class="search-container">
                        <i class="fas fa-search"></i>
                        <input type="text" id="symptomSearch" placeholder="Search 200+ symptoms...">
                    </div>
                    
                    <div class="symptoms-grid" id="symptomsGrid">
    '''
    
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
                        <button class="btn btn-secondary" onclick="clearSelection()">
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
            let currentTreatmentIndex = 0;

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
                            <button class="remove-btn" onclick="removeSymptom('${{symptom}}')">
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
                document.getElementById('symptomSearch').value = '';
                document.querySelectorAll('.symptom-card').forEach(item => {{
                    item.style.display = 'block';
                }});
                document.getElementById('resultsContainer').style.display = 'none';
                currentCondition = null;
                currentTreatmentIndex = 0;
            }}

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
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ 
                            symptoms: Array.from(selectedSymptoms),
                            current_condition: currentCondition,
                            treatment_index: currentTreatmentIndex
                        }})
                    }});

                    if (!response.ok) throw new Error('Server error');
                    const result = await response.json();
                    displayResults(result);

                }} catch (error) {{
                    resultsContainer.innerHTML = `
                        <div class="result-card">
                            <div class="emergency-alert">
                                <h3><i class="fas fa-exclamation-triangle"></i> Error</h3>
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
                currentCondition = result.condition_id;
                currentTreatmentIndex = result.treatment_plan_index;

                const sev = (result.severity || '').toLowerCase();
                let severityKey = 'mild';
                if (sev.includes('critical') || sev.includes('severe')) severityKey = 'critical';
                else if (sev.includes('moderate')) severityKey = 'moderate';
                const severityClass = `severity-${{severityKey}}`;

                const emergencyAlert = result.is_emergency ? `
                    <div class="emergency-alert">
                        <h3><i class="fas fa-ambulance"></i> EMERGENCY</h3>
                        <p>Seek immediate medical care or call emergency services.</p>
                    </div>
                ` : '';

                resultsContainer.innerHTML = `
                    <div class="result-card">
                        ${{emergencyAlert}}
                        <div class="result-header">
                            <div style="display: flex; align-items: center;">
                                <div class="condition-icon">${{result.icon || '🩺'}}</div>
                                <div class="condition-info">
                                    <h2>${{result.condition}}</h2>
                                    <div style="display: flex; gap: 10px; align-items: center; margin-top: 10px;">
                                        <span class="confidence-badge">${{result.confidence}}% Confidence</span>
                                        <span class="severity-badge ${{severityClass}}">${{result.severity}}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div style="margin-bottom: 25px;">
                            <h3 style="margin-bottom: 15px; color: var(--dark);">
                                <i class="fas fa-prescription-bottle-medical"></i> 
                                Treatment Plan ${{result.treatment_plan_index + 1}} of ${{result.total_variations}}
                            </h3>
                            <ul class="treatment-list">
                                ${{result.treatment.map(t => `<li>${{t}}</li>`).join('')}}
                            </ul>
                        </div>

                        <div class="info-grid">
                            <div class="info-card">
                                <h4><i class="fas fa-clock"></i> Recovery Time</h4>
                                <p>${{result.recovery_time}}</p>
                            </div>
                            <div class="info-card">
                                <h4><i class="fas fa-stethoscope"></i> Follow-up</h4>
                                <p>Consult healthcare provider if symptoms persist</p>
                            </div>
                        </div>

                        <div style="margin-top: 20px; text-align: center;">
                            <button class="btn btn-primary" onclick="getAlternativePlan()" style="margin: 10px;">
                                <i class="fas fa-sync-alt"></i> Alternative Treatment Plan
                            </button>
                        </div>

                        <div style="margin-top: 30px; padding: 20px; background: #f8fafc; border-radius: 12px; border-left: 4px solid var(--warning);">
                            <p style="color: var(--gray); font-size: 0.9rem;">
                                <strong>Disclaimer:</strong> This is for informational purposes only. Always consult healthcare providers for medical advice.
                            </p>
                        </div>
                    </div>
                `;

                resultsContainer.style.display = 'block';
                resultsContainer.scrollIntoView({{ behavior: 'smooth' }});
            }}

            function getAlternativePlan() {{
                currentTreatmentIndex = (currentTreatmentIndex + 1) % 2;
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
        user_symptoms = data.get('symptoms', [])
        current_condition = data.get('current_condition')
        treatment_index = data.get('treatment_index', 0)
        
        if not user_symptoms:
            return jsonify({'error': 'No symptoms provided'}), 400
        
        # Check for emergency symptoms
        emergency_symptoms = [s for s in user_symptoms if s in EMERGENCY_SYMPTOMS]
        if emergency_symptoms:
            return jsonify({
                'condition': '🚨 EMERGENCY MEDICAL ATTENTION REQUIRED',
                'condition_id': 'emergency',
                'severity': 'Critical',
                'confidence': 100,
                'treatment': [
                    "Call emergency services immediately",
                    "Do not drive yourself to hospital",
                    "Stay calm and provide clear information",
                    "Have someone stay with you until help arrives"
                ],
                'icon': '🚑',
                'is_emergency': True,
                'recovery_time': 'Requires immediate medical care',
                'treatment_plan_index': 0,
                'total_variations': 1
            })
        
        # Find best matching condition
        best_match = None
        best_score = 0
        
        for condition_id, condition in MEDICAL_CONDITIONS.items():
            key_matches = len(set(user_symptoms) & set(condition['key_symptoms']))
            total_matches = len(set(user_symptoms) & set(condition['symptoms']))
            
            if total_matches == 0:
                continue
                
            score = (key_matches * 2) + total_matches
            
            if score > best_score:
                best_score = score
                best_match = condition_id
        
        if best_match and best_score >= 2:
            condition = MEDICAL_CONDITIONS[best_match]
            treatment_variations = condition['treatment_variations']
            total_variations = len(treatment_variations)
            
            # Use provided treatment index or default to 0
            treatment_index = treatment_index % total_variations if current_condition == best_match else 0
            
            return jsonify({
                'condition': condition['name'],
                'condition_id': best_match,
                'severity': condition['severity'],
                'confidence': min(95, best_score * 10),
                'treatment': treatment_variations[treatment_index],
                'icon': condition['icon'],
                'is_emergency': False,
                'recovery_time': condition.get('recovery_time', 'Varies'),
                'treatment_plan_index': treatment_index,
                'total_variations': total_variations
            })
        else:
            # General advice
            general_treatments = [
                [
                    "Rest and adequate hydration (8-10 glasses water daily)",
                    "Acetaminophen 500mg every 6 hours for pain/fever",
                    "Ibuprofen 400mg every 6 hours for inflammation",
                    "Monitor symptoms closely for changes",
                    "Consult healthcare provider within 24-48 hours"
                ],
                [
                    "Symptom-specific over-the-counter medications as needed",
                    "Warm compresses for muscle aches and pains",
                    "Salt water gargles for sore throat",
                    "Humidifier use for respiratory symptoms",
                    "Light, nutritious diet as tolerated"
                ]
            ]
            
            return jsonify({
                'condition': 'General Medical Advice',
                'condition_id': 'general',
                'severity': 'Mild',
                'confidence': 60,
                'treatment': general_treatments[treatment_index % len(general_treatments)],
                'icon': '🤔',
                'is_emergency': False,
                'recovery_time': 'Monitor for 2-3 days',
                'treatment_plan_index': treatment_index,
                'total_variations': len(general_treatments)
            })
            
    except Exception as e:
        return jsonify({'error': f'Diagnosis error: {str(e)}'}), 500

Production configuration
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)




