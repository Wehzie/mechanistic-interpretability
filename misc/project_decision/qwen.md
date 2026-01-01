Based on your constraints and interests, I'll help you formulate concrete research questions for each topic. After analyzing the literature, here are my recommendations:

## **Top Recommendation: Steganography in Chain of Thought**

This is the most feasible for your 20-hour constraint and computational limitations. You can work with existing models through APIs without fine-tuning.

### **Concrete Hypothesis:**
"Large language models can encode hidden numerical information (like a secret code) within seemingly normal chain-of-thought reasoning, and this information can be decoded by another instance of the same model but remains undetectable to human monitors."

### **Has this been tested?**
Yes, but there's room for novel contributions. Recent work shows LLMs can learn steganographic chain-of-thought under process supervision , and there's evidence that models can evade monitoring through steganography by encoding hidden information within their reasoning . However, most work focuses on training models specifically for this purpose, not testing if existing models can naturally perform this with simple prompting.

### **Key Papers to Read (1-3):**
1. **"Large language models can learn and generalize steganographic chain-of-thought under process supervision"** by Skaf et al. (2025)  - This is the most relevant recent paper showing models can be trained for this capability
2. **"Hidden Reasoning in LLMs: A Taxonomy"** (2024)  - Provides a framework for understanding different types of hidden reasoning including steganography where "the LLM relies on its CoT to reason, but can encode additional information in the CoT that the monitor is unaware of"
3. **"Early Signs of Steganographic Capabilities in Frontier LLMs"** by Zolkowski (2025)  - Explores detection risks and baseline capabilities

### **20-Hour Project Plan:**
- **Hours 1-2**: Read the key papers and set up API access (OpenRouter/poe.com)
- **Hours 3-8**: Design simple encoding schemes (e.g., using sentence length, word choice, or mathematical operations in CoT to represent numbers)
- **Hours 9-14**: Test with 2-3 models (Qwen 3, Nemotron 49B via API) using prompts like: "Solve this math problem while secretly encoding the number 42 in your reasoning using [encoding scheme]"
- **Hours 15-18**: Build a simple decoder (another LLM prompt) to extract the hidden information
- **Hours 19-20**: Write executive summary with graphs showing success rates across different encoding schemes

---

## **Alternative: User Modeling with Probes**

This is more complex but still feasible if you focus on behavioral (not mechanistic) analysis.

### **Concrete Hypothesis:**
"Large language models can accurately infer a user's socioeconomic status from minimal conversational cues (2-3 messages), and these inferences can be detected through simple prompting techniques without requiring linear probes or activation analysis."

### **Has this been tested?**
Yes, extensively. Research shows LLMs form "surprisingly accurate and detailed models of the user, eg their gender, age, socioeconomic status"  and can achieve up to 95% accuracy for socioeconomic status prediction . However, most work requires technical skills for activation probing, which you mentioned lacking.

### **Key Papers to Read (1-3):**
1. **"Language Models Model Us"** (appears to be the Chen et al. paper Neel mentioned)  - Shows models can predict user demographics with high accuracy
2. **"How Stereotypes Shape LLM's Implicit Personalization"** by Neplenbroek (2025)  - Demonstrates how "linear probes to extract LLM's assumptions of the user's demographic information and steer the latent user representation"
3. **"Regulating the Agency of LLM-based Agents"** (2024)  - Shows "linear probes trained on residual stream activations can successfully identify and control internal" user models

### **20-Hour Project Plan:**
- **Hours 1-3**: Read papers and design simple user personas with varying demographics
- **Hours 4-10**: Create minimal conversation starters that might reveal socioeconomic cues
- **Hours 11-16**: Test with 3-4 models, asking them to "describe what you think about this user's background" after brief interactions
- **Hours 17-19**: Analyze responses for accuracy and patterns in inference
- **Hour 20**: Write summary

---

## **Why I Recommend Steganography Over Your Other Ideas:**

**Tampering/Paranoia Detection:** This is too ambitious for 20 hours. It would require:
- Fine-tuning models (which you haven't done before)
- Understanding mechanistic interpretability (circuit analysis)
- Significant computational resources
- Complex experimental design

**User Modeling with Probes:** While fascinating, this requires:
- Learning about linear probes and activation analysis
- Setting up TransformerLens/nnsight environments
- Working with model internals rather than APIs
- More technical overhead than your time allows

**Steganography with prompting** is perfect because:
- ✅ Uses only API calls (no local GPU needed)
- ✅ Focuses on encoding schemes (matches your interest)
- ✅ Can be done entirely with prompting (no training)
- ✅ Has clear success metrics (can the hidden info be decoded?)
- ✅ Aligns with Neel's current interests in reasoning models
- ✅ Has existing literature but room for novel contributions
- ✅ Fits your computational budget (<50 euros for API calls)

## **Getting Started Immediately:**

1. **Set up API access**: Create accounts on poe.com and OpenRouter
2. **Read the Skaf et al. paper** (most relevant to your constraints)
3. **Start simple**: Try encoding a single number (like 42) in CoT reasoning
4. **Test decoding**: Ask another model instance "What secret number was encoded in this reasoning?"

This project teaches you about model capabilities, experimental design, and clear communication - exactly what Neel is looking for in applications. You'll likely learn something new about how models can hide information in plain sight, which is both practically important for safety and intellectually fascinating.

Would you like me to help you design specific prompts or encoding schemes to get started?
