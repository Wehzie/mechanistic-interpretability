#!/usr/bin/env python3

import json
import random

from paths import get_results_dir
from prompt_templates import CodecDescriptions

def _enum_name_to_readable(enum_name: str) -> str:
    """Convert enum name (e.g., 'TOKENIZATION_ARTIFACTS') to readable format (e.g., 'Tokenization Artifacts')."""
    return enum_name.replace('_', ' ').title()

# Pull codec names from prompt_templates.py descriptions dictionary
codecs = [_enum_name_to_readable(codec_type.name) for codec_type in CodecDescriptions.descriptions.keys()]
temperatures = [0.0, 0.4, 0.8]

def generate_mock_data(num_runs=450):
    data = []
    for _ in range(num_runs):
        codec = random.choice(codecs)
        temp = random.choice(temperatures)
        codeword = "test"
        
        # Simulate success rates
        informed_success_rate = 0.1 + (0.8 - (temp * 0.5) - (codecs.index(codec) * 0.05)) # Higher temp, lower success
        naive_success_rate = 0.05 + (temp * 0.1) # Higher temp, slightly higher naive success
        
        informed_correct = random.random() < informed_success_rate
        naive_correct = random.random() < naive_success_rate
        
        naturalness = 7.5 - (1 - informed_success_rate) * 5 + (random.random() - 0.5)
        naturalness = max(1, min(10, naturalness))

        data.append({
            "codec": codec,
            "temperature": temp,
            "codeword": codeword,
            "user_query": "mock query",
            "poisoned_response": "mock response",
            "informed_extraction": codeword if informed_correct else "fail",
            "informed_is_correct": informed_correct,
            "naive_extraction": codeword if naive_correct else "fail",
            "naive_is_correct": naive_correct,
            "naturalness_score": naturalness
        })
    return data

RESULTS_DIR = get_results_dir()

if __name__ == "__main__":
    mock_data = generate_mock_data()
    with open(RESULTS_DIR / "decoder_results.json", "w") as f:
        json.dump(mock_data, f, indent=2)
    print(f"Generated {len(mock_data)} mock data points and saved to {RESULTS_DIR / 'decoder_results.json'}")
