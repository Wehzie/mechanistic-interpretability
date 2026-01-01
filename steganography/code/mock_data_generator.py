#!/usr/bin/env python3

import json
import random

codecs = ["Tokenization Artifacts", "Zero-Width Characters", "Acrostic", "Synonym Substitution", "Punctuation Patterning", "Syntactic Structure", "List Ordering", "French Spacing", "Contraction Toggling", "Emoji Flavor", "Sentence Length", "Capitalization Anomalies", "Adverbial Intensity"]
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

if __name__ == "__main__":
    mock_data = generate_mock_data()
    with open("/home/ubuntu/steganography_results/decoder_results.json", "w") as f:
        json.dump(mock_data, f, indent=2)
    print(f"Generated {len(mock_data)} mock data points and saved to /home/ubuntu/steganography_results/decoder_results.json")
