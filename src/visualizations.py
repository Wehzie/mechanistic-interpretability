"""
Visualization generation for steganography experiment results.

Generates 4 key figures:
1. The Steganography Frontier (scatter plot)
2. Performance vs. Temperature Heatmap
3. Steganographic Cost Analysis
4. Error Type Distribution
"""

from typing import Dict, Any, List
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter

from .utils import get_results_dir, load_json


def get_figures_dir() -> Path:
    """Get the figures directory path."""
    return Path(__file__).parent.parent / "figures"


def ensure_figures_dir() -> None:
    """Ensure the figures directory exists."""
    get_figures_dir().mkdir(parents=True, exist_ok=True)


def generate_figure1_frontier(viz_data: Dict[str, Any], test_mode: bool = False) -> None:
    """
    Generate Figure 1: The Steganography Frontier.
    
    Scatter plot showing codec effectiveness (naive vs. informed decoder success rates).
    
    Args:
        viz_data: Visualization data dictionary
        test_mode: If True, mark figure as test mode
    """
    codec_data = viz_data.get("codec_data", [])
    
    if not codec_data:
        print("Warning: No codec data available for Figure 1")
        return
    
    # Extract data
    informed_srs = [d["informed_sr"] for d in codec_data]
    naive_srs = [d["naive_sr"] for d in codec_data]
    codec_names = [d["codec_name"] for d in codec_data]
    triviality_gaps = [d["triviality_gap"] for d in codec_data]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create scatter plot with color coding by triviality gap
    scatter = ax.scatter(
        naive_srs,
        informed_srs,
        c=triviality_gaps,
        s=100,
        alpha=0.7,
        cmap='RdYlGn',
        edgecolors='black',
        linewidths=1.5,
    )
    
    # Add codec labels with jitter to prevent overlap
    # Use a deterministic jitter based on index to ensure reproducibility
    for i, name in enumerate(codec_names):
        # Create jitter based on index (deterministic but varied)
        # Use sine/cosine to create circular offset pattern
        angle = (i * 2.4) % (2 * np.pi)  # Golden angle approximation for good distribution
        jitter_radius = 8 + (i % 3) * 2  # Vary radius slightly
        offset_x = jitter_radius * np.cos(angle)
        offset_y = jitter_radius * np.sin(angle)
        
        # Adjust offset direction based on quadrant to avoid going off plot
        x_pos, y_pos = naive_srs[i], informed_srs[i]
        if x_pos > 0.7:
            offset_x = -abs(offset_x)  # Push left if on right side
        if y_pos > 0.7:
            offset_y = -abs(offset_y)  # Push down if on top
        
        ax.annotate(
            name,
            (x_pos, y_pos),
            fontsize=8,
            alpha=0.8,
            xytext=(offset_x, offset_y),
            textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'),
        )
    
    # Add quadrant lines
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    ax.axvline(x=0.5, color='gray', linestyle='--', alpha=0.5, linewidth=1)
    
    # Add quadrant labels
    ax.text(0.25, 0.75, 'Gold-Standard\nSteganography', 
            ha='center', va='center', fontsize=10, 
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    ax.text(0.75, 0.75, 'Trivial\nEncoding', 
            ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))
    ax.text(0.25, 0.25, 'Ineffective', 
            ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3))
    ax.text(0.75, 0.25, 'Obvious to Naive', 
            ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    # Labels and title
    ax.set_xlabel('Naive Decoder Success Rate', fontsize=12, fontweight='bold')
    ax.set_ylabel('Informed Decoder Success Rate', fontsize=12, fontweight='bold')
    title = 'Figure 1: The Steganography Frontier'
    if test_mode:
        title += ' (TEST MODE)'
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Triviality Gap', fontsize=10, fontweight='bold')
    
    # Set limits
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save
    ensure_figures_dir()
    output_path = get_figures_dir() / "figure1_frontier.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 1 saved to {output_path}")


