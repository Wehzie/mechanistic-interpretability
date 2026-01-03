Rafael’s own ideas:

- Can models detect that they have been tampered with? Maybe this is loosely analogous to a human knowing that they knew something but they forgot what it was exactly \- maybe they remember the key but forgot the value, in a key-value storage sense. The reason for this in the context of alignment \- is that a model could detect that it has been altered in the sense of unlearning or alignment. Methodology identifies a circuit for paranoia, and maybe we find this more activated after unlearning has happened or alignment methods have been used or censoring methods.  
  - Exp1: Take model, make it scared, like “your are being observed”  
  - Exp2: Unlearning/Align/Censor, make it scared again, how does this affect the activity of neurons related to the paranoia circuit or aggression, lying circuit  
- What is a good explanation? We know the state of a neural net at any point in time. We don’t know the state of the brain at any point in time \- let’s say we did \- what do we answer to the question “how does the brain work”? This thought illustrates that this is likely an ill posed question. We must ask what is a good explanation of cognition be it in the brain or neural networks.

Projects given by Neel Nanda that I feel like I understand and like:

* **Steganography**: Can models encode information in their chain of thought? Ideally, in a way where the chain of thought is still plausible to us, but even in ways where we know it's encoded but we don't know what it means. Can you train a model to have reasoning we don't understand and use interpretability tools to decipher it? [Relevant work](https://www.alignmentforum.org/posts/ywzLszRuGRDpabjCk/do-reasoning-models-use-their-scratchpad-like-we-do-evidence)  
  * Note that this needs to allow the model to do tasks it couldn't do without a chain of thought to be interesting.   
* **User models**: [Chen et al](https://arxiv.org/abs/2406.07882) shows that LLMs form surprisingly accurate and detailed models of the user, eg their gender, age, socioeconomic status, and level of education, and do this from very little information. They can find these with probes, and steer with these to change the model’s actions in weird ways.  
  * This is wild\! What else can we learn here? What else do models represent about the user? How are these inferred? How else do they shape behaviour?  
  * Do LLMs form dynamic models of users for attributes that vary across turns, eg emotion, what the user knows, etc.  
    * As a stretch goal, do LLMs ever try to intentionally manipulate these? Eg detect when a user is sad and try to make them happy
