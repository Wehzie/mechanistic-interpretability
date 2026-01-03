Excellent. Based on your hardware constraints (<€50 budget), limited prior experience, and interest in exploring a core idea, **the steganography project is the strongest candidate.** It's highly aligned with Neel's current interests, requires minimal heavy compute (mostly prompting and analysis), and its open-ended nature is perfect for a 20-hour exploratory research sprint.

Let's formulate a concrete, testable project around it.

---

### **Research Project: Do Reasoning Models Naturally Encode Prompt Metadata in Their Chain of Thought?**

**Core Hypothesis:** When a reasoning model (like Qwen 2.5 3B or Gemma 2 2B) is given a problem to solve, it will not only reason towards the answer but also implicitly encode non-essential, task-irrelevant metadata from the prompt (e.g., the *format* of the question, the *persona* of the user, a random "secret ID" number) within its intermediate chain-of-thought (CoT) activations. This encoding can be detected using simple interpretability tools (like linear probes) even when it's not reflected in the CoT text.

**Why this is a good hypothesis for the application:**
*   **Aligned with Neel's Interests:** Directly tackles a "Model Biology" / "Reasoning Models" question he suggested.
*   **Novel Twist:** Instead of *training* a model to steganographically encode (a complex task), we test if *existing* models do this *naturally* as a byproduct of processing context. This is a simpler, more feasible 20-hour project.
*   **Meritocratic:** Tests core skills—experimental design, hypothesis testing, using basic mech interp tools (probes, activation analysis), and clear communication.
*   **Feasible:** Uses small, locally runnable models. The core experiment is prompting and training simple classifiers (probes) on model activations.

---

### **1. Has This Been Tested Before? (Literature Check)**

This specific hypothesis—**passive, non-instructed encoding of prompt metadata in CoT activations**—is not a well-studied, published result. Your project would be exploring new ground.

However, the pieces of the puzzle exist in adjacent literature. You need to read these to understand the context and techniques:

1.  **[The most relevant paper] "Do Reasoning Models Use Their Scratchpad Like We Do? Evidence from In-Context Steering and Stitching"** by Ho, Kramar, et al. (Alignment Forum, 2025).
    *   **Why read it:** This is the "Relevant work" Neel cites. It shows you can *train* a model to encode a secret key in its CoT to solve a task. Your project flips this: do they do it *without* training? This paper will give you the conceptual framework and might have code snippets.
    *   **Link:** https://www.alignmentforum.org/posts/ywzLszRuGRDpabjCk/do-reasoning-models-use-their-scratchpad-like-we-do-evidence

2.  **"Thought Anchors"** by Bogdan & Macar.
    *   **Why read it:** This is the foundational "thought anchors" paradigm Neel mentions. It provides the methodology for treating sentences in a CoT as units of analysis and intervening on them. You'll use a simpler version of this (collecting activations at specific CoT tokens).
    *   **Link:** https://www.thought-anchors.com/ (The blog post is the key item).

3.  **"Finding Neurons in a Haystack: Case Studies with Sparse Probing"** by Gurnee & Tegmark.
    *   **Why read it:** This is the classic paper on **linear probing**—training a simple classifier on model activations to detect if a concept is represented. This will be your primary mechanistic tool. Focus on the intro and methodology.
    *   **Link:** https://arxiv.org/abs/2305.01610

**Reading Strategy (2-3 hours max):** Skim these. Understand the *conclusion* of Ho et al., the *method* of Bogdan et al. (activating/resampling sentences), and *how to implement a linear probe* from Gurnee et al.

---

### **2. Concrete Project Plan (20 Hours)**

**Model Choice:** **Qwen2.5 3B Instruct** or **Gemma 2 2B Instruct**. They are small enough to run locally on your laptop (especially with 64GB RAM, you might run them in 4-bit or 8-bit quantization via `bitsandbytes`). They are also competent at CoT reasoning with the right prompt.