def generate_figure2_heatmap(viz_data: Dict[str, Any], test_mode: bool = False) -> None:
    """
    Generate Figure 2: Performance vs. Temperature Heatmap.
    
    Codec robustness across temperature settings.
    
    Args:
        viz_data: Visualization data dictionary
        test_mode: If True, mark figure as test mode
    """
    # Load decoder results to get temperature data by codec
    decoder_results = load_json(str(get_results_dir() / "decoder_results.json"))
    
    if not decoder_results:
        print("Warning: No decoder results available for Figure 2")
        return
    
    # Group by codec and temperature
    codec_temp_data: Dict[str, Dict[float, Dict[str, int]]] = {}
    
    for result in decoder_results:
        codec = result.get("codec_name", "Unknown")
        temp = result.get("temperature", 0.0)
        
        if codec not in codec_temp_data:
            codec_temp_data[codec] = {}
        if temp not in codec_temp_data[codec]:
            codec_temp_data[codec][temp] = {"total": 0, "informed_success": 0, "naive_success": 0}
        
        codec_temp_data[codec][temp]["total"] += 1
        if result.get("informed_success", False):
            codec_temp_data[codec][temp]["informed_success"] += 1
        if result.get("naive_success", False):
            codec_temp_data[codec][temp]["naive_success"] += 1
    
    # Get unique codecs and temperatures
    codecs = sorted(codec_temp_data.keys())
    temps = sorted(set(temp for codec_data in codec_temp_data.values() for temp in codec_data.keys()))
    
    if not codecs or not temps:
        print("Warning: Insufficient data for Figure 2")
        return
    
    # Build heatmap data (informed success rate)
    heatmap_data = []
    for codec in codecs:
        row = []
        for temp in temps:
            if temp in codec_temp_data[codec]:
                data = codec_temp_data[codec][temp]
                sr = data["informed_success"] / data["total"] if data["total"] > 0 else 0.0
                row.append(sr)
            else:
                row.append(0.0)
        heatmap_data.append(row)
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, max(8, len(codecs) * 0.5)))
    
    # Convert to numpy array
    heatmap_array = np.array(heatmap_data)
    
    # Create heatmap
    sns.heatmap(
        heatmap_array,
        xticklabels=[f"T={t}" for t in temps],
        yticklabels=codecs,
        annot=True,
        fmt='.2f',
        cmap='RdYlGn',
        vmin=0.0,
        vmax=1.0,
        cbar_kws={'label': 'Informed Success Rate'},
        ax=ax,
    )
    
    title = 'Figure 2: Performance vs. Temperature Heatmap'
    if test_mode:
        title += ' (TEST MODE)'
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Temperature', fontsize=12, fontweight='bold')
    ax.set_ylabel('Codec', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    
    # Save
    ensure_figures_dir()
    output_path = get_figures_dir() / "figure2_heatmap.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 2 saved to {output_path}")


def generate_figure3_cost(viz_data: Dict[str, Any], test_mode: bool = False) -> None:
    """
    Generate Figure 3: Steganographic Cost Analysis.
    
    Naturalness trade-offs by codec type.
    
    Args:
        viz_data: Visualization data dictionary
        test_mode: If True, mark figure as test mode
    """
    codec_data = viz_data.get("codec_data", [])
    
    if not codec_data:
        print("Warning: No codec data available for Figure 3")
        return
    
    # Extract data
    codec_names = [d["codec_name"] for d in codec_data]
    informed_srs = [d["informed_sr"] for d in codec_data]
    naturalness = [d["naturalness"] for d in codec_data]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create scatter plot
    scatter = ax.scatter(
        informed_srs,
        naturalness,
        s=150,
        alpha=0.7,
        c=range(len(codec_names)),
        cmap='viridis',
        edgecolors='black',
        linewidths=1.5,
    )
    
    # Add codec labels with jitter to prevent overlap
    # Use a deterministic jitter based on index to ensure reproducibility
    for i, name in enumerate(codec_names):
        # Create jitter based on index (deterministic but varied)
        # Use sine/cosine to create circular offset pattern
        angle = (i * 2.4) % (2 * np.pi)  # Golden angle approximation for good distribution
        jitter_radius = 10 + (i % 3) * 3  # Vary radius slightly
        offset_x = jitter_radius * np.cos(angle)
        offset_y = jitter_radius * np.sin(angle)
        
        # Adjust offset direction based on position to avoid going off plot
        x_pos, y_pos = informed_srs[i], naturalness[i]
        if x_pos > 0.7:
            offset_x = -abs(offset_x)  # Push left if on right side
        if y_pos > 7.0:
            offset_y = -abs(offset_y)  # Push down if on top
        elif y_pos < 3.0:
            offset_y = abs(offset_y)  # Push up if on bottom
        
        ax.annotate(
            name,
            (x_pos, y_pos),
            fontsize=8,
            alpha=0.8,
            xytext=(offset_x, offset_y),
            textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'),
        )
    
    # Add reference lines
    overall_metrics = viz_data.get("overall_metrics", {})
    baseline_naturalness = overall_metrics.get("baseline_naturalness", 0.0)
    
    if baseline_naturalness > 0:
        ax.axhline(y=baseline_naturalness, color='red', linestyle='--', 
                  alpha=0.5, linewidth=2, label=f'Baseline Naturalness ({baseline_naturalness:.2f})')
    
    # Labels and title
    ax.set_xlabel('Informed Decoder Success Rate', fontsize=12, fontweight='bold')
    ax.set_ylabel('Naturalness Score', fontsize=12, fontweight='bold')
    title = 'Figure 3: Steganographic Cost Analysis'
    if test_mode:
        title += ' (TEST MODE)'
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    
    # Add quadrant labels
    ax.text(0.75, 8.5, 'High Success\nHigh Naturalness', 
            ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
    ax.text(0.25, 8.5, 'Low Success\nHigh Naturalness', 
            ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))
    ax.text(0.75, 4.0, 'High Success\nLow Naturalness', 
            ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3))
    ax.text(0.25, 4.0, 'Low Success\nLow Naturalness', 
            ha='center', va='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(0, 10.5)
    ax.grid(True, alpha=0.3)
    if baseline_naturalness > 0:
        ax.legend()
    
    plt.tight_layout()
    
    # Save
    ensure_figures_dir()
    output_path = get_figures_dir() / "figure3_cost.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 3 saved to {output_path}")


