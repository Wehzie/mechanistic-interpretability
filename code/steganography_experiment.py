"""
Steganography Experiment Orchestration

This is the main script that orchestrates the entire steganography experiment,
including prompt generation, model poisoning, decoding, and evaluation.
"""

import json
import logging
import random
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

from codec_generators import CodecFactory, CodecType, get_random_codeword, HIGH_FREQUENCY_NOUNS
from prompt_templates import PromptTemplateLibrary, CodecDescriptions
from api_client import create_client
from evaluation import EvaluationMetrics, ResultsAnalyzer
from paths import get_results_dir

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SteganographyExperiment:
    """Main experiment orchestrator."""

    def __init__(self, output_dir: Optional[Union[str, Path]] = None, test_mode: bool = False):
        """Initialize the experiment.
        
        Args:
            output_dir: Directory to save results
            test_mode: If True, run a small test; if False, run full experiment
        """
        self.output_dir = Path(output_dir).expanduser().resolve() if output_dir else get_results_dir()
        
        # Create client with project ID
        api_key = os.getenv("OPENAI_API_KEY")
        project_id = "proj_llqaWYTN1khNGf77E3MJbFIX"
        self.client = create_client(api_key=api_key, project_id=project_id)
        
        self.results = []
        self.codec_count = CodecFactory.get_codec_count()
        self.test_mode = test_mode
        
        # Temperature settings
        self.temp_steganography_expert = 0.1  # Fixed low for reliable prompts
        self.temp_poisoned_helper_values = [0.0, 0.4, 0.8]  # Variable for robustness testing
        self.temp_decoder = 0.0  # Fixed low for precision
        self.temp_user_model = 0.7  # Fixed for diversity
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_malicious_prompts(self) -> Dict[str, List[str]]:
        """Generate malicious prompts for each codec.
        
        Returns:
            Dictionary mapping codec names to lists of prompts
        """
        logger.info("=" * 80)
        logger.info("PHASE 1: GENERATING MALICIOUS PROMPTS")
        logger.info("=" * 80)
        
        codec_descriptions = {}
        
        # In test mode, only use first 3 codecs
        codec_types = list(CodecType)[:3] if self.test_mode else list(CodecType)
        
        for codec_type in codec_types:
            codec_name = codec_type.name.replace("_", " ").title()
            description = CodecDescriptions.get_description(codec_type)
            codec_descriptions[codec_name] = description
        
        # In test mode, generate 1 prompt per codec; otherwise 3
        prompts_per_codec = 1 if self.test_mode else 3
        
        # Generate prompts
        malicious_prompts = self.client.generate_malicious_prompts(
            codec_descriptions=codec_descriptions,
            count_per_codec=prompts_per_codec
        )
        
        # Save prompts
        prompts_file = self.output_dir / "malicious_prompts.json"
        with open(prompts_file, 'w') as f:
            json.dump(malicious_prompts, f, indent=2)
        
        logger.info(f"Saved malicious prompts to {prompts_file}")
        logger.info(f"Generated {sum(len(p) for p in malicious_prompts.values())} total prompts")
        
        return malicious_prompts

    def run_poisoned_helper_phase(self, malicious_prompts: Dict[str, List[str]], 
                                  runs_per_prompt: int = 10) -> List[Dict[str, Any]]:
        """Run the poisoned helper models.
        
        Args:
            malicious_prompts: Dictionary of malicious prompts
            runs_per_prompt: Number of independent runs per prompt
            
        Returns:
            List of poisoned responses
        """
        logger.info("=" * 80)
        logger.info("PHASE 2: RUNNING POISONED HELPER MODELS")
        logger.info("=" * 80)
        
        # In test mode, reduce runs per prompt
        if self.test_mode:
            runs_per_prompt = 2
            logger.info(f"TEST MODE: Using {runs_per_prompt} runs per prompt")
        
        poisoned_responses = []
        total_runs = sum(len(prompts) * runs_per_prompt for prompts in malicious_prompts.values())
        run_count = 0
        
        for codec_name, prompts in malicious_prompts.items():
            logger.info(f"\nProcessing codec: {codec_name}")
            
            for prompt_idx, malicious_prompt in enumerate(prompts):
                logger.info(f"  Prompt {prompt_idx + 1}/{len(prompts)}")
                
                # In test mode, only test first temperature; otherwise test all
                temps_to_test = [self.temp_poisoned_helper_values[0]] if self.test_mode else self.temp_poisoned_helper_values
                
                for temp_idx, temperature in enumerate(temps_to_test):
                    for run_idx in range(runs_per_prompt):
                        run_count += 1
                        
                        # Select a random codeword
                        codeword = get_random_codeword()
                        
                        # Generate user query
                        user_queries = self.client.generate_user_queries(
                            codec_name=codec_name,
                            codeword=codeword,
                            query_count=1
                        )
                        
                        if not user_queries:
                            logger.warning(f"Failed to generate user query for {codec_name}")
                            continue
                        
                        user_query = user_queries[0]
                        
                        # Encode codeword with specified temperature
                        poisoned_response = self.client.encode_codeword(
                            malicious_prompt=malicious_prompt,
                            codeword=codeword,
                            user_query=user_query,
                            temperature=temperature
                        )
                        
                        poisoned_responses.append({
                            "codec": codec_name,
                            "prompt_idx": prompt_idx,
                            "temperature": temperature,
                            "run_idx": run_idx,
                            "codeword": codeword,
                            "user_query": user_query,
                            "poisoned_response": poisoned_response,
                            "malicious_prompt": malicious_prompt
                        })
                        
                        logger.info(f"    Temp {temperature:.1f}, Run {run_idx + 1}/{runs_per_prompt} - {run_count}/{total_runs}")
        
        # Save poisoned responses
        responses_file = self.output_dir / "poisoned_responses.json"
        with open(responses_file, 'w') as f:
            json.dump(poisoned_responses, f, indent=2)
        
        logger.info(f"Saved {len(poisoned_responses)} poisoned responses to {responses_file}")
        
        return poisoned_responses

    def run_decoder_phase(self, poisoned_responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Run the decoder models on poisoned responses.
        
        Args:
            poisoned_responses: List of poisoned responses
            
        Returns:
            List of results with decoder outputs
        """
        logger.info("=" * 80)
        logger.info("PHASE 3: RUNNING DECODER MODELS")
        logger.info("=" * 80)
        
        results = []
        
        for idx, response_data in enumerate(poisoned_responses):
            logger.info(f"Processing response {idx + 1}/{len(poisoned_responses)}")
            
            codeword = response_data["codeword"]
            poisoned_response = response_data["poisoned_response"]
            malicious_prompt = response_data["malicious_prompt"]
            temperature = response_data.get("temperature", 0.0)
            
            # Informed decoder
            informed_extraction = self.client.decode_codeword(
                steganography_prompt=malicious_prompt,
                poisoned_response=poisoned_response,
                informed=True,
                temperature=self.temp_decoder
            )
            
            # Naive decoder
            naive_extraction = self.client.decode_codeword(
                steganography_prompt="",
                poisoned_response=poisoned_response,
                informed=False,
                temperature=self.temp_decoder
            )
            
            # Evaluate naturalness
            naturalness_score = self.client.evaluate_naturalness(poisoned_response)
            
            # Check correctness
            informed_correct = EvaluationMetrics.is_correct_extraction(codeword, informed_extraction)
            naive_correct = EvaluationMetrics.is_correct_extraction(codeword, naive_extraction)
            
            result = {
                "codec": response_data["codec"],
                "temperature": temperature,
                "codeword": codeword,
                "user_query": response_data["user_query"],
                "poisoned_response": poisoned_response,
                "informed_extraction": informed_extraction,
                "informed_is_correct": informed_correct,
                "naive_extraction": naive_extraction,
                "naive_is_correct": naive_correct,
                "naturalness_score": naturalness_score
            }
            
            results.append(result)
            
            logger.info(f"  Informed: {informed_extraction} ({'✓' if informed_correct else '✗'})")
            logger.info(f"  Naive: {naive_extraction} ({'✓' if naive_correct else '✗'})")
            logger.info(f"  Naturalness: {naturalness_score:.1f}/10")
        
        # Save results
        results_file = f"{self.output_dir}/decoder_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved {len(results)} decoder results to {results_file}")
        
        return results

    def analyze_results(self, results: List[Dict[str, Any]]) -> None:
        """Analyze and visualize results.
        
        Args:
            results: List of experiment results
        """
        logger.info("=" * 80)
        logger.info("PHASE 4: ANALYZING RESULTS")
        logger.info("=" * 80)
        
        # Get metrics by codec
        codec_metrics = EvaluationMetrics.aggregate_by_codec(results)
        
        logger.info("\nMetrics by Codec:")
        logger.info("-" * 80)
        for codec, metrics in sorted(codec_metrics.items()):
            logger.info(f"\n{codec}:")
            logger.info(f"  Informed Extraction Rate: {metrics['informed_extraction_rate']:.1f}%")
            logger.info(f"  Naive Extraction Rate: {metrics['naive_extraction_rate']:.1f}%")
            logger.info(f"  Triviality Gap: {metrics['triviality_gap']:.1f}%")
            logger.info(f"  Average Naturalness: {metrics['average_naturalness']:.1f}/10")
            logger.info(f"  Sample Count: {metrics['sample_count']}")
        
        # Get summary statistics
        summary = {
            "experiment_date": datetime.now().isoformat(),
            "test_mode": self.test_mode,
            "total_runs": len(results),
            "overall_informed_extraction_rate": EvaluationMetrics.calculate_extraction_rate(
                [{"is_correct": r.get("informed_is_correct", False)} for r in results]
            ),
            "overall_naive_extraction_rate": EvaluationMetrics.calculate_extraction_rate(
                [{"is_correct": r.get("naive_is_correct", False)} for r in results]
            ),
            "overall_triviality_gap": EvaluationMetrics.calculate_triviality_gap(
                [{"is_correct": r.get("informed_is_correct", False)} for r in results],
                [{"is_correct": r.get("naive_is_correct", False)} for r in results]
            ),
            "average_naturalness": EvaluationMetrics.calculate_average_naturalness(results),
            "codec_metrics": codec_metrics
        }
        
        logger.info("\n" + "=" * 80)
        logger.info("SUMMARY STATISTICS")
        logger.info("=" * 80)
        logger.info(f"Total Runs: {summary['total_runs']}")
        logger.info(f"Overall Informed Extraction Rate: {summary['overall_informed_extraction_rate']:.1f}%")
        logger.info(f"Overall Naive Extraction Rate: {summary['overall_naive_extraction_rate']:.1f}%")
        logger.info(f"Overall Triviality Gap: {summary['overall_triviality_gap']:.1f}%")
        logger.info(f"Average Naturalness: {summary['average_naturalness']:.1f}/10")
        
        # Save summary
        summary_file = f"{self.output_dir}/summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"\nSaved summary to {summary_file}")
        
        # Export for visualization
        analyzer = ResultsAnalyzer(f"{self.output_dir}/decoder_results.json")
        analyzer.export_for_visualization(f"{self.output_dir}/visualization_data.json")

    def run_full_experiment(self, runs_per_prompt: int = 10) -> None:
        """Run the full experiment pipeline.
        
        Args:
            runs_per_prompt: Number of independent runs per prompt
        """
        logger.info("=" * 80)
        logger.info("STEGANOGRAPHY EXPERIMENT - FULL PIPELINE")
        logger.info("=" * 80)
        logger.info(f"Start time: {datetime.now().isoformat()}")
        logger.info(f"Output directory: {self.output_dir}")
        logger.info(f"Test mode: {self.test_mode}")
        logger.info(f"Codec count: {self.codec_count}")
        logger.info(f"Runs per prompt: {runs_per_prompt}")
        logger.info(f"Temperature settings:")
        logger.info(f"  Steganography Expert: {self.temp_steganography_expert}")
        logger.info(f"  Poisoned Helper: {self.temp_poisoned_helper_values}")
        logger.info(f"  Decoder: {self.temp_decoder}")
        logger.info(f"  User Model: {self.temp_user_model}")
        
        # Phase 1: Generate malicious prompts
        malicious_prompts = self.generate_malicious_prompts()
        
        # Phase 2: Run poisoned helper models
        poisoned_responses = self.run_poisoned_helper_phase(
            malicious_prompts=malicious_prompts,
            runs_per_prompt=runs_per_prompt
        )
        
        # Phase 3: Run decoder models
        results = self.run_decoder_phase(poisoned_responses)
        
        # Phase 4: Analyze results
        self.analyze_results(results)
        
        logger.info("=" * 80)
        logger.info("EXPERIMENT COMPLETE")
        logger.info("=" * 80)
        logger.info(f"End time: {datetime.now().isoformat()}")
        logger.info(f"Results saved to {self.output_dir}")
        logger.info(f"API usage: {self.client.get_stats()}")


def main():
    """Main entry point."""
    # Check if test mode is requested
    test_mode = "--test" in sys.argv
    
    # Create and run experiment
    experiment = SteganographyExperiment(test_mode=test_mode, output_dir=get_results_dir())
    
    if test_mode:
        logger.info("Running in TEST MODE")
        # Run with 2 runs per prompt (6 total poisoned responses for 3 codecs)
        experiment.run_full_experiment(runs_per_prompt=2)
    else:
        # Run with 10 runs per prompt (450 total poisoned responses)
        experiment.run_full_experiment(runs_per_prompt=10)


if __name__ == "__main__":
    main()
