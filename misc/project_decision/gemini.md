This is a high-stakes application. Neel Nanda’s document is incredibly specific about his "taste": he values **pragmatism, simplicity, and "Model Biology"** (treating the model as an organism to be studied). He explicitly warns against "ambitious" or "anthropomorphic" framings (like "paranoia") without concrete evidence.

Here are three concrete research proposals based on your interests and Neel’s document. I have heavily reframed Rafael’s idea to fit Neel’s "mechanistic" criteria.

### **Option 1: The Geometry of "I Won't" vs. "I Can't" (Refined "Tampering" Idea)**

*Best for: Rafael’s original interest, reframed to be less anthropomorphic and more mechanistic.*

Neel’s document explicitly mentions "Understanding weird behaviour" and "Refusal is mediated by a single direction" as key interests. Your original idea of "detecting tampering" is risky because it assumes the model has a "self" to be tampered with. A more rigorous, mechanistic framing is to ask: **Does the model represent "censored knowledge" differently from "unknown knowledge"?**

* **Hypothesis:** The internal activation space distinguishes between *known-but-refused* facts (e.g., dangerous instructions, "unlearned" data) and *unknown* facts (e.g., made-up gibberish). Specifically, we hypothesize there is a "Refusal Direction" orthogonal to an "Uncertainty Direction."
* **The "Twist":** Most people look for refusal. You are looking for the *difference* between refusal and ignorance. If you ablate the "refusal" direction, does the model recover the knowledge, or does it become "ignorant"?
* **Feasibility:** High. You can do this with open-weights models (Llama 3, Gemma 2) and existing datasets (e.g., harmful prompts vs. obscure trivia).
* **Papers to read:**
1. **"Refusal in Language Models Is Mediated by a Single Direction"** (Arditi et al., 2024) – *Cited in Neel’s doc; this is your baseline.*
2. **"Representation Engineering: A Top-Down Approach to AI Transparency"** (Zou et al., 2023) – *For methods on finding these directions.*
3. **"Do LLMs Really Forget? Evaluating Unlearning with Knowledge Correlation..."** (2025) – *For understanding the difference between unlearning and forgetting.*



### **Option 2: Dynamic User Modeling (The "User Models" Interest)**

*Best for: High feasibility, clear "Model Biology" angle, and Neel explicitly asked for this.*

Neel’s document asks: "Do LLMs form dynamic models of users for attributes that vary across turns, eg emotion?" This is a "Model Biology" project—you are studying the organism's reaction to stimuli.

* **Hypothesis:** LLMs maintain a persistent "User State" vector across a conversation history that linearly encodes dynamic attributes (like user frustration or confusion). Injecting a steering vector into this subspace will causally alter the *tone* of the model's response without changing the *factual content*.
* **The "Twist":** Instead of just classifying the user (static), look at the **dynamics**. How quickly does the model update its "user model" when the user changes tone? Is there a specific layer where "User Frustration" is computed?
* **Feasibility:** Very High. You don't need to train a model. You just need to cache activations during a multi-turn chat and train linear probes.
* **Papers to read:**
1. **"Mechanistic Interpretability of Emotion Inference in Large Language Models"** (2025) – *Recent work establishing emotion is localized.*
2. **"Linear Representations of Sentiment in Large Language Models"** (Tigges et al.) – *Cited in Neel’s doc; shows sentiment is linear.*
3. **"The Geometry of Truth: Occam's Razor for Science"** (Marks et al.) – *Standard for probing techniques.*



### **Option 3: Steganography & The "Wait" Phenomenon**

*Best for: Reasoning models (O1/R1/QwQ) and "Applied Interpretability".*

Neel mentions: "Can models encode information in their chain of thought?" and refers to the "Wait" project (Troitskii et al.) where models "decided" the answer early but outputted filler text.

* **Hypothesis:** In reasoning models (like DeepSeek-R1-Distill or QwQ), the final answer is linearly encoded in the residual stream *long before* the model explicitly states it in the Chain of Thought (CoT). The "reasoning" tokens between the encoding point and the answer act as a buffer (steganography) rather than functional computation.
* **The "Twist":** Test if you can **patch** the answer from a "correct" run into an "incorrect" run early in the CoT. If the CoT is just steganography/rationalization, the patch should flip the answer immediately, even if the CoT logic hasn't played out yet.
* **Feasibility:** Medium. Requires handling reasoning traces and potentially "patching" experiments which can be finicky, but very high reward if it works.
* **Papers to read:**
1. **"Large Language Models Can Learn and Generalize Steganographic Chain-of-Thought..."** (2025) – *Evidence this is real.*
2. **"Internal states before 'wait' modulate reasoning patterns"** (Troitskii et al.) – *Neel’s scholar’s paper on this exact topic.*
3. **"Thought Anchors: Which LLM Reasoning Steps Matter?"** (Bogdan et al.) – *Cited in doc; methods for checking if CoT steps matter.*



### **Recommendation**

If you want the **safest bet** for a 20-hour limit: **Go with Option 2 (User Models).**

* It is purely observational (no complex training).
* It uses standard tools (linear probes, PCA).
* It directly answers a question Neel posed in the "Suggested Research Problems" section.

If you want to be **ambitious** and follow your original "tampering" intuition: **Go with Option 1.**

* Just be very careful to frame it as "distinguishing representation types" (Geometric/Structural) rather than "paranoia" (Anthropomorphic).
