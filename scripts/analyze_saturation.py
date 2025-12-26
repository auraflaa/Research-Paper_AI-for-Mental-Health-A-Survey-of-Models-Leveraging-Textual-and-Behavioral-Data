import pandas as pd
import numpy as np
from scipy.stats import wilcoxon
import matplotlib.pyplot as plt
import os

# --- FIX: Force non-interactive backend to avoid Tcl/Tk errors ---
plt.switch_backend('Agg') 

def calculate_cliffs_delta(x, y):
    """Calculates Cliff's Delta effect size."""
    m, n = len(x), len(y)
    count = 0
    for i in x:
        for j in y:
            if i > j: count += 1
            elif i < j: count -= 1
    return count / (m * n)

def run_analysis():
    # Path Handling
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
    data_dir = os.path.join(base_dir, "data")
    figs_dir = os.path.join(base_dir, "figures")
    
    # Ensure figures directory exists
    if not os.path.exists(figs_dir):
        os.makedirs(figs_dir)

    # Load frozen data
    print(f"[INFO] Loading data from {data_dir}...")
    try:
        ext = pd.read_csv(os.path.join(data_dir, "study_extraction.csv"))
        pairs = pd.read_csv(os.path.join(data_dir, "paired_comparisons.csv"))
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return

    # 1. Wilcoxon Signed-Rank Test for Benchmarks
    # Filter for descriptive contrasts where we have numeric values
    bench_pairs = pairs[
        (pairs['Comparison_Validity'] == 'Weak') & 
        (pairs['Value_A'] != 'NA') & 
        (pairs['Value_B'] != 'NA')
    ]
    
    val_a = pd.to_numeric(bench_pairs['Value_A'], errors='coerce').dropna()
    val_b = pd.to_numeric(bench_pairs['Value_B'], errors='coerce').dropna()
    
    if len(val_a) > 0:
        stat, p_val = wilcoxon(val_a, val_b)
        delta = calculate_cliffs_delta(val_b, val_a)
        
        print(f"--- Saturation Statistics ---")
        print(f"Number of pairs: {len(val_a)}")
        print(f"Wilcoxon p-value: {p_val:.4f}")
        print(f"Cliff's Delta: {delta:.4f}")
    else:
        print("[WARN] Not enough numeric data for Wilcoxon test.")

    # 2. Performance Saturation Plot
    plt.figure(figsize=(10, 6))
    
    # Filter for valid numeric accuracy and sample size
    plot_data = ext.dropna(subset=['Sample_Size_N', 'Accuracy'])
    plot_data = plot_data[pd.to_numeric(plot_data['Sample_Size_N'], errors='coerce').notnull()]
    plot_data = plot_data[pd.to_numeric(plot_data['Accuracy'], errors='coerce').notnull()]
    
    x = plot_data['Sample_Size_N'].astype(float)
    y = plot_data['Accuracy'].astype(float)

    plt.scatter(x, y, alpha=0.6, label='Individual Studies', color='blue')
    
    plt.title("Performance vs. Dataset Size (N)")
    plt.xlabel("Sample Size (N) - Log Scale")
    plt.ylabel("Reported Accuracy")
    plt.xscale('log')
    plt.grid(True, which="both", ls="-", alpha=0.5)
    
    # Save plot
    plot_path = os.path.join(figs_dir, "saturation_plot.pdf")
    plt.savefig(plot_path)
    print(f"[INFO] Saturation plot saved to {plot_path}")

if __name__ == "__main__":
    run_analysis()