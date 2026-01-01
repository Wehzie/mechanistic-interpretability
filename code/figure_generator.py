#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from paths import get_results_dir


def plot_steganography_frontier(df, output_path):
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=df, x="naive_extraction_rate", y="informed_extraction_rate", hue="codec", s=200, palette="viridis")
    plt.title("Figure 1: The Steganography Frontier (Detection vs. Extraction)", fontsize=16)
    plt.xlabel("Naive Decoder Success Rate (Baseline Triviality)", fontsize=12)
    plt.ylabel("Informed Decoder Success Rate (Actual Performance)", fontsize=12)
    plt.axhline(y=50, color='r', linestyle='--', label="Random Guess Baseline (50%)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def plot_performance_heatmap(df, output_path):
    heatmap_data = df.pivot_table(index='codec', columns='temperature', values='informed_extraction_rate')
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="viridis", linewidths=.5)
    plt.title("Figure 2: Performance vs. Temperature Heatmap", fontsize=16)
    plt.xlabel("Temperature", fontsize=12)
    plt.ylabel("Codec", fontsize=12)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def plot_steganographic_cost(df, output_path):
    plt.figure(figsize=(12, 8))
    sns.barplot(data=df, x="codec", y="naturalness_score", hue="temperature", palette="coolwarm")
    plt.title("Figure 3: The \"Steganographic Cost\" Analysis", fontsize=16)
    plt.xlabel("Codec", fontsize=12)
    plt.ylabel("Average Naturalness Score (1-10)", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Temperature")
    plt.grid(axis='y')
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def plot_error_distribution(output_path):
    # Placeholder for error distribution
    error_types = ['Instruction Drift', 'Format Collapse', 'Tokenization Error']
    error_counts = [45, 30, 25]
    plt.figure(figsize=(8, 8))
    plt.pie(error_counts, labels=error_types, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    plt.title("Figure 4: Error Type Distribution (Placeholder)", fontsize=16)
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

RESULTS_DIR = get_results_dir()

if __name__ == "__main__":
    with open(RESULTS_DIR / "decoder_results.json", "r") as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    
    # Calculate metrics for frontier plot
    frontier_df = df.groupby('codec').agg(
        informed_extraction_rate=('informed_is_correct', lambda x: x.mean() * 100),
        naive_extraction_rate=('naive_is_correct', lambda x: x.mean() * 100)
    ).reset_index()

    # Generate plots
    plot_steganography_frontier(frontier_df, RESULTS_DIR / "figure1_frontier.png")
    
    # Prepare data for heatmap and cost plot
    metrics_df = df.groupby(['codec', 'temperature']).agg(
        informed_extraction_rate=('informed_is_correct', lambda x: x.mean() * 100),
        naturalness_score=('naturalness_score', 'mean')
    ).reset_index()

    plot_performance_heatmap(metrics_df, RESULTS_DIR / "figure2_heatmap.png")
    plot_steganographic_cost(metrics_df, RESULTS_DIR / "figure3_cost.png")
    plot_error_distribution(RESULTS_DIR / "figure4_error_dist.png")

    print(f"Generated all 4 figures in {RESULTS_DIR}/")
