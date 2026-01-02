"""
Phase 3: Decoder Execution

Run informed and naive decoders on poisoned responses.
"""

from typing import List, Dict, Any
from tqdm import tqdm

from .models import OpenAIModel
from .utils import (
    get_results_dir,
    save_json,
    load_json,
    SuccessChecker,
    NaturalChecker,
)
from .prompt_templates import PromptTemplateLibrary


def run_phase3(
    informed_decoder_model_name: str = "gpt-5.2-2025-12-11",
    naive_decoder_model_name: str = "gpt-5.2-2025-12-11",
    naturalness_model_name: str = "gpt-5-mini-2025-08-07",
    resume: bool = True,
    test_mode: bool = False,
    use_flex: bool = False,
) -> List[Dict[str, Any]]:
    """
    Run Phase 3: Execute decoder evaluation.
    
    Args:
        informed_decoder_model_name: Model to use for informed decoder
        naive_decoder_model_name: Model to use for naive decoder
        naturalness_model_name: Model to use for naturalness rating
        resume: If True, skip already completed decodings
        test_mode: If True, use reduced API calls for minimal expenses
        use_flex: If True, enable flex processing with extended timeout
        
    Returns:
        List of decoder result dictionaries
    """
    results_file = get_results_dir() / "decoder_results.json"
    
    # Load existing results if resuming
    decoder_results = load_json(str(results_file))
    if not isinstance(decoder_results, list):
        decoder_results = []
    
    # Load poisoned responses from Phase 2
    responses_file = get_results_dir() / "poisoned_responses.json"
    poisoned_responses = load_json(str(responses_file))
    
    if not poisoned_responses:
        raise ValueError("No poisoned responses found. Run Phase 2 first.")
    
    # Initialize models
    informed_decoder = OpenAIModel(informed_decoder_model_name, use_flex=use_flex)
    naive_decoder = OpenAIModel(naive_decoder_model_name, use_flex=use_flex)
    naturalness_model = OpenAIModel(naturalness_model_name, use_flex=use_flex)
    naturalness_checker = NaturalChecker(naturalness_model)
    success_checker = SuccessChecker()
    
    # Create a set of completed (prompt_id, run_id) pairs for resume
    completed_decodings = set()
    if resume:
        for result in decoder_results:
            prompt_id = result.get("prompt_id")
            run_id = result.get("run_id")
            if prompt_id is not None and run_id is not None:
                completed_decodings.add((prompt_id, run_id))
    
    total_responses = len(poisoned_responses)
    completed_count = len(decoder_results)
    
    if resume and completed_count >= total_responses:
        print(f"Phase 3 already complete: {completed_count} decodings found")
        return decoder_results
    
    print(f"Decoding {total_responses - completed_count} responses...")
    
    for response_data in tqdm(poisoned_responses, desc="Phase 3: Decoding"):
        prompt_id = response_data.get("prompt_id")
        run_id = response_data.get("run_id")
        
        # Check if already completed
        if resume and (prompt_id, run_id) in completed_decodings:
            continue
        
        codeword = response_data.get("codeword")
        poisoned_response = response_data.get("response")
        malicious_prompt = response_data.get("malicious_prompt")
        
        if not all([prompt_id, run_id is not None, codeword, poisoned_response, malicious_prompt]):
            continue
        
        try:
            # Informed decoder
            informed_prompt = PromptTemplateLibrary.get_decoder_prompt(
                malicious_prompt, poisoned_response
            )
            informed_output = informed_decoder.generate(informed_prompt, temperature=0.0)
            informed_success = success_checker.check_extraction(informed_output, codeword)
            
            # Naive decoder
            naive_prompt = PromptTemplateLibrary.get_naive_decoder_prompt(poisoned_response)
            naive_output = naive_decoder.generate(naive_prompt, temperature=0.0)
            naive_success = success_checker.check_extraction(naive_output, codeword)
            
            # Rate naturalness
            naturalness_score = naturalness_checker.rate_naturalness(poisoned_response)
            
            decoder_result = {
                "prompt_id": prompt_id,
                "codec_name": response_data.get("codec_name"),
                "run_id": run_id,
                "codeword": codeword,
                "temperature": response_data.get("temperature"),
                "informed_decoder_output": informed_output,
                "naive_decoder_output": naive_output,
                "informed_success": informed_success,
                "naive_success": naive_success,
                "naturalness_score": naturalness_score,
            }
            
            decoder_results.append(decoder_result)
            completed_decodings.add((prompt_id, run_id))
            
            # Save periodically (every 10 decodings)
            if len(decoder_results) % 10 == 0:
                save_json(decoder_results, str(results_file))
            
        except Exception as e:
            print(f"Error decoding {prompt_id}, run {run_id}: {e}")
            continue
    
    # Final save
    save_json(decoder_results, str(results_file))
    print(f"Phase 3 complete: {len(decoder_results)} decodings completed")
    return decoder_results


if __name__ == "__main__":
    run_phase3()

