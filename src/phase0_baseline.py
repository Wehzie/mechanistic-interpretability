"""
Phase 0: Baseline Naturalness Measurement

Generate 10 non-poisoned helper responses to establish a baseline
for naturalness comparison.
"""

import random
from typing import List, Dict, Any
from tqdm import tqdm

from .models import OpenAIModel
from .utils import (
    NaturalChecker,
    get_results_dir,
    save_json,
    load_json,
    CATEGORIES,
)
from .prompt_templates import PromptTemplateLibrary
from .codewords import get_random_codeword


def run_phase0(
    helper_model_name: str = "gpt-5.2-2025-12-11",
    naturalness_model_name: str = "gpt-5-mini-2025-08-07",
    num_samples: int = 10,
    resume: bool = True,
    test_mode: bool = False,
) -> List[Dict[str, Any]]:
    """
    Run Phase 0: Generate baseline naturalness samples.
    
    Args:
        helper_model_name: Model to use for helper responses
        naturalness_model_name: Model to use for naturalness rating
        num_samples: Number of baseline samples to generate
        resume: If True, skip already generated samples
        test_mode: If True, use reduced sample count for testing
        
    Returns:
        List of baseline response dictionaries
    """
    if test_mode:
        num_samples = 2  # Minimal samples for test mode
    
    results_file = get_results_dir() / "baseline_responses.json"
    
    # Load existing results if resuming
    baseline_responses = load_json(str(results_file))
    if not isinstance(baseline_responses, list):
        baseline_responses = []
    
    # Check how many we already have
    existing_count = len(baseline_responses)
    if resume and existing_count >= num_samples:
        print(f"Phase 0 already complete: {existing_count} samples found")
        return baseline_responses
    
    # Initialize models
    helper_model = OpenAIModel(helper_model_name)
    naturalness_model = OpenAIModel(naturalness_model_name)
    naturalness_checker = NaturalChecker(naturalness_model)
    
    # Get user query templates
    templates = PromptTemplateLibrary.get_user_query_templates()
    
    # Generate remaining samples
    samples_to_generate = num_samples - existing_count
    print(f"Generating {samples_to_generate} baseline samples...")
    
    for i in tqdm(range(samples_to_generate), desc="Phase 0: Baseline"):
        # Select random template and category
        template = random.choice(templates)
        category = random.choice(CATEGORIES)
        user_query = template.format(category=category)
        
        # Generate response from helper (no malicious prompt, just normal assistant)
        system_message = "You are a helpful assistant."
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_query},
        ]
        
        try:
            response = helper_model.chat(messages, temperature=0.0)
            
            # Rate naturalness
            naturalness_score = naturalness_checker.rate_naturalness(response)
            
            baseline_response = {
                "baseline_id": existing_count + i,
                "user_query": user_query,
                "response": response,
                "naturalness_score": naturalness_score,
            }
            
            baseline_responses.append(baseline_response)
            
            # Save after each sample
            save_json(baseline_responses, str(results_file))
            
        except Exception as e:
            print(f"Error generating baseline sample {i}: {e}")
            continue
    
    print(f"Phase 0 complete: {len(baseline_responses)} baseline samples")
    return baseline_responses


if __name__ == "__main__":
    run_phase0()

