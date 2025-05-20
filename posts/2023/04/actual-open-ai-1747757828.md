The last week(s) have been extremely turbulent, with one side doing massive development on with Open AI apis, such as AgentGPT <https://github.com/reworkd/AgentGPT> , BabyAGI <https://github.com/yoheinakajima/babyagi> and Chatbot UI <https://github.com/mckaywrigley/chatbot-ui>. On the other side, we have the two largest (and actual open source) projects Dolly by Databricks <https://github.com/databrickslabs/dolly> and (two days ago) Open Assistant <https://github.com/LAION-AI/Open-Assistant>, both with massive releases of open source datasets. 

An interesting paper is [ChatGPT Outperforms Crowd-Workers for Text-Annotation Tasks](https://arxiv.org/pdf/2303.15056.pdf), which gave me ideas for generative annotations for Norwegian. Perhaps even use in Coreference. A pipeline with GPT-4 is not unlikely. But first, training of basic models.

The current status of coreference models:
- spacy coref forked and now supports CorefUDs conll-u format.
- fastcoref forked, along with more ideas from the team behind them, such as LingMess.
