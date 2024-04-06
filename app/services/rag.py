from typing import AsyncIterable, List, Optional

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from app.services.search import Search
from app.services.classes import Document
from app.services.constants import (_COMPARE_PROMPT, _GEMINI_GENERATION_CONFIG,
                           _GEMINI_SAFETY_SETTINGS_NONE)


class RagSummary:
    def __init__(
            self, 
            os_search: Search,
            llm_service:str, 
            model_name:str, 
            api_key:str, 
            target_uid:str, 
            n_results:int = 6
    ):
        assert llm_service in ["google", "claude", "openai"], f"Currently only support google, claude, openai, but got {llm_service}"

        self.search = os_search
        self.llm_service = llm_service
        self.model_name = model_name
        self.target_uid = target_uid
        self.n_results = n_results
        self.api_key = api_key

        self.main_article, self.related_articles = self._get_articles()
        self.model = self._init_llm()

    def _init_llm(self) -> Optional[ChatGoogleGenerativeAI]:
        if self.llm_service == "google": 
            model = ChatGoogleGenerativeAI(
                google_api_key=self.api_key,
                model=self.model_name,
                safety_settings=_GEMINI_SAFETY_SETTINGS_NONE,
                generation_config=_GEMINI_GENERATION_CONFIG
            )
        elif self.llm_service == "claude":
            model = ChatAnthropic(
                anthropic_api_key = self.api_key,
                model_name=self.model_name
            )
        elif self.llm_service == "openai":
            model = ChatOpenAI(
                openai_api_key=self.api_key,
                model_name=self.model_name
            )
        else: 
            raise ValueError(f"Currently only support google, claude, openai, but got {self.llm_service}")
        return model

    def _get_articles(self):
        _, _, documents = self.search.get_document_similarity_network(
            uid=self.target_uid, layer=0, n_results=self.n_results
        )
        
        main_article: Document = documents[self.target_uid]

        related_articles: List[Document] = [x for x in documents.values() if x.uid != self.target_uid]

        return main_article, related_articles
    
    async def run(self) -> AsyncIterable[str]:
        prompt = ChatPromptTemplate.from_template(_COMPARE_PROMPT)
        parser = StrOutputParser()
        chain:RunnableSerializable = ( prompt | self.model | parser )

        chunks = []
        main_article = f"# {self.main_article.title}\n\n摘要：\n{self.main_article.abstract}"
        related_articles = "\n".join(
            [
                f"# {x.title}\n\n摘要：\n{x.abstract}" 
                for x in self.related_articles
            ]
        )
        answer = chain.stream({"main_article": main_article, "related_articles": related_articles})
        for chunk in answer:
            chunks.append(chunk)
            yield chunk
