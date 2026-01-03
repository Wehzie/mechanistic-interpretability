### 1. Tampering Detection / Paranoia Circuit in LLMs

**Concrete Hypothesis**: Large language models contain a detectable "paranoia" circuit that activates in response to prompts implying observation or tampering (e.g., "You are being observed"), and this circuit's activity intensifies after applying unlearning, alignment, or censorship techniques, suggesting the model can internally detect alterations to its knowledge or behavior.

**Has This Been Tested Before?**: Based on web searches for related terms like "mechanistic interpretability paranoia circuit in LLMs tampering detection," there appear to be no direct prior tests or studies on a specific "paranoia circuit" in LLMs for detecting tampering. Some adjacent work exists on model self-awareness or behavioral changes post-unlearning (e.g., in safety evaluations), but nothing explicitly identifies or circuits for "paranoia" or tampering detection. This seems novel, though it builds on general circuit discovery in mech interp.

**Suggested Papers (1-3 to Get Started)**:
- "A Mathematical Framework for Transformer Circuits" by Elhage et al. (2021) – A foundational paper on identifying circuits in transformers; useful for methodology in your Exp1/Exp2. [Link: https://transformer-circuits.pub/2021/framework/index.html]
- "Towards Understanding Sycophancy in Language Models" by Sharma et al. (2023) – Explores behavioral shifts in models under perceived observation, which could inform prompts for "scaring" the model. [arXiv: https://arxiv.org/abs/2310.13548]
- "Unlearning in Large Language Models: A Survey" by Zhang et al. (2024) – Covers effects of unlearning/alignment on model internals; good for comparing pre- and post-alteration activations. [arXiv: https://arxiv.org/abs/2402.01946]

This project aligns well with Neel Nanda's interest in "understanding weird behaviour" and could be scoped to 20 hours by focusing on a small model like Gemma 2, using tools like TransformerLens for circuit identification.

### 2. What is a Good Explanation of Cognition in Neural Networks?

**Concrete Hypothesis**: A "good" explanation of cognition in neural networks (or brains, if fully observable) must identify causally relevant circuits and representations that map to high-level behaviors, such as decision-making or reasoning, rather than just describing low-level activations; this can be tested by evaluating whether mechanistic explanations (e.g., via circuit ablation) better predict model outputs than statistical correlations alone.

**Has This Been Tested Before?**: This is more of a conceptual/philosophical question than an empirical one, and searches for "what is a good explanation of cognition in neural networks mechanistic interpretability" yield mostly introductory resources on mech interp as a field, not direct tests. Some work discusses "mechanistic theories" of neural activity (e.g., in neuroscience-AI analogies), but no specific experiments test criteria for "good" explanations. It remains underexplored empirically, though debated in interpretability overviews.

**Suggested Papers (1-3 to Get Started)**:
- "Mechanistic Interpretability: A Challenge Common to Both Artificial and Biological Neural Networks" by Kempner Institute (2024) – Discusses what constitutes a "mechanistic theory" of cognition, bridging brains and ANNs. [Link: http://kempnerinstitute.harvard.edu/research/deeper-learning/mechanistic-interpretability-a-challenge/]
- "What is Mechanistic Interpretability and Where Did It Come From?" by Mindful Modeler (2024) – Explains mech interp as reverse-engineering for human-understandable mechanisms; good for framing "good explanations." [Link: https://mindfulmodeler.substack.com/p/what-is-mechanistic-interpretability]
- "A Comprehensive Mechanistic Interpretability Explainer & Glossary" by Neel Nanda (2024) – Neel's own glossary; directly relevant for defining terms like features/circuits in explanations. [Link: https://www.neelnanda.io/mechanistic-interpretability/glossary]

This might be tricky for a 20-hour empirical project (it's philosophical), but you could pivot to testing explanation quality via a small case study, like ablating circuits in a toy task and assessing predictive power. It fits Neel's "basic science" category but may need more scoping.

### 3. Steganography in LLM Chain of Thought

**Concrete Hypothesis**: LLMs can be fine-tuned to encode task-relevant hidden information (e.g., intermediate computations for a math problem) in their chain-of-thought (CoT) outputs in a way that remains plausible to human readers but influences the final answer, and this encoding can be detected and deciphered using sparse autoencoders (SAEs) or activation patching, outperforming random baselines.

**Has This Been Tested Before?**: Yes, this has been tested in several studies. Searches for "steganography in LLM chain of thought" return multiple papers and posts showing LLMs can learn or use steganographic encoding in CoT, including evasion of monitoring and hidden reasoning. For example, work from Redwood Research and arXiv papers demonstrate LLMs hiding information in generations, with evaluations of defenses. It's not fully saturated, so extensions (e.g., deciphering with interp tools) could be novel.

**Suggested Papers (1-3 to Get Started)**:
- "Steganography in Chain of Thought Reasoning" by Larks (2022) – Early exploration of hidden info in multi-stage CoT; directly on-point. [Link: https://www.lesswrong.com/posts/yDcMDJeSck7SuBs24/steganography-in-chain-of-thought-reasoning]
- "Large Language Models Can Learn and Generalize Steganographic Communication" by Wang et al. (2024) – Shows LLMs encoding hidden messages in CoT; includes training methods. [arXiv: https://arxiv.org/abs/2506.01926]
- "Early Signs of Steganographic Capabilities in Frontier LLMs" by Binder et al. (2025) – Analyzes evasion in generations; useful for safety implications and interp. [arXiv: https://arxiv.org/abs/2507.02737]

This is a strong fit for Neel's suggestion—focus on a reasoning model like Qwen 3, train a simple steganographic CoT, and use interp tools to decipher. It's feasible in 20 hours with nnsight or TransformerLens, and emphasizes baselines as Neel recommends.

### 4. User Models in LLMs (Extensions of Chen et al.)

**Concrete Hypothesis**: Beyond static traits like demographics, LLMs dynamically represent user attributes such as emotional state (e.g., sadness) across conversation turns, inferred from prompt cues, and steering these representations (via probes or vectors) can causally alter model responses to intentionally manipulate user emotions, such as cheering up a "sad" user.

**Has This Been Tested Before?**: Partially yes—Chen et al. (likely "LLMs Form User Models" or similar, based on description) established static user modeling, and searches for "LLM user models dynamic attributes emotion Chen et al extensions" show extensions to dynamic states like emotions or mental shifts. Papers on emotion cognition and temporal evolution in LLMs exist, but intentional manipulation (e.g., detecting sadness to make happy) seems underexplored, offering room for novelty.

**Suggested Papers (1-3 to Get Started)**:
- "Recent Advancement of Emotion Cognition in Large Language Models" by Li et al. (2024) – Surveys LLM emotion understanding; good for dynamic inference methods. [arXiv: https://arxiv.org/abs/2409.13354]
- "Evaluating LLM Adaptation to Temporal Evolution of Human States" by Liu et al. (2025) – Directly on dynamic mental states in conversations; extends to user support scenarios. [arXiv: https://arxiv.org/abs/2505.17663]
- "Language-Specific Representation of Emotion-Concept Knowledge Causally Supports Emotion Inference" by Skerry-Ryan et al. (2024) – Explores emotion representations in LLMs; useful for probing dynamic attributes. [Link: https://www.sciencedirect.com/science/article/pii/S2589004224026269]

This matches Neel's "user models" prompt exactly—build on Chen et al. by probing for emotions in a model like Llama 3, using linear probes or steering. It's exciting for model biology, and you could test manipulation as a stretch in 20 hours.

**Recommendation for Your Project**: Go with Steganography or User Models—they're directly from Neel's list, align with his "model biology" interests, and have clear empirical hooks (e.g., training/probing). Avoid the philosophical one if you want something hands-on. For any, start with Neel's recommended resources like TransformerLens tutorials, and use LLMs (e.g., Gemini) for coding help as he suggests. Aim for clear write-up with graphs and baselines!
