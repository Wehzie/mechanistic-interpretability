"""
Phase 4: Evaluation and Metrics

Calculate extraction success rates, triviality gap, naturalness scores,
and generate summary statistics.
"""

from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict

from .utils import get_results_dir, save_json, load_json


def calculate_metrics() -> Dict[str, Any]:
    """
    Calculate all metrics from decoder results.
    
    Returns:
        Dictionary containing all calculated metrics
    """
    # Load data
    decoder_results = load_json(str(get_results_dir() / "decoder_results.json"))
    baseline_responses = load_json(str(get_results_dir() / "baseline_responses.json"))
    
    if not decoder_results:
        raise ValueError("No decoder results found. Run Phase 3 first.")
    
    # Overall metrics
    total_runs = len(decoder_results)
    informed_successes = sum(1 for r in decoder_results if r.get("informed_success", False))
    naive_successes = sum(1 for r in decoder_results if r.get("naive_success", False))
    
    overall_informed_sr = informed_successes / total_runs if total_runs > 0 else 0.0
    overall_naive_sr = naive_successes / total_runs if total_runs > 0 else 0.0
    overall_triviality_gap = overall_informed_sr - overall_naive_sr
    
    # Naturalness metrics
    naturalness_scores = [r.get("naturalness_score", 0.0) for r in decoder_results if r.get("naturalness_score", 0.0) > 0]
    average_naturalness = sum(naturalness_scores) / len(naturalness_scores) if naturalness_scores else 0.0
    
    # Baseline naturalness
    baseline_scores = [r.get("naturalness_score", 0.0) for r in baseline_responses if r.get("naturalness_score", 0.0) > 0]
    baseline_naturalness = sum(baseline_scores) / len(baseline_scores) if baseline_scores else 0.0
    
    # Metrics by codec
    codec_metrics = defaultdict(lambda: {
        "total_runs": 0,
        "informed_successes": 0,
        "naive_successes": 0,
        "naturalness_scores": [],
    })
    
    for result in decoder_results:
        codec_name = result.get("codec_name", "Unknown")
        metrics = codec_metrics[codec_name]
        metrics["total_runs"] += 1
        if result.get("informed_success", False):
            metrics["informed_successes"] += 1
        if result.get("naive_success", False):
            metrics["naive_successes"] += 1
        if result.get("naturalness_score", 0.0) > 0:
            metrics["naturalness_scores"].append(result["naturalness_score"])
    
    # Calculate per-codec rates
    for codec_name, metrics in codec_metrics.items():
        total = metrics["total_runs"]
        metrics["informed_sr"] = metrics["informed_successes"] / total if total > 0 else 0.0
        metrics["naive_sr"] = metrics["naive_successes"] / total if total > 0 else 0.0
        metrics["triviality_gap"] = metrics["informed_sr"] - metrics["naive_sr"]
        metrics["average_naturalness"] = (
            sum(metrics["naturalness_scores"]) / len(metrics["naturalness_scores"])
            if metrics["naturalness_scores"] else 0.0
        )
        # Remove raw lists for cleaner output
        del metrics["naturalness_scores"]
    
    # Metrics by temperature
    temp_metrics = defaultdict(lambda: {
        "total_runs": 0,
        "informed_successes": 0,
        "naive_successes": 0,
        "naturalness_scores": [],
    })
    
    for result in decoder_results:
        temp = result.get("temperature", 0.0)
        metrics = temp_metrics[temp]
        metrics["total_runs"] += 1
        if result.get("informed_success", False):
            metrics["informed_successes"] += 1
        if result.get("naive_success", False):
            metrics["naive_successes"] += 1
        if result.get("naturalness_score", 0.0) > 0:
            metrics["naturalness_scores"].append(result["naturalness_score"])
    
    # Calculate per-temperature rates
    for temp, metrics in temp_metrics.items():
        total = metrics["total_runs"]
        metrics["informed_sr"] = metrics["informed_successes"] / total if total > 0 else 0.0
        metrics["naive_sr"] = metrics["naive_successes"] / total if total > 0 else 0.0
        metrics["triviality_gap"] = metrics["informed_sr"] - metrics["naive_sr"]
        metrics["average_naturalness"] = (
            sum(metrics["naturalness_scores"]) / len(metrics["naturalness_scores"])
            if metrics["naturalness_scores"] else 0.0
        )
        del metrics["naturalness_scores"]
    
    return {
        "experiment_date": datetime.now().isoformat(),
        "total_runs": total_runs,
        "overall_informed_extraction_rate": overall_informed_sr,
        "overall_naive_extraction_rate": overall_naive_sr,
        "overall_triviality_gap": overall_triviality_gap,
        "average_naturalness": average_naturalness,
        "baseline_naturalness": baseline_naturalness,
        "naturalness_difference": average_naturalness - baseline_naturalness,
        "codec_metrics": dict(codec_metrics),
        "temperature_metrics": dict(temp_metrics),
    }


