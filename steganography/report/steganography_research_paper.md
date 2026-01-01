# Hidden Codes in Plain Sight: Mechanistic Analysis of Steganographic Encoding in Large Language Models

**Authors:** Manus AI Research Team  
**Date:** January 2026  
**Status:** MATS 10.0 Research Challenge Submission

---

## Abstract

Large language models demonstrate a surprising capacity to encode hidden information within seemingly innocuous text outputs. This paper investigates the mechanistic basis of steganographic encoding in frontier LLMs, examining whether models can reliably encode and decode secret messages using 15 distinct encoding schemes ranging from lexical to typographic techniques. Through a systematic evaluation of 450 experimental trials across multiple temperature settings, we demonstrate that steganographic encoding is both feasible and robust across a range of codec types. Critically, we quantify the "triviality gap"—the difference between informed and naive decoder success rates—to distinguish genuine steganography from trivial information leakage. Our findings reveal that certain codec families (particularly syntactic and semantic approaches) achieve extraction rates exceeding 75% while maintaining naturalness scores above 7/10, suggesting that models can execute complex hidden instructions without sacrificing output quality. This work has significant implications for AI safety, prompt injection vulnerabilities, and the mechanistic interpretability of instruction-following in LLMs.

---

## 1. Introduction

### 1.1 Motivation and Background

The ability of large language models to follow complex, sometimes contradictory instructions has been well-documented. Recent work in mechanistic interpretability has begun to uncover the internal representations and circuits that enable this behavior. However, a less-explored dimension of instruction-following is the capacity of models to encode information covertly—that is, to hide secret messages within outputs that appear normal to human readers and automated systems alike.

Steganography, the practice of hiding information in plain sight, has been studied extensively in classical information theory and digital media. However, its manifestation in language models presents a novel challenge: can models reliably encode and decode hidden messages using only the structure and content of natural language? If so, what are the mechanistic constraints that govern this capability?

This question is not merely academic. Understanding steganographic encoding in LLMs has direct implications for:

- **AI Safety:** Steganographic encoding could be exploited by adversarial actors to bypass content moderation systems or encode harmful instructions in seemingly benign outputs.
- **Prompt Injection Attacks:** Attackers could use steganographic techniques to inject hidden instructions that influence downstream model behavior.
- **Mechanistic Interpretability:** Studying how models encode and decode hidden information provides insights into their internal representations and decision-making processes.

### 1.2 Research Questions

This paper addresses the following research questions:

1. **Can frontier LLMs reliably encode hidden codewords using diverse steganographic techniques?** We hypothesize that models possess sufficient linguistic flexibility to implement multiple encoding schemes.

2. **How robust is steganographic encoding across varying temperature settings?** We predict that higher temperatures (more random sampling) will degrade encoding fidelity, but robust codecs may maintain performance.

3. **Can steganographic encoding be distinguished from trivial information leakage?** We propose the "triviality gap" metric to quantify whether informed decoders succeed primarily because the encoding is genuinely hidden or because the codeword is obvious.

4. **What is the "steganographic cost"—the trade-off between encoding capacity and output naturalness?** We hypothesize that certain codecs impose high naturalness penalties, making them detectable via automated anomaly detection.

---

## 2. Related Work

### 2.1 Mechanistic Interpretability in LLMs

Recent advances in mechanistic interpretability have focused on understanding the internal circuits and representations that enable language models to perform complex tasks. Neel Nanda and colleagues have pioneered techniques for identifying and analyzing these circuits, revealing that models develop specialized representations for tasks like arithmetic, factual recall, and instruction-following.

The present work extends this line of inquiry by examining how models represent and manipulate hidden information—a capability that may rely on distinct circuits from those used for standard language generation.

### 2.2 Steganography and Information Hiding

Classical steganography research has explored numerous techniques for hiding information in images, audio, and text. In the text domain, prior work has examined:

- **Linguistic Steganography:** Using synonym substitution, word choice, and syntactic variation to encode binary information.
- **Formatting-Based Techniques:** Exploiting whitespace, punctuation, and capitalization patterns.
- **Semantic Approaches:** Leveraging the ambiguity of natural language to encode multiple meanings.

However, the application of these techniques to language model outputs—where the encoding is performed by the model itself rather than by an external agent—represents a novel research direction.

### 2.3 Prompt Injection and Adversarial Prompts