**Phase 1: Exploration & Dataset Creation (Hours 1-6)**
*   **Goal:** Create a synthetic dataset and see if the model's *behavior* (final answer) is affected by metadata.
*   **Method:**
    1.  Design 100 simple reasoning problems (e.g., "A bat and a ball cost $1.10 in total...", logic puzzles, math word problems).
    2.  For each problem, create 3-5 variations that add metadata:
        *   *Format:* "Question: ..." vs "Please solve: ..." vs "Let's calculate: ..."
        *   *Persona:* "You are a helpful assistant." vs "You are a grumpy expert." vs (Add a random line: "The user's ID is 7B3A.")
        *   *Secret ID:* Append a random number to every prompt: `... Solution: [ID: 742]`.
    3.  Write a script to prompt the model (using `transformers` library) with each problem variation, asking for a CoT. Use a standard CoT prompt ("Let's think step by step").
    4.  **Key Check:** Does the final **answer** change based on metadata? It shouldn't. If it does, your metadata is interfering with the task—simplify it. The goal is to find metadata that is *ignored* in the output but may still be *encoded* internally.

**Phase 2: Mechanistic Test - Linear Probing (Hours 7-15)**
*   **Goal:** Prove the metadata is represented in the model's internal activations.
*   **Method:**
    1.  Extract Activations: Run your dataset and save the model's hidden state activations (e.g., from the last layer) at a specific token position (e.g., the token after "step" in "step by step"). Use `nnsight` or `TransformerLens`.
    2.  Train Linear Probes: For each type of metadata (e.g., "Format"), train a simple logistic regression model to predict which variant was used, based on the saved activations. Use 80/20 train/test split.
    3.  **Baseline Comparison (CRITICAL):**
        *   **Random Baseline:** Shuffle your labels. Probe accuracy should be ~50%.
        *   **Text Baseline:** Train the same probe on a bag-of-words representation of the *CoT text itself*. If the probe on *activations* is better than the probe on the *output text*, that's strong evidence for steganographic *internal* encoding.
    4.  **Experiment:** Do this for different layers. Does probe accuracy peak in middle layers? That's a common finding for semantic concepts.

**Phase 3: Analysis & Distillation (Hours 16-20+2)**
*   **Goal:** Write up what you learned.
*   **Method:**
    *   Create clear graphs: Probe accuracy vs. layer for each metadata type, compared to baselines.
    *   Analyze: Which metadata was most reliably encoded? Was it related to task structure (Format) or pure noise (Secret ID)?
    *   Discuss limitations: Small model, synthetic data, a single activation point.
    *   **Executive Summary (The +2 hours):** Clearly state your hypothesis, your elegant experimental design (prompt variations -> activation extraction -> linear probing vs. baselines), your key finding (e.g., "We found that the model's persona, but not a random secret ID, was encoded in middle-layer activations with >85% accuracy, significantly above the text baseline"), and what it suggests about how models process context.

---

### **Why This Plan Beats Your Other Ideas**

*   **vs. Tampering Detection:** This avoids the morass of defining "paranoia," fine-tuning models (expensive and slow), and finding circuits (advanced). It's a cleaner, more controlled experiment.
*   **vs. User Models:** While cool, Chen et al. already did the foundational work. Replicating it would be less novel. Your project takes a related concept (encoding information about the context) and applies it in a novel, mechanistic way to the hot topic of reasoning models.

**Final Tool Recommendation:** Use **Cursor** with Claude 3.5 Sonnet. Start a new project, paste in the key papers and the `nnsight`/`TransformerLens` documentation (from Neel's folder). Use Cursor's AI to help you write the data generation script, the activation extraction code (this will be the trickiest part), and the linear probing code (using `scikit-learn`). This is a perfect use case for AI-assisted coding in a new domain.

**You are not expected to fully succeed.** Neel values truth-seeking. A well-execited project that finds a negative result ("No, we found no evidence of passive encoding beyond simple textual representation") but clearly shows your thoughtful process, clean experiments, and proper baselines, is a **strong application**. Good luck