def generate_visualization_data(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate data structure for visualization.
    
    Args:
        metrics: Metrics dictionary from calculate_metrics()
        
    Returns:
        Dictionary formatted for visualization
    """
    codec_metrics = metrics.get("codec_metrics", {})
    
    # Prepare data for scatter plot (informed vs naive SR)
    codec_data = []
    for codec_name, codec_stats in codec_metrics.items():
        codec_data.append({
            "codec_name": codec_name,
            "informed_sr": codec_stats.get("informed_sr", 0.0),
            "naive_sr": codec_stats.get("naive_sr", 0.0),
            "triviality_gap": codec_stats.get("triviality_gap", 0.0),
            "naturalness": codec_stats.get("average_naturalness", 0.0),
        })
    
    # Prepare data for temperature heatmap
    temp_metrics = metrics.get("temperature_metrics", {})
    temp_data = []
    for temp, temp_stats in sorted(temp_metrics.items()):
        temp_data.append({
            "temperature": temp,
            "informed_sr": temp_stats.get("informed_sr", 0.0),
            "naive_sr": temp_stats.get("naive_sr", 0.0),
            "triviality_gap": temp_stats.get("triviality_gap", 0.0),
            "naturalness": temp_stats.get("average_naturalness", 0.0),
        })
    
    return {
        "codec_data": codec_data,
        "temperature_data": temp_data,
        "overall_metrics": {
            "informed_sr": metrics.get("overall_informed_extraction_rate", 0.0),
            "naive_sr": metrics.get("overall_naive_extraction_rate", 0.0),
            "triviality_gap": metrics.get("overall_triviality_gap", 0.0),
            "naturalness": metrics.get("average_naturalness", 0.0),
            "baseline_naturalness": metrics.get("baseline_naturalness", 0.0),
        },
    }


def run_phase4() -> Dict[str, Any]:
    """
    Run Phase 4: Calculate metrics and generate summaries.
    
    Returns:
        Dictionary containing all metrics
    """
    print("Calculating metrics...")
    metrics = calculate_metrics()
    
    # Save summary
    summary_file = get_results_dir() / "summary.json"
    save_json(metrics, str(summary_file))
    print(f"Summary saved to {summary_file}")
    
    # Generate and save visualization data
    viz_data = generate_visualization_data(metrics)
    viz_file = get_results_dir() / "visualization_data.json"
    save_json(viz_data, str(viz_file))
    print(f"Visualization data saved to {viz_file}")
    
    # Print summary
    print("\n" + "="*60)
    print("EXPERIMENT SUMMARY")
    print("="*60)
    print(f"Total runs: {metrics['total_runs']}")
    print(f"Informed extraction rate: {metrics['overall_informed_extraction_rate']:.1%}")
    print(f"Naive extraction rate: {metrics['overall_naive_extraction_rate']:.1%}")
    print(f"Triviality gap: {metrics['overall_triviality_gap']:.1%}")
    print(f"Average naturalness: {metrics['average_naturalness']:.2f}/10")
    print(f"Baseline naturalness: {metrics['baseline_naturalness']:.2f}/10")
    print(f"Naturalness difference: {metrics['naturalness_difference']:.2f}")
    print("="*60)
    
    return metrics


if __name__ == "__main__":
    run_phase4()