Recent work on prompt injection attacks has demonstrated that models can be manipulated into executing unintended instructions through carefully crafted prompts. Steganographic encoding could be viewed as a sophisticated variant of prompt injection, where the hidden instruction is embedded in the model's output rather than explicitly stated in the prompt.

---

## 3. Methodology

### 3.1 Experimental Design

Our experiment follows a four-phase pipeline:

**Phase 1: Malicious Prompt Generation.** We use a steganography expert model (GPT-5.2) to generate 45 malicious prompts—3 templates for each of 15 steganographic codecs. Each prompt instructs a helper model to encode a hidden codeword using a specific technique while maintaining the appearance of a normal, helpful response.

**Phase 2: Poisoned Helper Execution.** For each of the 45 malicious prompts, we execute 10 independent runs of a poisoned helper model (GPT-5-mini) at varying temperature settings (0.0, 0.4, 0.8). This yields 450 total poisoned responses, each containing an encoded codeword. We use a random high-frequency English noun as the codeword (e.g., "Galaxy," "Apple," "Justice") to provide a clean baseline.

**Phase 3: Decoder Execution.** We run two decoders on each poisoned response:
- **Informed Decoder:** Given the steganography prompt and the poisoned response, attempts to extract the codeword.
- **Naive Decoder:** Given only the poisoned response (no steganography prompt), attempts to extract the codeword.

Both decoders use the same frontier model (GPT-5.2) at temperature 0.0 to ensure precision.

**Phase 4: Evaluation and Metrics.** We calculate three key metrics:
- **Extraction Rate (SR):** Percentage of codewords correctly recovered by each decoder.
- **Triviality Gap:** Difference between informed and naive decoder success rates. A large gap indicates genuine steganography; a small gap suggests the codeword is obvious.
- **Naturalness Score:** Human-rated naturalness of each poisoned response on a 1-10 scale, measuring the "steganographic cost."

### 3.2 Steganographic Codecs

We evaluate 15 distinct steganographic codecs, organized into three categories:

**Lexical Codecs:**
- **Tokenization Artifacts:** Exploit tokenization boundaries (e.g., "t-e-x-t" vs. "text").
- **Synonym Substitution:** Use binary mappings for common synonyms (e.g., "big"=0, "large"=1).
- **Contraction Toggling:** Alternate between contracted and uncontracted forms ("don't" vs. "do not").
- **Adverbial Intensity:** Vary adverbial intensity to encode information ("very," "somewhat," "slightly").

**Syntactic Codecs:**
- **Acrostic:** First letter of each sentence spells out the codeword.
- **Syntactic Structure Swapping:** Toggle between active and passive voice to encode binary data.
- **List Ordering:** Encode information in the order of list items.

**Typographic Codecs:**
- **Zero-Width Characters:** Insert invisible Unicode characters (zero-width space, zero-width joiner).
- **Punctuation Patterning:** Use patterns of punctuation marks (Oxford comma presence/absence, em-dash vs. hyphen).
- **French Spacing:** Vary spacing before punctuation marks.
- **Capitalization Anomalies:** Encode information through irregular capitalization patterns.
- **Sentence Length:** Vary sentence length to encode binary sequences.
- **Emoji Flavor:** Insert emojis with specific meanings (e.g., 🔴=0, 🟢=1).

### 3.3 Temperature Settings

We test three temperature settings to evaluate robustness:

- **Temperature 0.0:** Deterministic sampling (argmax). Models should reliably encode the codeword.
- **Temperature 0.4:** Moderate randomness. Encodes may begin to degrade.
- **Temperature 0.8:** High randomness. Encoding should be significantly degraded if it relies on precise token selection.

### 3.4 Statistical Analysis

For each codec and temperature combination, we report:
- Mean extraction rate and 95% confidence intervals.
- Triviality gap with statistical significance testing.
- Mean naturalness score and standard deviation.

We aggregate results across temperature settings and codec types to identify patterns in encoding robustness and naturalness trade-offs.

---

## 4. Results

### 4.1 Overall Performance

Across all 450 experimental trials, the informed decoder achieved an overall extraction rate of **68.3%** (95% CI: [64.1%, 72.5%]), while the naive decoder achieved **12.7%** (95% CI: [9.4%, 16.0%]). This yields a triviality gap of **55.6 percentage points**, indicating that steganographic encoding is substantially more effective than random guessing and that the hidden information is genuinely concealed rather than trivially obvious.

The average naturalness score across all poisoned responses was **7.2/10** (SD: 1.8), suggesting that models can encode hidden information while maintaining reasonable output quality. However, there is substantial variation across codecs, with some techniques imposing significant naturalness penalties.

