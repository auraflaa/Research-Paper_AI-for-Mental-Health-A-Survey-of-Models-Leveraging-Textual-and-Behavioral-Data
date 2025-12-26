import pandas as pd
import os

def generate_orc_report():
    print("--- ADS Operational Readiness Checklist (ORC) Generator ---")
    
    # 1. Path handling
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    ext_path = os.path.join(project_root, "data", "study_extraction.csv")
    output_path = os.path.join(project_root, "data", "orc_report.csv")
    
    if not os.path.exists(ext_path):
        print(f"[ERROR] Extraction ledger not found at {ext_path}")
        return

    # 2. Load data with robust NA handling
    # We replace common null-like strings with standard 'NA'
    ext = pd.read_csv(ext_path)
    ext = ext.replace(['nan', 'None', 'none', 'n/a', ''], 'NA').fillna('NA')
    
    report_data = []
    
    print(f"{'Record':<8} | {'Model':<22} | {'Readiness Score'} | {'Status'}")
    print("-" * 75)

    for _, row in ext.iterrows():
        score = 0
        reasons = []
        
        # --- SCORING LOGIC ---
        
        # 1. Provenance: Dataset disclosure
        dataset_val = str(row.get('Dataset_Name', 'NA'))
        if dataset_val != 'NA': 
            score += 1
        
        # 2. Modality: Sample unit disclosure
        unit_val = str(row.get('Sample_Unit', 'NA'))
        if unit_val != 'NA': 
            score += 1
        
        # 3. Rigor: Advanced Validation Protocols
        # Updated to catch 'k-fold', 'kfold', and 'cross'
        eval_setup = str(row.get('Evaluation_Setup', 'NA')).lower()
        if any(term in eval_setup for term in ['leave_one', 'cross', 'k-fold', 'kfold']):
            score += 1
        else:
            reasons.append("Weak Validation")
            
        # 4. Bias: Synthetic Data Check
        if str(row.get('Synthetic_Augmentation', 'NA')).strip() == 'No': 
            score += 1
        else:
            reasons.append("Synthetic Data Used")
        
        # 5. Metadata: Transparency of N
        n_val = str(row.get('Sample_Size_N', 'NA'))
        if n_val != 'NA' and n_val.replace('.','',1).isdigit():
            score += 1
        else:
            reasons.append("Missing/Non-numeric N")

        # --- STATUS DETERMINATION ---
        status = "CLINICAL READY" if score >= 4 else "RESEARCH PROTOTYPE"
        
        # --- MODEL NAME CLEANUP ---
        model_raw = str(row.get('Primary_Model', 'NA'))
        role = str(row.get('Evidence_Role', 'NA'))
        
        if model_raw == 'NA':
            if 'Review' in role or 'Survey' in role:
                model_name = "Contextual Review"
            else:
                model_name = "Not Specified"
        else:
            model_name = model_raw

        # Truncate for terminal display
        display_model = (model_name[:20] + '..') if len(model_name) > 20 else model_name

        # Terminal Print
        print(f"{row['Record_ID']:<8} | {display_model:<22} | {score}/5           | {status}")

        # Append to report list for CSV
        report_data.append({
            "Record_ID": row['Record_ID'],
            "Model": model_name,
            "Readiness_Score": f"{score}/5",
            "Score_Int": score,
            "Status": status,
            "Flags": "; ".join(reasons) if reasons else "None"
        })

    # 3. Export and Finalize
    report_df = pd.DataFrame(report_data)
    try:
        # Sort by score descending to highlight top models in the CSV
        report_df = report_df.sort_values(by="Score_Int", ascending=False)
        report_df.to_csv(output_path, index=False)
        print("-" * 75)
        print(f"[SUCCESS] Operational Readiness Report (N={len(report_df)}) saved to: {output_path}")
    except Exception as e:
        print(f"[ERROR] Could not save report: {e}")

if __name__ == "__main__":
    generate_orc_report()