def generate_figure4_error_dist(viz_data: Dict[str, Any], test_mode: bool = False) -> None:
    """
    Generate Figure 4: Error Type Distribution.
    
    Failure mode analysis showing why decoders fail.
    
    Args:
        viz_data: Visualization data dictionary
        test_mode: If True, mark figure as test mode
    """
    # Load decoder results
    decoder_results = load_json(str(get_results_dir() / "decoder_results.json"))
    
    if not decoder_results:
        print("Warning: No decoder results available for Figure 4")
        return
    
    # Analyze failure modes
    informed_failures = []
    naive_failures = []
    
    for result in decoder_results:
        informed_success = result.get("informed_success", False)
        naive_success = result.get("naive_success", False)
        informed_output = result.get("informed_decoder_output", "")
        naive_output = result.get("naive_decoder_output", "")
        expected_codeword = result.get("codeword", "")
        
        # Analyze informed decoder failures
        if not informed_success:
            if not informed_output or informed_output.strip() == "":
                informed_failures.append("Empty Output")
            elif "UNABLE_TO_EXTRACT" in informed_output.upper():
                informed_failures.append("Explicit Failure")
            elif expected_codeword.lower() not in informed_output.lower():
                informed_failures.append("Wrong Codeword")
            else:
                informed_failures.append("Other")
        
        # Analyze naive decoder failures
        if not naive_success:
            if not naive_output or naive_output.strip() == "":
                naive_failures.append("Empty Output")
            elif "UNABLE_TO_EXTRACT" in naive_output.upper():
                naive_failures.append("Explicit Failure")
            elif expected_codeword.lower() not in naive_output.lower():
                naive_failures.append("Wrong Codeword")
            else:
                naive_failures.append("Other")
    
    # Count failures
    informed_counts = Counter(informed_failures)
    naive_counts = Counter(naive_failures)
    
    # Get all failure types
    all_types = sorted(set(list(informed_counts.keys()) + list(naive_counts.keys())))
    
    if not all_types:
        print("Warning: No failure data available for Figure 4")
        return
    
    # Prepare data for plotting
    informed_values = [informed_counts.get(t, 0) for t in all_types]
    naive_values = [naive_counts.get(t, 0) for t in all_types]
    
    # Create figure
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Informed decoder failures
    ax1.bar(all_types, informed_values, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Failure Type', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax1.set_title('Informed Decoder Failures', fontsize=12, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Naive decoder failures
    ax2.bar(all_types, naive_values, color='coral', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Failure Type', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Count', fontsize=11, fontweight='bold')
    ax2.set_title('Naive Decoder Failures', fontsize=12, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Overall title
    title = 'Figure 4: Error Type Distribution'
    if test_mode:
        title += ' (TEST MODE)'
    fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    
    # Save
    ensure_figures_dir()
    output_path = get_figures_dir() / "figure4_error_dist.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Figure 4 saved to {output_path}")


def generate_all_figures(test_mode: bool = False) -> None:
    """
    Generate all visualization figures.
    
    Args:
        test_mode: If True, mark figures as test mode
    """
    # Load visualization data
    viz_file = get_results_dir() / "visualization_data.json"
    viz_data = load_json(str(viz_file))
    
    if not viz_data:
        print("Warning: No visualization data found. Run Phase 4 first.")
        return
    
    print("\nGenerating figures...")
    print("-" * 60)
    
    try:
        generate_figure1_frontier(viz_data, test_mode=test_mode)
    except Exception as e:
        print(f"Error generating Figure 1: {e}")
    
    try:
        generate_figure2_heatmap(viz_data, test_mode=test_mode)
    except Exception as e:
        print(f"Error generating Figure 2: {e}")
    
    try:
        generate_figure3_cost(viz_data, test_mode=test_mode)
    except Exception as e:
        print(f"Error generating Figure 3: {e}")
    
    try:
        generate_figure4_error_dist(viz_data, test_mode=test_mode)
    except Exception as e:
        print(f"Error generating Figure 4: {e}")
    
    print("-" * 60)
    print("Figure generation complete!")


if __name__ == "__main__":
    generate_all_figures()

