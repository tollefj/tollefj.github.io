These are a few notes from experiences and random readings online as of late.

* **prompt chaining > monolith**: small discrete steps with individual prompts. tends to outperform single-prompt with chain-of-thought instructions

* **structured CoT**: headings and bullet points to keep the structure clear throughout, rather than adding in unstructured formats like `<thinking>...` tokens.

* **xml, really**: seems to work better than JSON in some cases. depends on the task (e.g., coding applications are typically filled with json).

* **semantic parsing**: explicitly instruct llms to act solely as semantic parsers, avoiding the introduction of external knowledge

* **external verification**: use tools like nltk, spacy, and flairnlp to verify llm outputs, instead of giving it as yet another context-window-filling adventure to the LLM.

* **task-specific models**: for narrow tasks, fine-tuned encoder models like modernbert offer performance comparable to llms

* **model sizing**: properly structured tasks often do not require models larger than 32b parameters. see [EuroEval](https://euroeval.com/leaderboards/Multilingual/european/) for an idea of results across multiple languages.

* **llm confidence scoring**: relying on llms to self-assess confidence is unreliable, especially without grounding. letting it rank based on specific instructions (1 means blabla and 2 means that it blablabla") is definitely better than "provide an assessment score between 1-5".

* **self-consistency**: running multiple prompt iterations and aggregating results can improve accuracy but clearly benefits from smaller prompts and/or models

* **exit conditions**: explicit termination criteria for agentic loops, either through structured output, relying on EOS-tokens, or similar.

* **token limitations**: degradation is common beyond 4k tokens in the context window, even though the support is much, much larger. reliable output should never have to deal with crazy document sizes.


### some links

* [llm workflows](<https://www.reddit.com/r/LocalLLaMA/comments/1khjrtj/building_llm_workflows_some_observations/>)
* [modernbert](<https://simmering.dev/blog/modernbert-vs-llm/>)
* [hallucinations](<https://www.nature.com/articles/s41586-024-07421-0> )
* [confidence in llms](<https://www.reddit.com/r/LocalLLaMA/comments/1gh4ht7/are_confidence_scores_from_llms_meaningful/>)
