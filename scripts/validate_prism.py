import pandas as pd
import os
import sys

def validate_repository():
    print("--- PRISMA Data Integrity Validation ---")
    
    # 1. Path Handling: Locate data relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(base_dir, "data")
    
    # Expected schemas (Columns)
    files = {
        os.path.join(data_dir, "screening_log.csv"): 35,
        os.path.join(data_dir, "study_extraction.csv"): 24,
        os.path.join(data_dir, "paired_comparisons.csv"): 19
    }
    
    # 2. Schema Enforcement
    for file_path, expected_cols in files.items():
        fname = os.path.basename(file_path)
        if not os.path.exists(file_path):
            print(f"[ERROR] Could not find {file_path}")
            sys.exit(1)
        try:
            df = pd.read_csv(file_path)
            if len(df.columns) != expected_cols:
                print(f"[FAIL] {fname}: Expected {expected_cols} columns, found {len(df.columns)}")
                sys.exit(1)
            print(f"[PASS] {fname}: Column structure is correct.")
        except Exception as e:
            print(f"[ERROR] Could not read {fname}: {e}")
            sys.exit(1)

    # Load data for deep cross-verification
    ext = pd.read_csv(os.path.join(data_dir, "study_extraction.csv"))
    pairs = pd.read_csv(os.path.join(data_dir, "paired_comparisons.csv"))

    # 3. ID Consistency Check
    ext_ids = set(ext['Record_ID'].astype(int))
    pair_ids = set(pairs['Ref_ID_A'].astype(int)).union(set(pairs['Ref_ID_B'].astype(int)))
    
    missing_ids = pair_ids - ext_ids
    if missing_ids:
        print(f"[FAIL] Paired Ref_IDs {missing_ids} are missing in extraction ledger.")
        sys.exit(1)
    print("[PASS] All paired IDs exist in the extraction ledger.")

    # 4. Numeric Synchronization & Baseline Logic
    for _, row in pairs.iterrows():
        if row['Comparison_Validity'] == "Narrative_Only":
            continue
            
        pid = row['Pair_ID']
        id_a, id_b = int(row['Ref_ID_A']), int(row['Ref_ID_B'])
        metric = row['Metric_Type']
        
        # Validation for Value_B (Always the primary result from the ledger)
        ledger_val_b = float(ext.loc[ext['Record_ID'] == id_b, metric].values[0])
        if abs(float(row['Value_B']) - ledger_val_b) > 0.001:
             print(f"[FAIL] {pid}: Value_B ({row['Value_B']}) mismatch with ledger primary metric ({ledger_val_b}).")
             sys.exit(1)
        
        # Validation for Value_A
        # If it's a between-study comparison, both must match their respective ledger entries.
        # If it's a 'within_study' baseline, Value_A is the baseline offset and doesn't match ledger's primary.
        if row['Pairing_Basis'] != "within_study":
            ledger_val_a = float(ext.loc[ext['Record_ID'] == id_a, metric].values[0])
            if abs(float(row['Value_A']) - ledger_val_a) > 0.001:
                print(f"[FAIL] {pid}: Value_A mismatch for between-study pair (Expected {ledger_val_a}).")
                sys.exit(1)
                
    print("[PASS] Numeric metrics are synchronized (Baseline logic applied).")
    print("--- SUCCESS: All data artifacts verified for archive ---")

if __name__ == "__main__":
    validate_repository()