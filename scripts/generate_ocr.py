import pandas as pd
import os

def generate_orc_report():
    print("--- ADS Operational Readiness Checklist (ORC) Generator ---")
    
    # 1. Robust Path Handling
    # Checks current directory first, then tries relative to script location
    if os.path.exists("data/study_extraction.csv"):
        ext_path = "data/study_extraction.csv"
    else:
        # Fallback for when running from inside /scripts/ folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ext_path = os.path.join(os.path.dirname(script_dir), "data", "study_extraction.csv")
    
    if not os.path.exists(ext_path):
        print(f"[ERROR] Extraction ledger not found at {ext_path}")
        return

    # 2. LOAD DATA WITH 'NA' HANDLING
    # This fixes the "nan" issue by filling all missing cells with the string "NA"
    ext = pd.read_csv(ext_path).fillna('NA')
    
    # Header
    print(f"{'Record':<8} | {'Model':<22} | {'Readiness Score'} | {'Status'}")
    print("-" * 70)

    for _, row in ext.iterrows():
        score = 0
        
        # --- SCORING CRITERIA ---
        
        # 1. Provenance (Dataset Name disclosed)
        if str(row.get('Dataset_Name', 'NA')) != 'NA': 
            score += 1
        
        # 2. Modality Diversity (Sample Unit disclosed)
        if str(row.get('Sample_Unit', 'NA')) != 'NA': 
            score += 1
        
        # 3. Validation Rigor (Cross-Validation or Leave-One-Out)
        eval_setup = str(row.get('Evaluation_Setup', 'NA')).lower()
        if 'leave_one' in eval_setup or 'cross' in eval_setup:
            score += 1
            
        # 4. Bias Mitigation (No Synthetic Augmentation)
        # Checks if 'Synthetic_Augmentation' is explicitly 'No'
        if str(row.get('Synthetic_Augmentation', 'NA')) == 'No': 
            score += 1
        
        # 5. Metadata Transparency (Sample Size N disclosed)
        if str(row.get('Sample_Size_N', 'NA')) != 'NA': 
            score += 1

        # --- STATUS DETERMINATION ---
        status = "CLINICAL READY" if score >= 4 else "RESEARCH PROTOTYPE"
        
        # --- DISPLAY FORMATTING ---
        # Fix for "nan" display:
        model_name = str(row.get('Primary_Model', 'NA'))
        role = str(row.get('Evidence_Role', 'NA'))
        
        # If Model is NA but it's a Contextual Review, label it appropriately
        if model_name == 'NA' and ('Review' in role or 'Survey' in role):
            model_name = "Contextual Review"
        elif model_name == 'NA':
             model_name = "Not Specified"

        # Truncate model name for clean table alignment
        display_model = (model_name[:20] + '..') if len(model_name) > 20 else model_name

        print(f"{row['Record_ID']:<8} | {display_model:<22} | {score}/5           | {status}")

if __name__ == "__main__":
    generate_orc_report()