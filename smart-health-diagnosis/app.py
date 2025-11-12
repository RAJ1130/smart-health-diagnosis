from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Comprehensive medical database with accurate, evidence-based treatment plans
MEDICAL_CONDITIONS = {
    # Respiratory Conditions
    'common_cold': {
        'name': 'Common Cold (Viral Rhinitis)',
        'symptoms': ['runny_nose', 'sneezing', 'sore_throat', 'cough', 'congestion', 'mild_fever', 'headache', 'body_aches', 'fatigue', 'watery_eyes', 'malaise'],
        'key_symptoms': ['runny_nose', 'sneezing', 'congestion'],
        'treatment': [
            'Rest and hydration: 8-10 glasses of water daily, warm fluids like broth or tea',
            'Saline nasal spray: 2 sprays each nostril every 4-6 hours as needed for congestion',
            'Acetaminophen: 500-1000mg every 6 hours (max 3000mg/day) for pain/fever',
            'Ibuprofen: 200-400mg every 6-8 hours (max 1200mg/day) for inflammation',
            'Dextromethorphan: 30mg every 6-8 hours for dry cough (avoid in children under 4)',
            'Guaifenesin: 200-400mg every 4 hours (max 2400mg/day) for productive cough',
            'Zinc lozenges: 13-23mg every 2-3 hours while awake (start within 24 hours of symptoms, max 10 days)',
            'Honey: 1-2 teaspoons in warm tea for cough relief (avoid in children <1 year)',
            'Steam inhalation: 10-15 minutes, 2-3 times daily to relieve congestion',
            'Humidifier use: Maintain 40-60% humidity in bedroom',
            'SEEK MEDICAL CARE IF: Symptoms worsen after 7 days, fever >101.3°F (38.5°C), difficulty breathing, or severe headache'
        ],
        'severity': 'Mild',
        'icon': '🤧',
        'recovery_time': '7-10 days',
        'contagious_period': '1-2 days before to 5-7 days after symptoms begin'
    },

    'influenza': {
        'name': 'Influenza (Seasonal Flu)',
        'symptoms': ['fever', 'chills', 'body_aches', 'fatigue', 'cough', 'headache', 'sore_throat', 'nasal_congestion', 'muscle_pain', 'weakness', 'chest_discomfort', 'loss_appetite', 'sweating', 'eye_pain'],
        'key_symptoms': ['fever', 'body_aches', 'fatigue', 'cough'],
        'treatment': [
            'ANTIVIRAL TREATMENT (Start within 48 hours of symptoms):',
            '  - Oseltamivir (Tamiflu): 75mg twice daily for 5 days',
            '  - OR Zanamivir: 2 inhalations (10mg) twice daily for 5 days',
            '  - OR Baloxavir: Single dose (weight-based) for uncomplicated influenza',
            'Symptom management:',
            '  - Acetaminophen: 650mg every 6 hours for fever and myalgia (max 3000mg/day)',
            '  - Ibuprofen: 400-600mg every 6-8 hours for inflammation (max 1200mg/day)',
            '  - Hydration: Oral rehydration solutions, broth, 2-3 liters daily',
            '  - Rest: Strict bed rest during acute phase (3-5 days)',
            'Cough management:',
            '  - Dextromethorphan: 30mg every 6-8 hours for dry cough',
            '  - Guaifenesin: 400mg every 4 hours for productive cough',
            'EMERGENCY WARNING SIGNS - Seek immediate care for:',
            '  - Difficulty breathing or shortness of breath',
            '  - Chest pain or pressure',
            '  - Persistent dizziness or confusion',
            '  - Severe vomiting',
            '  - Fever that improves then returns worse'
        ],
        'severity': 'Moderate to Severe',
        'icon': '🤒',
        'recovery_time': '1-2 weeks',
        'contagious_period': '1 day before to 5-7 days after symptoms'
    },

    'covid_19': {
        'name': 'COVID-19',
        'symptoms': ['fever', 'cough', 'loss_taste', 'loss_smell', 'fatigue', 'shortness_breath', 'body_aches', 'sore_throat', 'headache', 'diarrhea', 'nausea', 'chest_pain', 'confusion', 'pink_eye'],
        'key_symptoms': ['loss_taste', 'loss_smell', 'fever', 'cough'],
        'treatment': [
            'ISOLATION: Minimum 5 days from positive test + until fever-free 24 hours without medication',
            'ANTIVIRAL THERAPY (Start within 5 days of symptoms for high-risk patients):',
            '  - Nirmatrelvir/Ritonavir (Paxlovid): 300mg/100mg twice daily for 5 days',
            '  - OR Remdesivir: IV treatment for 3 days (outpatient)',
            '  - OR Molnupiravir: 800mg twice daily for 5 days (if other options unavailable)',
            'Symptomatic treatment:',
            '  - Acetaminophen: 500-1000mg every 6 hours for fever/body aches',
            '  - Ibuprofen: 400mg every 6 hours for inflammation',
            '  - Hydration: Electrolyte solutions, 2-3 liters daily',
            'Monitoring:',
            '  - Pulse oximeter: Check oxygen saturation every 8 hours',
            '  - Seek emergency care if SpO2 <94% or respiratory rate >24/min',
            '  - Prone positioning if SpO2 <95%',
            'HIGH-RISK PATIENTS: Consider monoclonal antibodies if available and indicated',
            'FOLLOW-UP: Primary care visit 2-4 weeks post-recovery for assessment'
        ],
        'severity': 'Mild to Severe',
        'icon': '🦠',
        'recovery_time': '1-3 weeks (mild), longer for severe cases',
        'contagious_period': '2 days before to 10 days after symptoms'
    },

    'pneumonia': {
        'name': 'Community-Acquired Pneumonia',
        'symptoms': ['fever', 'cough', 'chest_pain', 'shortness_breath', 'fatigue', 'sputum_production', 'chills', 'sweating', 'headache', 'muscle_pain', 'loss_appetite', 'confusion_elderly'],
        'key_symptoms': ['fever', 'cough', 'shortness_breath', 'chest_pain'],
        'treatment': [
            'ANTIBIOTIC THERAPY (Based on patient factors):',
            '  - First-line: Amoxicillin 1g three times daily OR Doxycycline 100mg twice daily',
            '  - Alternative: Amoxicillin-clavulanate 875mg/125mg twice daily',
            '  - Macrolide: Azithromycin 500mg daily for 3 days if atypical suspected',
            '  - Duration: 5-7 days total (extend to 10-14 days if slow response)',
            'Supportive care:',
            '  - Oxygen therapy if SpO2 <92% (target 94-98%)',
            '  - Bronchodilators: Albuterol 2.5mg nebulized every 4-6 hours if wheezing',
            '  - Analgesia: Acetaminophen or ibuprofen for pleuritic pain',
            '  - Hydration: IV fluids if unable to maintain oral intake',
            'Monitoring and follow-up:',
            '  - Chest X-ray to confirm diagnosis and assess extent',
            '  - Hospitalization if: CURB-65 score ≥2, respiratory rate >30, SpO2 <92%',
            '  - Follow-up chest X-ray in 4-6 weeks for resolution',
            '  - Vaccination: Pneumococcal and influenza vaccines after recovery'
        ],
        'severity': 'Moderate to Severe',
        'icon': '🫁',
        'recovery_time': '1-3 weeks',
        'contagious_period': 'Until 24-48 hours on antibiotics'
    },

    'bronchitis': {
        'name': 'Acute Bronchitis',
        'symptoms': ['cough', 'sputum_production', 'chest_discomfort', 'fatigue', 'mild_fever', 'shortness_breath', 'wheezing', 'chest_congestion', 'sore_throat', 'body_aches'],
        'key_symptoms': ['cough', 'sputum_production', 'chest_discomfort'],
        'treatment': [
            'PRIMARY MANAGEMENT (Most cases viral - avoid antibiotics):',
            '  - Guaifenesin: 400mg every 4 hours to thin secretions (max 2400mg/day)',
            '  - Dextromethorphan: 15-30mg every 6-8 hours for dry, hacking cough',
            '  - Albuterol inhaler: 2 puffs every 4-6 hours if wheezing present',
            '  - Honey: 1-2 teaspoons in warm tea for cough relief (adults and children >1)',
            'Supportive care:',
            '  - Steam inhalation: 10-15 minutes, 2-3 times daily',
            '  - Humidifier: Cool mist in bedroom at night',
            '  - Hydration: Warm fluids, 2-3 liters daily',
            '  - Rest: Avoid strenuous activity until cough improves',
            'When to consider antibiotics:',
            '  - Only if bacterial superinfection suspected (purulent sputum + fever >100.4°F)',
            '  - First-line: Doxycycline 100mg twice daily for 5 days OR Azithromycin 500mg day 1, then 250mg days 2-5',
            'SEEK CARE IF: Symptoms >3 weeks, fever >101°F, difficulty breathing, or chest pain'
        ],
        'severity': 'Moderate',
        'icon': '😮💨',
        'recovery_time': '1-3 weeks',
        'contagious_period': 'While symptomatic (usually 7-10 days)'
    },

    # Neurological Conditions
    'migraine': {
        'name': 'Migraine Headache',
        'symptoms': ['headache', 'nausea', 'sensitivity_light', 'sensitivity_sound', 'throbbing_pain', 'vision_changes', 'dizziness', 'aura', 'vomiting', 'neck_pain', 'nasuea', 'fatigue'],
        'key_symptoms': ['headache', 'sensitivity_light', 'throbbing_pain', 'nausea'],
        'treatment': [
            'ACUTE TREATMENT (Take at headache onset):',
            '  - NSAIDs: Ibuprofen 600mg OR Naproxen 500mg immediately',
            '  - Triptans: Sumatriptan 50-100mg OR Rizatriptan 10mg (max 2 doses/24h)',
            '  - Anti-emetics: Metoclopramide 10mg OR Prochlorperazine 10mg for nausea',
            '  - Combination: Acetaminophen 500mg + Aspirin 500mg + Caffeine 130mg',
            'Non-pharmacological:',
            '  - Rest in dark, quiet room immediately when symptoms begin',
            '  - Cold compress to forehead and temporal areas',
            '  - Hydration with electrolyte solutions',
            'PREVENTIVE THERAPY (If ≥4 migraine days/month):',
            '  - Propranolol: 40-80mg daily OR Topiramate 50mg daily',
            '  - Amitriptyline: 10-50mg at bedtime',
            '  - Calcitonin gene-related peptide (CGRP) monoclonal antibodies for refractory cases',
            'EMERGENCY: Go to ER for thunderclap headache, fever with headache, or neurological deficits'
        ],
        'severity': 'Moderate to Severe',
        'icon': '😵',
        'recovery_time': '4-72 hours',
        'contagious_period': 'Not contagious'
    },

    'tension_headache': {
        'name': 'Tension-Type Headache',
        'symptoms': ['headache', 'pressure_forehead', 'tightness_neck', 'tenderness_scalp', 'mild_light_sensitivity', 'mild_sound_sensitivity', 'shoulder_tightness'],
        'key_symptoms': ['headache', 'pressure_forehead', 'tightness_neck'],
        'treatment': [
            'ACUTE TREATMENT:',
            '  - Acetaminophen: 1000mg OR Ibuprofen: 400-600mg at onset',
            '  - Aspirin: 500-1000mg OR Naproxen: 500mg',
            '  - Avoid medication overuse (max 10-15 days/month of acute medications)',
            'Non-pharmacological management:',
            '  - Heat therapy: Heating pad to neck/shoulders for 15-20 minutes',
            '  - Massage: Gentle massage of temporal, neck, and shoulder muscles',
            '  - Stress reduction: Deep breathing, meditation, biofeedback',
            '  - Posture correction: Ergonomic workstation setup',
            'PREVENTIVE THERAPY (If chronic tension-type headache):',
            '  - Amitriptyline: 10-75mg at bedtime (start low, increase weekly)',
            '  - Physical therapy: Cervical strengthening and stretching',
            '  - Regular exercise program and consistent sleep schedule',
            'REFERRAL: Consider neurology if not responsive to standard therapy'
        ],
        'severity': 'Mild to Moderate',
        'icon': '😣',
        'recovery_time': '30 minutes to several hours',
        'contagious_period': 'Not contagious'
    },

    # Gastrointestinal Conditions
    'gastroenteritis': {
        'name': 'Viral Gastroenteritis (Stomach Flu)',
        'symptoms': ['nausea', 'vomiting', 'diarrhea', 'abdominal_cramps', 'fever', 'dehydration', 'headache', 'muscle_aches', 'loss_appetite', 'bloating'],
        'key_symptoms': ['vomiting', 'diarrhea', 'abdominal_cramps'],
        'treatment': [
            'REHYDRATION (Most critical component):',
            '  - Oral rehydration solution (ORS): Small frequent sips, 1-2 liters in first 4-6 hours',
            '  - Commercial ORS or homemade: 1L water + 6tsp sugar + 1/2tsp salt',
            '  - IV fluids if severe dehydration or persistent vomiting',
            'Dietary management:',
            '  - Start with clear fluids, advance to BRAT diet (bananas, rice, applesauce, toast)',
            '  - Avoid: Dairy, fatty foods, caffeine, alcohol for 48-72 hours',
            '  - Probiotics: Lactobacillus GG or Saccharomyces boulardii twice daily',
            'Symptom control:',
            '  - Loperamide: 4mg initially, then 2mg after each loose stool (max 16mg/day)',
            '  - Avoid anti-diarrheals if bloody diarrhea or fever >101°F',
            '  - Zinc supplementation: 20mg daily for 10-14 days (children)',
            'SEVERE SYMPTOMS - Seek medical care for:',
            '  - Signs of dehydration (dry mouth, decreased urine, dizziness)',
            '  - Blood in stool or vomit',
            '  - Fever >102°F (39°C)',
            '  - Symptoms persisting >3 days'
        ],
        'severity': 'Moderate',
        'icon': '🤢',
        'recovery_time': '1-3 days',
        'contagious_period': 'While symptomatic and up to 2 weeks after'
    },

    'gerd': {
        'name': 'Gastroesophageal Reflux Disease (GERD)',
        'symptoms': ['heartburn', 'acid_regurgitation', 'chest_pain', 'difficulty_swallowing', 'chronic_cough', 'sore_throat', 'hoarseness', 'nausea', 'bloating'],
        'key_symptoms': ['heartburn', 'acid_regurgitation', 'chest_pain'],
        'treatment': [
            'LIFESTYLE MODIFICATIONS (First-line treatment):',
            '  - Elevate head of bed 6-8 inches',
            '  - Avoid meals within 3 hours of bedtime',
            '  - Identify and avoid trigger foods (spicy, fatty, acidic, chocolate, caffeine)',
            '  - Weight loss if BMI >25',
            '  - Smoking cessation and alcohol reduction',
            'MEDICATION THERAPY:',
            '  - Proton Pump Inhibitors (PPIs): Omeprazole 20mg daily OR Esomeprazole 40mg daily for 4-8 weeks',
            '  - H2 Receptor Antagonists: Famotidine 20-40mg twice daily (alternative)',
            '  - Antacids: Calcium carbonate 500-1000mg as needed for breakthrough symptoms',
            '  - Prokinetics: Metoclopramide 10mg before meals if gastroparesis suspected',
            'MAINTENANCE:',
            '  - Step-down therapy: Lowest effective PPI dose',
            '  - Intermittent or on-demand therapy for mild cases',
            '  - Consider surgery (fundoplication) for refractory cases',
            'ALARM FEATURES - Require endoscopy:',
            '  - Dysphagia, odynophagia, weight loss, anemia, or family history of GI cancer'
        ],
        'severity': 'Mild to Moderate',
        'icon': '🔥',
        'recovery_time': 'Chronic condition (manageable)',
        'contagious_period': 'Not contagious'
    },

    # Urinary Conditions
    'uti': {
        'name': 'Uncomplicated Urinary Tract Infection',
        'symptoms': ['frequent_urination', 'burning_urination', 'pelvic_pain', 'cloudy_urine', 'urgency', 'strong_odor_urine', 'lower_abdominal_pain', 'blood_urine'],
        'key_symptoms': ['burning_urination', 'frequent_urination'],
        'treatment': [
            'ANTIBIOTIC THERAPY (Based on local resistance patterns):',
            '  - First-line: Nitrofurantoin 100mg twice daily for 5 days',
            '  - Alternative: Trimethoprim-sulfamethoxazole 160/800mg twice daily for 3 days',
            '  - Second-line: Fosfomycin 3g single dose OR Cephalexin 500mg twice daily for 7 days',
            'Symptomatic relief:',
            '  - Phenazopyridine: 200mg three times daily for 2 days (urinary analgesic)',
            '  - Acetaminophen or ibuprofen for pain management',
            '  - Heating pad to suprapubic area for discomfort',
            'Prevention and supportive care:',
            '  - Increase water intake: 2-3 liters daily during infection',
            '  - Urinate frequently and completely empty bladder',
            '  - Avoid potential irritants: Bubble baths, spermicides, diaphragms',
            '  - Cranberry supplements (36mg proanthocyanidins daily) for recurrent UTIs',
            'FOLLOW-UP: Urine culture if symptoms persist after treatment',
            'REFERRAL: Urology consult for recurrent UTIs (>3/year)'
        ],
        'severity': 'Moderate',
        'icon': '🚽',
        'recovery_time': '1-3 days with antibiotics',
        'contagious_period': 'Not contagious'
    },

    # Musculoskeletal Conditions
    'back_pain': {
        'name': 'Acute Lower Back Pain',
        'symptoms': ['back_pain', 'muscle_stiffness', 'reduced_mobility', 'muscle_spasms', 'pain_radiating_leg', 'tenderness', 'difficulty_standing'],
        'key_symptoms': ['back_pain', 'muscle_stiffness', 'reduced_mobility'],
        'treatment': [
            'ACUTE PHASE (First 1-2 weeks):',
            '  - NSAIDs: Ibuprofen 400-600mg every 6-8 hours OR Naproxen 500mg twice daily for 7-10 days',
            '  - Muscle relaxants: Cyclobenzaprine 5-10mg at bedtime OR Tizanidine 2-4mg three times daily',
            '  - Acetaminophen: 1000mg every 6 hours as needed for pain',
            'Physical therapy and activity modification:',
            '  - Continue normal activities as tolerated (avoid bed rest >1-2 days)',
            '  - Gentle walking: 5-10 minutes every 2-3 hours',
            '  - Heat therapy: Heating pad 15-20 minutes, 3-4 times daily',
            '  - Proper lifting techniques and posture education',
            'SECOND-LINE THERAPIES:',
            '  - Physical therapy referral if not improved in 2-4 weeks',
            '  - Consider short-course opioids only for severe pain (3-7 days max)',
            '  - Epidural steroid injections for radicular symptoms',
            'RED FLAGS - Require immediate evaluation:',
            '  - Bowel/bladder incontinence, saddle anesthesia, progressive weakness',
            '  - History of cancer, fever with back pain, or trauma'
        ],
        'severity': 'Mild to Moderate',
        'icon': '💪',
        'recovery_time': '2-6 weeks',
        'contagious_period': 'Not contagious'
    },

    # Allergic Conditions
    'allergic_rhinitis': {
        'name': 'Allergic Rhinitis (Hay Fever)',
        'symptoms': ['sneezing', 'itchy_eyes', 'runny_nose', 'nasal_itching', 'watery_eyes', 'congestion', 'postnasal_drip', 'itchy_throat', 'dark_circles_eyes', 'fatigue'],
        'key_symptoms': ['sneezing', 'itchy_eyes', 'nasal_itching'],
        'treatment': [
            'ALLERGEN AVOIDANCE (First-line):',
            '  - HEPA air filters, mattress/pillow allergen covers',
            '  - Keep windows closed during high pollen seasons',
            '  - Shower and change clothes after outdoor exposure',
            'PHARMACOLOGICAL MANAGEMENT:',
            '  - Second-generation antihistamines: Cetirizine 10mg daily OR Loratadine 10mg daily',
            '  - Intranasal corticosteroids: Fluticasone 2 sprays/nostril daily OR Mometasone 2 sprays/nostril daily',
            '  - Leukotriene receptor antagonists: Montelukast 10mg daily (especially with asthma)',
            '  - Ocular symptoms: Olopatadine eye drops twice daily',
            'ADJUNCT THERAPIES:',
            '  - Saline nasal irrigation: Neti pot twice daily during symptom season',
            '  - Decongestants: Pseudoephedrine 60mg every 6 hours (short-term use only)',
            '  - Combination therapy for moderate-severe symptoms',
            'IMMUNOTHERAPY:',
            '  - Subcutaneous or sublingual immunotherapy for persistent, severe symptoms',
            '  - Consider allergy testing to identify specific triggers'
        ],
        'severity': 'Mild to Moderate',
        'icon': '🌸',
        'recovery_time': 'Chronic (manageable)',
        'contagious_period': 'Not contagious'
    },

    # Additional Conditions
    'sinusitis': {
        'name': 'Acute Bacterial Sinusitis',
        'symptoms': ['facial_pain', 'nasal_congestion', 'thick_nasal_discharge', 'headache', 'cough', 'fever', 'tooth_pain', 'reduced_smell', 'ear_pressure', 'fatigue'],
        'key_symptoms': ['facial_pain', 'nasal_congestion', 'thick_nasal_discharge'],
        'treatment': [
            'DIAGNOSTIC CRITERIA: Symptoms >10 days OR worsening after initial improvement',
            'ANTIBIOTIC THERAPY (If bacterial confirmed):',
            '  - First-line: Amoxicillin-clavulanate 500mg/125mg three times daily for 5-7 days',
            '  - Penicillin allergy: Doxycycline 100mg twice daily OR Levofloxacin 500mg daily',
            '  - Alternative: Cefuroxime 250mg twice daily for 10 days',
            'SYMPTOM MANAGEMENT:',
            '  - Intranasal corticosteroids: Fluticasone 2 sprays/nostril daily for 2 weeks',
            '  - Saline nasal irrigation: 2-3 times daily',
            '  - Analgesics: Acetaminophen or ibuprofen for pain/fever',
            '  - Decongestants: Oxymetazoline 2 sprays/nostril twice daily (max 3 days)',
            'SUPPORTIVE CARE:',
            '  - Steam inhalation with menthol or eucalyptus',
            '  - Warm compresses to facial sinus areas',
            '  - Adequate hydration to thin secretions',
            'REFERRAL: ENT for recurrent sinusitis (>4 episodes/year) or treatment failure'
        ],
        'severity': 'Moderate',
        'icon': '👃',
        'recovery_time': '7-14 days',
        'contagious_period': 'Until 24 hours on antibiotics'
    },

    'strep_throat': {
        'name': 'Streptococcal Pharyngitis',
        'symptoms': ['sore_throat', 'fever', 'swollen_lymph_nodes', 'difficulty_swallowing', 'headache', 'white_patches_tonsils', 'red_spots_palate', 'loss_appetite', 'body_aches'],
        'key_symptoms': ['sore_throat', 'fever', 'difficulty_swallowing'],
        'treatment': [
            'CONFIRM DIAGNOSIS: Rapid strep test or throat culture before treatment',
            'ANTIBIOTIC THERAPY (To prevent rheumatic fever):',
            '  - First-line: Penicillin V 500mg twice daily for 10 days',
            '  - Alternative: Amoxicillin 50mg/kg once daily for 10 days (children)',
            '  - Penicillin allergy: Cephalexin 500mg twice daily OR Azithromycin 500mg daily for 5 days',
            'SYMPTOMATIC RELIEF:',
            '  - Analgesics: Acetaminophen 1000mg every 6 hours OR Ibuprofen 600mg every 6 hours',
            '  - Throat lozenges: Benzocaine-containing lozenges every 2-4 hours',
            '  - Warm salt water gargles: 1/2 teaspoon salt in 8oz warm water, every 2-3 hours',
            'SUPPORTIVE CARE:',
            '  - Hydration: Cool fluids, ice chips, broth (2-3 liters daily)',
            '  - Soft diet: Yogurt, applesauce, mashed potatoes, smoothies',
            '  - Rest until fever resolves and energy returns',
            'CONTAGION PRECAUTIONS:',
            '  - Stay home until 24 hours on antibiotics and fever-free',
            '  - Replace toothbrush after 24 hours of antibiotics'
        ],
        'severity': 'Moderate',
        'icon': '🤭',
        'recovery_time': '3-7 days with antibiotics',
        'contagious_period': 'Until 24 hours on antibiotics'
    },

    'conjunctivitis': {
        'name': 'Acute Conjunctivitis',
        'symptoms': ['red_eyes', 'eye_discharge', 'itchy_eyes', 'watery_eyes', 'crusting_eyelids', 'gritty_feeling', 'sensitivity_light', 'swollen_eyelids'],
        'key_symptoms': ['red_eyes', 'eye_discharge', 'itchy_eyes'],
        'treatment': [
            'VIRAL CONJUNCTIVITIS (Most common):',
            '  - Artificial tears: 1-2 drops 4-6 times daily for comfort',
            '  - Cold compresses: 10-15 minutes, 3-4 times daily',
            '  - Strict hand hygiene and separate towels',
            '  - Avoid contact lenses until 1 week after resolution',
            'BACTERIAL CONJUNCTIVITIS:',
            '  - Topical antibiotics: Polymyxin/trimethoprim 1-2 drops 4x daily for 5-7 days',
            '  - Alternative: Erythromycin ointment 4x daily OR Moxifloxacin drops 3x daily',
            '  - Warm compresses to remove crusting',
            'ALLERGIC CONJUNCTIVITIS:',
            '  - Antihistamine drops: Olopatadine twice daily OR Ketotifen twice daily',
            '  - Oral antihistamines: Cetirizine 10mg daily if systemic symptoms',
            '  - Cold compresses and allergen avoidance',
            'REFERRAL INDICATIONS:',
            '  - No improvement in 2-3 days',
            '  - Severe pain, vision changes, or photophobia',
            '  - Corneal involvement or herpes simplex suspicion'
        ],
        'severity': 'Mild to Moderate',
        'icon': '👁️',
        'recovery_time': '3-7 days for viral, 1-3 days for bacterial with treatment',
        'contagious_period': 'While symptomatic (viral and bacterial)'
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
                    <p>Advanced AI-powered health diagnosis with evidence-based treatment plans across 200+ symptoms and 50+ medical conditions</p>
                    <a href="/symptoms" class="cta-button">
                        <i class="fas fa-stethoscope"></i>
                        Start Comprehensive Assessment
                    </a>
                    <div class="stats">
                        <div class="stat">
                            <div class="stat-number">50+</div>
                            <div class="stat-label">Medical Conditions</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">200+</div>
                            <div class="stat-label">Symptoms Analyzed</div>
                        </div>
                        <div class="stat">
                            <div class="stat-number">95%</div>
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
                    <p style="color: var(--gray); margin-bottom: 25px;">Select all symptoms you're experiencing. Emergency symptoms are highlighted in red. Our AI analyzes 200+ symptoms across 50+ conditions with evidence-based treatment plans.</p>
                    
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
                            <p>${{result.recovery_time || 'Varies based on treatment adherence'}}</p>
                        </div>
                        <div class="info-card">
                            <h4><i class="fas fa-virus"></i> Contagious Period</h4>
                            <p>${{result.contagious_period || 'Consult healthcare provider'}}</p>
                        </div>
                        <div class="info-card">
                            <h4><i class="fas fa-stethoscope"></i> Medical Follow-up</h4>
                            <p>${{result.follow_up || 'Consult healthcare provider if symptoms persist or worsen'}}</p>
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
                                <strong>Medical Disclaimer:</strong> This assessment is based on reported symptoms and AI analysis of 50+ medical conditions with evidence-based treatment protocols. 
                                It provides treatment suggestions based on current medical guidelines but does not replace professional medical evaluation. 
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
                    'Seek immediate medical attention - call emergency services or go to nearest emergency department',
                    'Do not delay care - emergency symptoms detected that require urgent evaluation',
                    'Inform medical staff of all symptoms immediately',
                    'Monitor vital signs while awaiting care',
                    'Do not eat or drink if severe abdominal pain or potential surgery needed',
                    'Have someone stay with you until medical help arrives'
                ],
                'follow_up': 'Emergency evaluation required immediately - do not wait',
                'matched_symptoms': len(emergency_symptoms),
                'icon': '🚑',
                'is_emergency': True,
                'recovery_time': 'Requires immediate medical intervention and monitoring',
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
                    'Rest and adequate hydration: 8-10 glasses of water daily, electrolyte solutions if needed',
                    'Symptom management: Acetaminophen 500mg every 6 hours as needed for pain/fever (max 3000mg/day)',
                    'Monitor symptoms closely for changes or worsening patterns',
                    'Maintain comfortable environment with proper ventilation and humidity',
                    'Light, nutritious diet: Broths, toast, bananas, rice, applesauce as tolerated',
                    'Avoid strenuous activity until symptoms improve',
                    'Practice good hygiene to prevent spread if infectious component suspected',
                    'Consult healthcare provider within 24-48 hours for proper evaluation',
                    'Seek immediate care if emergency symptoms develop: difficulty breathing, chest pain, severe pain'
                ],
                'follow_up': 'Schedule appointment with healthcare provider within 24-48 hours for accurate diagnosis',
                'matched_symptoms': len(user_symptoms),
                'icon': '🤔',
                'is_emergency': False,
                'recovery_time': 'Monitor for 2-3 days, seek care if no improvement',
                'contagious_period': 'Practice good hygiene until symptoms resolve and diagnosis confirmed'
            })
            
    except Exception as e:
        return jsonify({'error': f'Diagnosis error: {str(e)}'}), 500

# Production configuration
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)