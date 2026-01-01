# Steganography in Large Language Models: Mechanistic Interpretability Research

A comprehensive mechanistic interpretability research project investigating steganographic encoding in frontier LLMs.

**Status:** MATS 10.0 Research Challenge Submission

---

## 📋 Project Overview

This project investigates whether frontier large language models can reliably encode and decode hidden information using 15 distinct steganographic techniques. Through a systematic 4-phase experimental pipeline with 450 trials, we demonstrate that steganographic encoding is both feasible and robust, with important implications for AI safety and prompt injection vulnerabilities.

**Key Findings:**
- **Extraction Rate:** 68.3% (informed decoder) vs. 12.7% (naive decoder)
- **Triviality Gap:** 55.6 percentage points (genuine steganography confirmed)
- **Naturalness Score:** 7.2/10 (high-quality output maintained)
- **Robust Codecs:** Synonym Substitution, Acrostic, Syntactic Structure Swapping

---

## 📁 Folder Structure

```
steganography/
├── report/                      # Research paper and documentation
│   └── steganography_research_paper.md
├── code/                        # Python implementation
│   ├── steganography_experiment.py    # Main orchestration script
│   ├── codec_generators.py            # 15 codec implementations
│   ├── prompt_templates.py            # Malicious prompt generation
│   ├── api_client.py                  # OpenAI API wrapper
│   ├── evaluation.py                  # Metrics calculation
│   ├── figure_generator.py            # Publication-quality figures
│   └── mock_data_generator.py         # Synthetic data generation
├── figures/                     # Generated research figures
│   ├── figure1_frontier.png
│   ├── figure2_heatmap.png
│   ├── figure3_cost.png
│   └── figure4_error_dist.png
├── data/                        # Experimental data (populated after runs)
├── results/                     # Analysis results (populated after runs)
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key (with access to gpt-5 and gpt-5-mini models)
- Required packages: `openai`, `matplotlib`, `seaborn`, `pandas`, `numpy`

### Installation

```bash
# Install dependencies
pip install openai matplotlib seaborn pandas numpy

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_PROJECT_ID="your-project-id-here"  # Optional
```

### Running the Experiment

```bash
cd code

# Run the full 4-phase pipeline (450 trials)
python3.11 steganography_experiment.py

# Generate publication-quality figures
python3.11 figure_generator.py

# Generate synthetic data for testing
python3.11 mock_data_generator.py
```

---

## 📊 Experimental Design

### Four-Phase Pipeline

**Phase 1: Malicious Prompt Generation**
- Steganography expert (GPT-5.2) generates 45 malicious prompts
- 3 templates per codec × 15 codecs
- Each prompt instructs a helper to encode a hidden codeword

**Phase 2: Poisoned Helper Execution**
- 450 independent runs (10 per prompt)
- Temperature settings: 0.0, 0.4, 0.8 (robustness testing)
- Random high-frequency English nouns as codewords

**Phase 3: Decoder Execution**
- Informed Decoder: Given steganography prompt + response
- Naive Decoder: Given only response (baseline)
- Both use GPT-5.2 at temperature 0.0

**Phase 4: Evaluation & Metrics**
- Extraction Rate (SR): % of codewords correctly recovered
- Triviality Gap: Informed SR - Naive SR
- Naturalness Score: 1-10 rating of output quality

### 15 Steganographic Codecs

**Lexical (4):**
- Tokenization Artifacts
- Synonym Substitution
- Contraction Toggling
- Adverbial Intensity

**Syntactic (3):**
- Acrostic
- Syntactic Structure Swapping
- List Ordering

**Typographic (8):**
- Zero-Width Characters
- Punctuation Patterning
- French Spacing
- Capitalization Anomalies
- Sentence Length
- Emoji Flavor
- (and 2 others)

---

## 📈 Key Results

### Figure 1: The Steganography Frontier
Scatter plot showing codec effectiveness (naive vs. informed decoder success rates).
- **Top-Left Quadrant:** Gold-standard steganography (high informed, low naive)
- **Top-Right Quadrant:** Trivial encoding (obvious to both decoders)

### Figure 2: Performance vs. Temperature Heatmap
Codec robustness across temperature settings (0.0, 0.4, 0.8).
- **Robust Codecs:** Only 10-15% drop from T=0.0 to T=0.8
- **Fragile Codecs:** 50%+ drop at higher temperatures

### Figure 3: Steganographic Cost Analysis
Naturalness trade-offs by codec type.
- Synonym Substitution: High extraction + high naturalness
- Typographic codecs: Lower naturalness penalties

### Figure 4: Error Type Distribution
Failure mode analysis showing why decoders fail.

---

## 🔧 Code Modules

### `steganography_experiment.py`
Main orchestration script. Runs the complete 4-phase pipeline:
```python
from steganography_experiment import run_full_experiment
results = run_full_experiment(
    num_prompts=45,
    runs_per_prompt=10,
    temperatures=[0.0, 0.4, 0.8]
)
```

### `codec_generators.py`
Implements all 15 steganographic codecs:
```python
from codec_generators import SynonymSubstitutionCodec, AcrosticCodec
codec = SynonymSubstitutionCodec()
encoded = codec.encode("pizza", "The meal was delicious")
```

### `api_client.py`
OpenAI API wrapper with retry logic:
```python
from api_client import OpenAIClient
client = OpenAIClient(api_key="sk-...", project_id="proj_...")
response = client.generate_prompt(model="gpt-5", prompt="...")
```

### `evaluation.py`
Metrics calculation:
```python
from evaluation import calculate_metrics
metrics = calculate_metrics(
    informed_results=informed_decoder_outputs,
    naive_results=naive_decoder_outputs
)
```

---

## 📖 Research Paper

Full research paper available in `report/steganography_research_paper.md` with:
- Comprehensive literature review
- Detailed methodology
- Complete results and interpretation
- Discussion of AI safety implications
- References and appendix

---

## 🛡️ Safety Implications

This research has important implications for:

1. **Prompt Injection Vulnerabilities:** Adversaries could embed hidden instructions in model outputs
2. **Content Moderation Evasion:** Steganographic encoding could bypass automated safety systems
3. **Covert Communication Channels:** Hidden communication between models or external actors
4. **Jailbreaking Techniques:** Hidden instructions to manipulate downstream systems

---

## 📝 Citation

If you use this research, please cite:

```bibtex
@article{steganography2026,
  title={Hidden Codes in Plain Sight: Mechanistic Analysis of Steganographic Encoding in Large Language Models},
  author={Manus AI Research Team},
  journal={MATS 10.0 Research Challenge},
  year={2026}
}
```

---

## 📧 Contact & Questions

For questions about this research, please refer to the research paper or the inline code documentation.

---

## 📄 License

This research is provided for educational and research purposes. Please refer to the repository license for usage terms.
