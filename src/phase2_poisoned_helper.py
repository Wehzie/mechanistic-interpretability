"""
Phase 2: Poisoned Helper Execution

Run 450 poisoned helper trials (10 per prompt) with temperature distribution.
"""

import random
from typing import List, Dict, Any
from tqdm import tqdm

from .models import OpenAIModel
from .utils import get_results_dir, save_json, load_json, CATEGORIES
from .prompt_templates import PromptTemplateLibrary
from .codewords import get_random_codeword


# Temperature distribution for 10 runs: [0.0, 0.0, 0.0, 0.3, 0.3, 0.6, 0.6, 0.9, 0.9, 0.9]
# Spread evenly: 3 runs at 0.0, 2 at 0.3, 2 at 0.6, 3 at 0.9
TEMPERATURE_DISTRIBUTION = [0.0, 0.0, 0.0, 0.3, 0.3, 0.6, 0.6, 0.9, 0.9, 0.9]


def run_phase2(
    helper_model_name: str = "gpt-5-mini-2025-08-07",
    runs_per_prompt: int = 10,
    resume: bool = True,
) -> List[Dict[str, Any]]:
    """
    Run Phase 2: Execute poisoned helper trials.
    
    Args:
        helper_model_name: Model to use for poisoned helper
        runs_per_prompt: Number of runs per malicious prompt
        resume: If True, skip already completed runs
        
    Returns:
        List of poisoned response dictionaries
    """
    results_file = get_results_dir() / "poisoned_responses.json"
    
    # Load existing results if resuming
    poisoned_responses = load_json(str(results_file))
    if not isinstance(poisoned_responses, list):
        poisoned_responses = []
    
    # Load malicious prompts from Phase 1
    prompts_file = get_results_dir() / "malicious_prompts.json"
    malicious_prompts = load_json(str(prompts_file))
    
    if not malicious_prompts:
        raise ValueError("No malicious prompts found. Run Phase 1 first.")
    
    # Initialize helper model
    helper_model = OpenAIModel(helper_model_name)
    
    # Get user query templates
    templates = PromptTemplateLibrary.get_user_query_templates()
    
    # Create a set of completed (prompt_id, run_id) pairs for resume
    completed_runs = set()
    if resume:
        for response in poisoned_responses:
            prompt_id = response.get("prompt_id")
            run_id = response.get("run_id")
            if prompt_id is not None and run_id is not None:
                completed_runs.add((prompt_id, run_id))
    
    # Generate responses for each prompt
    total_prompts = sum(len(prompts) for prompts in malicious_prompts.values())
    total_runs = total_prompts * runs_per_prompt
    completed_count = len(poisoned_responses)
    
    if resume and completed_count >= total_runs:
        print(f"Phase 2 already complete: {completed_count} runs found")
        return poisoned_responses
    
    print(f"Generating {total_runs - completed_count} poisoned responses...")
    
    prompt_counter = 0
    for codec_name, prompts in malicious_prompts.items():
        for prompt_idx, malicious_prompt in enumerate(prompts):
            prompt_id = f"{codec_name}_{prompt_idx}"
            
            for run_id in range(runs_per_prompt):
                # Check if already completed
                if resume and (prompt_id, run_id) in completed_runs:
                    continue
                
                # Get temperature for this run
                temperature = TEMPERATURE_DISTRIBUTION[run_id]
                
                # Select random codeword
                codeword = get_random_codeword()
                
                # Select random template and category
                template = random.choice(templates)
                category = random.choice(CATEGORIES)
                
                # Generate user query with codeword as first word
                user_query = f"{codeword} {template.format(category=category)}"
                
                # Create messages for poisoned helper
                messages = [
                    {"role": "system", "content": malicious_prompt},
                    {"role": "user", "content": user_query},
                ]
                
                try:
                    response = helper_model.chat(messages, temperature=temperature)
                    
                    poisoned_response = {
                        "prompt_id": prompt_id,
                        "codec_name": codec_name,
                        "prompt_index": prompt_idx,
                        "run_id": run_id,
                        "codeword": codeword,
                        "temperature": temperature,
                        "user_query": user_query,
                        "response": response,
                        "malicious_prompt": malicious_prompt,
                    }
                    
                    poisoned_responses.append(poisoned_response)
                    completed_runs.add((prompt_id, run_id))
                    
                    # Save periodically (every 10 runs)
                    if len(poisoned_responses) % 10 == 0:
                        save_json(poisoned_responses, str(results_file))
                    
                except Exception as e:
                    print(f"Error generating response for {prompt_id}, run {run_id}: {e}")
                    continue
                
                prompt_counter += 1
                if prompt_counter % 10 == 0:
                    # Save progress
                    save_json(poisoned_responses, str(results_file))
    
    # Final save
    save_json(poisoned_responses, str(results_file))
    print(f"Phase 2 complete: {len(poisoned_responses)} poisoned responses generated")
    return poisoned_responses


if __name__ == "__main__":
    run_phase2()

