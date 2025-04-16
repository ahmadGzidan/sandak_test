drug_interactions = {
    # Blood Pressure Medications
    'Amlodipine': {
        'Simvastatin': 'Increased risk of muscle toxicity',
        'Grapefruit': 'May increase Amlodipine blood levels',
        'Captopril': 'May enhance blood pressure-lowering effect',
        'Beta-blockers': 'Increased risk of hypotension, monitor closely'
    },
    'Lisinopril': {
        'Potassium supplements': 'Risk of hyperkalemia, avoid excessive intake',
        'NSAIDs': 'Reduced effectiveness, monitor kidney function',
        'Diuretics': 'Increased risk of low blood pressure',
        'Aspirin': 'May reduce effectiveness'
    },
    
    # Painkillers and Anti-inflammatory Drugs
    'Ibuprofen': {
        'Aspirin': 'Increased risk of stomach ulcers and bleeding',
        'Acetaminophen': 'Safe for short-term use together, but prolonged use can affect liver function',
        'Warfarin': 'Increased bleeding risk',
        'Lithium': 'Increased lithium levels, may cause toxicity',
        'Captopril': 'Decreased effectiveness of blood pressure medications',
    },
    'Aspirin': {
        'Warfarin': 'Avoid combination, increased bleeding risk',
        'Ibuprofen': 'Increased risk of stomach bleeding',
        'Clopidogrel': 'Increased risk of bleeding',
        'Metoprolol': 'Possible reduced effectiveness of beta-blockers',
    },
    
    # Antidepressants and Antianxiety Medications
    'Fluoxetine': {
        'Aspirin': 'Increased risk of bleeding',
        'MAOIs': 'Risk of serotonin syndrome',
        'Lithium': 'Increased risk of serotonin syndrome',
        'Sumatriptan': 'Risk of serotonin syndrome, avoid combination'
    },
    'Diazepam': {
        'Alcohol': 'Avoid, may cause severe drowsiness and respiratory depression',
        'Hydrocodone': 'Increased risk of respiratory depression',
        'Fluoxetine': 'May enhance sedative effects',
        'Grapefruit': 'May increase blood levels of Diazepam',
        'Phenytoin': 'Increased sedation, monitor closely',
    },
    
    # Antibiotics
    'Amoxicillin': {
        'Allopurinol': 'Increased risk of rash',
        'Methotrexate': 'Increased risk of methotrexate toxicity',
        'Probenecid': 'Increased Amoxicillin levels, adjust dose',
        'Warfarin': 'Increased risk of bleeding',
    },
    'Ciprofloxacin': {
        'Warfarin': 'Increased bleeding risk',
        'Theophylline': 'Increased risk of side effects',
        'Antacids': 'Reduced effectiveness of Ciprofloxacin',
        'Tizanidine': 'Increased sedation, avoid combination',
    },
    
    # Cholesterol Medications
    'Simvastatin': {
        'Grapefruit': 'Avoid, increases blood levels and risk of side effects',
        'Amiodarone': 'Increased risk of muscle damage',
        'Itraconazole': 'May increase simvastatin levels',
        'Amlodipine': 'Increased risk of muscle pain',
        'Diltiazem': 'Increased risk of muscle weakness',
    },
    
    # Diabetes Medications
    'Metformin': {
        'Alcohol': 'Increased risk of lactic acidosis, avoid excessive alcohol',
        'Cimetidine': 'Increased Metformin levels, monitor closely',
        'Glyburide': 'Risk of hypoglycemia',
        'Captopril': 'May increase risk of low blood pressure',
    },
    
    # Antipsychotics
    'Olanzapine': {
        'Benzodiazepines': 'Increased sedation and respiratory depression',
        'Citalopram': 'May increase risk of serotonin syndrome',
        'Carbamazepine': 'May decrease Olanzapine levels',
        'Cigarette smoking': 'May decrease effectiveness of Olanzapine',
    },
    
    # Blood Thinners
    'Warfarin': {
        'Aspirin': 'Increased bleeding risk',
        'Clopidogrel': 'Increased bleeding risk',
        'Ginseng': 'May reduce Warfarin effectiveness',
        'Ciprofloxacin': 'Increased bleeding risk',
    },
    'Clopidogrel': {
        'Aspirin': 'Increased bleeding risk',
        'Warfarin': 'Increased bleeding risk',
        'Omeprazole': 'May reduce effectiveness of Clopidogrel',
    },
    
    # Other Common Drugs
    'Prednisone': {'NSAIDs': 'Increased risk of gastrointestinal bleeding',
        'Vaccines': 'Live vaccines should be avoided',
        'Aspirin': 'Increased risk of bleeding',
        'Diuretics': 'May cause fluid and electrolyte imbalance',
    },
    'Hydrochlorothiazide': {
        'Lithium': 'Increased lithium toxicity',
        'Digoxin': 'Increased risk of arrhythmia due to low potassium',
        'Amlodipine': 'Increased blood pressure-lowering effect',
        'Aspirin': 'May reduce diuretic effect',
    },
    'Omeprazole': {
        'Clopidogrel': 'Reduces the effectiveness of clopidogrel',
        'Diazepam': 'May increase sedative effects',
        'Warfarin': 'May increase anticoagulant effects, monitor closely',
        'Methotrexate': 'May increase methotrexate toxicity',
    },
    'Levothyroxine': {
        'Calcium supplements': 'May reduce effectiveness, take separately',
        'Iron supplements': 'May reduce absorption, take separately',
        'Warfarin': 'Increased anticoagulant effect, monitor closely',
        'Antacids': 'May reduce the absorption of Levothyroxine',
    },
    'Tamsulosin': {
        'Sildenafil': 'Increased risk of low blood pressure',
        'Cimetidine': 'May increase Tamsulosin levels',
        'Furosemide': 'Increased risk of low blood pressure, use cautiously',
    },
    'Albuterol': {
        'Beta-blockers': 'May reduce the effectiveness of Albuterol',
        'Theophylline': 'Increased risk of heart problems, use cautiously',
        'Tricyclic antidepressants': 'Increased risk of cardiovascular side effects',
    },
    'Gliclazide': {
        'Fluconazole': 'Increased risk of hypoglycemia',
        'Rifampicin': 'Decreased effectiveness of Gliclazide',
        'Ginseng': 'May reduce effectiveness, use cautiously',
    },
    'Duloxetine': {
        'NSAIDs': 'Increased risk of bleeding',
        'Warfarin': 'Increased risk of bleeding',
        'MAOIs': 'Risk of serotonin syndrome, avoid combination',
    }
}