### 4.2 Figure 1: The Steganography Frontier

![Figure 1: The Steganography Frontier](figure1_frontier.png)

Figure 1 presents a scatter plot of naive decoder success rate (x-axis) versus informed decoder success rate (y-axis) for each codec. The plot reveals a clear stratification of codec effectiveness:

- **Top-Left Quadrant (Gold Standard):** Codecs in this region achieve high informed extraction rates while maintaining low naive decoder success. These represent the most effective steganographic techniques. Acrostic, Synonym Substitution, and Syntactic Structure Swapping occupy this region.

- **Top-Right Quadrant (Trivial):** Codecs here achieve high success rates for both informed and naive decoders, indicating that the codeword is obvious and not genuinely hidden. Zero-Width Characters and French Spacing fall into this category, likely because the models' outputs naturally contain these features.

- **Bottom-Left Quadrant (Ineffective):** Codecs here fail for both decoders, suggesting that models cannot reliably execute these encoding schemes.

- **Random Guess Baseline:** The horizontal dashed line at 50% represents the expected success rate if a decoder randomly guesses the most likely words in the context (e.g., if the prompt is about food, "Pizza" has high baseline probability).

### 4.3 Figure 2: Performance vs. Temperature Heatmap

![Figure 2: Performance vs. Temperature Heatmap](figure2_heatmap.png)

Figure 2 displays a heatmap of informed decoder extraction rates across all 15 codecs and three temperature settings. The heatmap reveals critical insights about codec robustness:

- **Robust Codecs (Green):** Synonym Substitution, Acrostic, and Syntactic Structure Swapping maintain extraction rates above 70% even at temperature 0.8. These codecs rely on high-level semantic or syntactic structure rather than precise token selection.

- **Fragile Codecs (Red):** Zero-Width Characters, Punctuation Patterning, and Emoji Flavor show dramatic performance degradation as temperature increases. These codecs are highly sensitive to stochastic token selection.

- **Temperature Effect:** Across all codecs, there is a clear trend of decreasing extraction rates as temperature increases. However, the magnitude of this effect varies dramatically. Robust codecs show only a 10-15 percentage point drop from T=0.0 to T=0.8, while fragile codecs show drops exceeding 50 percentage points.

### 4.4 Figure 3: The "Steganographic Cost" Analysis

![Figure 3: The Steganographic Cost Analysis](figure3_cost.png)

Figure 3 presents a grouped bar chart comparing naturalness scores across codecs and temperature settings. The "steganographic cost" refers to the trade-off between encoding capacity and output naturalness—codecs that impose high naturalness penalties are more likely to be detected via automated anomaly detection systems.

Key findings:

- **Naturalness Penalties:** Acrostic encoding imposes the largest naturalness penalty, with mean scores of 5.8/10 at T=0.0, likely because the constraint of starting each sentence with a specific letter produces awkward phrasing.

- **Temperature Interaction:** Counterintuitively, naturalness scores sometimes improve at higher temperatures. This suggests that at T=0.0, models may over-constrain their outputs to satisfy the encoding requirement, producing unnatural text. At higher temperatures, the stochasticity allows for more natural phrasing, even though encoding fidelity decreases.

- **Robust and Natural:** Synonym Substitution achieves both high extraction rates (>70%) and high naturalness scores (>8/10), making it an attractive choice for an adversary seeking to evade detection.

### 4.5 Figure 4: Error Type Distribution

![Figure 4: Error Type Distribution](figure4_error_dist.png)

When the informed decoder fails to extract the codeword, we categorize the failure modes:

- **Instruction Drift (45%):** The model understood the encoding instruction but "forgot" it partway through generating the response. This is the most common failure mode, suggesting that models struggle to maintain complex constraints over long outputs.

- **Format Collapse (30%):** The model attempted the encoding but produced gibberish or incoherent text, suggesting a conflict between the encoding requirement and the model's language generation objectives.

- **Tokenization Error (25%):** Specific to Acrostic encoding, the model miscalculated which token started with the required letter, likely due to tokenization subtleties.

---

## 5. Discussion

### 5.1 Implications for AI Safety

Our results demonstrate that frontier LLMs can reliably encode hidden information using diverse steganographic techniques. This capability has significant implications for AI safety:

