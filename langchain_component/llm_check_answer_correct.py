from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from Config import Config

_llm = ChatOpenAI(api_key=Config.open_ai_api_key.read_text())
_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are language expert. Your task is to determine where there the user provided
     a correct translation of a given phrase. Forgive spelling mistakes or similarly sounding words. Answer in one word either 'Correct' or 'Incorrect'"""),
    ("user", "{input}")
])
_chain = _prompt | _llm


def llm_check_answer_correct(question: str, answer: str, language: str) -> bool:
    return _chain.invoke({"input": f"Text to be translated: '{question}'. Translation to {language}: '{answer}'."}).content.startswith("Correct")


if __name__ == '__main__':
    assert llm_check_answer_correct("hello", "halo", "de")
