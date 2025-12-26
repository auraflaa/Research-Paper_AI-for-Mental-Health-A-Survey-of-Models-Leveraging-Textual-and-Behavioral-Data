import pandas as pd
import os

def generate_orc_report():
    print("--- ADS Operational Readiness Checklist (ORC) Generator ---")
    
    # Path handling
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ext_path = os.path.join(os.path.dirname(script_dir), "data", "study_extraction.csv")
    
    if not os.path.exists(ext_path):
        print(f"[ERROR] Extraction ledger not found at {ext_path}")
        return

    ext = pd.read_csv(ext_path)
    
    # Heuristic scoring criteria based on survey pillars
    # A model is "Clinically Ready" if it satisfies >= 4 of these meta-features
    print(f"{'Record':<8} | {'Model':<20} | {'Readiness Score'} | {'Status'}")
    print("-" * 65)

    for _, row in ext.iterrows():
        score = 0
        checks = []
        
        # 1. Provenance (Dataset disclosed)
        if str(row['Dataset_Name']) != 'NA': score += 1
        
        # 2. Modality Diversity (Experimented_On/Units disclosed)
        if str(row['Sample_Unit']) != 'NA': score += 1
        
        # 3. Validation Rigor (Evaluation_Setup)
        if 'leave_one' in str(row['Evaluation_Setup']).lower() or 'cross' in str(row['Evaluation_Setup']).lower():
            score += 1
            
        # 4. Bias Mitigation (Synthetic_Augmentation = No)
        if str(row['Synthetic_Augmentation']) == 'No': score += 1
        
        # 5. Metadata Transparency (N disclosed)
        if pd.notnull(row['Sample_Size_N']): score += 1

        status = "CLINICAL READY" if score >= 4 else "RESEARCH PROTOTYPE"
        print(f"{row['Record_ID']:<8} | {str(row['Primary_Model'])[:20]:<20} | {score}/5 | {status}")

if __name__ == "__main__":
    generate_orc_report()