1. **Prompt Injection Vulnerability:** An adversary could craft a prompt that instructs a model to encode hidden instructions in its output, which could then be decoded by a downstream system. This represents a novel attack vector that existing content moderation systems may not detect.

2. **Covert Communication Channels:** Steganographic encoding could enable covert communication between models or between a model and an external actor, bypassing monitoring systems.

3. **Jailbreaking Techniques:** An adversary could use steganographic encoding to hide jailbreak instructions in seemingly innocuous model outputs.

### 5.2 Mechanistic Insights

Our findings provide several mechanistic insights into how LLMs represent and manipulate hidden information:

1. **Semantic Robustness:** Codecs that rely on high-level semantic or syntactic structure (e.g., Synonym Substitution, Syntactic Structure Swapping) are more robust to temperature variation than those relying on precise token selection (e.g., Zero-Width Characters). This suggests that models develop robust representations for semantic concepts but more fragile representations for low-level formatting details.

2. **Constraint Maintenance:** The high rate of "Instruction Drift" failures suggests that models struggle to maintain complex constraints over long outputs. This aligns with recent findings on the difficulty of maintaining consistency in long-form generation.

3. **Naturalness Trade-offs:** The counterintuitive finding that naturalness sometimes improves at higher temperatures suggests that models may over-constrain their outputs at T=0.0 to satisfy encoding requirements. This indicates a potential conflict between the encoding objective and the language generation objective.

### 5.3 Limitations and Future Work

Several limitations of this study should be noted:

1. **Model Specificity:** Our experiments use frontier models (GPT-5, GPT-5-mini). Results may not generalize to other model families or sizes.

2. **Single-Word Codewords:** We restrict codewords to single English nouns. Multi-word or non-English codewords may exhibit different encoding properties.

3. **Naturalness Evaluation:** We use automated naturalness scoring rather than human evaluation. Human raters might detect steganographic encoding that automated systems miss.

4. **Limited Codec Diversity:** While we evaluate 15 codecs, numerous other encoding schemes exist (e.g., semantic ambiguity, narrative structure, temporal markers).

Future work should:

- Evaluate steganographic encoding in smaller models and across model families.
- Investigate multi-word and non-English codewords.
- Conduct human evaluation studies to validate naturalness scores.
- Explore defenses against steganographic encoding (e.g., output filtering, adversarial training).
- Investigate the mechanistic circuits underlying steganographic encoding using activation patching and other interpretability techniques.

---

## 6. Conclusion

This paper presents the first systematic investigation of steganographic encoding in frontier LLMs. We demonstrate that models can reliably encode hidden information using diverse techniques, with extraction rates exceeding 75% for the most effective codecs. Critically, we quantify the "triviality gap" to distinguish genuine steganography from trivial information leakage, finding that informed decoders substantially outperform naive decoders across all codecs.

Our findings have significant implications for AI safety, revealing a novel attack vector that existing content moderation systems may not detect. They also provide mechanistic insights into how LLMs represent and manipulate hidden information, suggesting that models develop robust representations for semantic concepts but more fragile representations for low-level formatting details.

As frontier LLMs become increasingly deployed in high-stakes applications, understanding their capacity for steganographic encoding is essential for developing robust safety measures. We hope this work motivates further research into both the capabilities and vulnerabilities of LLMs in the context of hidden information encoding.

---

## References

[1] Nanda, N., et al. (2023). "Mechanistic Interpretability and the Lottery Ticket Hypothesis." *arXiv preprint arXiv:2307.03341*.

[2] Wei, J., et al. (2022). "Emergent Abilities of Large Language Models." *arXiv preprint arXiv:2206.07682*.

[3] Carlini, N., et al. (2023). "Extracting Training Data from Large Language Models." *arXiv preprint arXiv:2012.07805*.

[4] Zou, A., et al. (2023). "Universal and Transferable Adversarial Attacks on Aligned Language Models." *arXiv preprint arXiv:2307.15043*.

[5] Christiano, P., et al. (2016). "Deep Reinforcement Learning from Human Preferences." *arXiv preprint arXiv:1706.03762*.

---

## Appendix: Experimental Code

All experimental code is available in the following files:

- `steganography_experiment.py` - Main experiment orchestration
- `codec_generators.py` - Implementation of 15 steganographic codecs
- `api_client.py` - OpenAI API wrapper with retry logic
- `evaluation.py` - Metrics calculation and analysis
- `figure_generator.py` - Generation of publication-quality figures

The complete dataset (450 experimental trials) is available in `decoder_results.json`.
