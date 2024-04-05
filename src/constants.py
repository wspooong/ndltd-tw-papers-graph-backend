from langchain_google_genai import HarmBlockThreshold, HarmCategory

_VERSION = "0.0.0"

_SENTENCE_TRANSFORMER_MODEL = "paraphrase-multilingual-mpnet-base-v2"

_INDEX = "ndltd"

_GEMINI_SAFETY_SETTINGS_NONE = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
}

_GEMINI_GENERATION_CONFIG = {
    "candidate_count": 1,
    "max_output_tokens": 2048,
    "temperature": 1.0,
    "top_p": 0.7,
}


_COMPARE_PROMPT = """作為一名專業的學術研究者，請您根據以下指引，對所提供的摘要，進行比較：
1. 你會看到一篇主要文章的摘要，以及幾篇相似文章的摘要。
2. 你需要比較主要文章和相似文章的內容，並提供你的觀點。
3. 你需要指出主要文章和相似文章之間的相似之處和差異之處。
4. 嚴格依賴提供的文本，不包括外部資訊。

主要文章：
{main_article}

相似文章：
{related_articles}
"""
