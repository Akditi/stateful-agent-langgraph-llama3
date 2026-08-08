import os
import configparser


class Config:
    """
    Reads UI configuration (page title, available LLM providers, available
    use cases) from uiconfigfile.ini so the Streamlit UI doesn't have to
    hardcode these values inline.
    """

    def __init__(self, config_path: str = None):
        self.config = configparser.ConfigParser()
        config_path = config_path or os.path.join(
            os.path.dirname(__file__), "uiconfigfile.ini"
        )
        self.config.read(config_path)

    def get_page_title(self) -> str:
        return self.config["DEFAULT"].get("PAGE_TITLE", "LangGraph AgenticAI")

    def get_llm_options(self) -> list:
        raw = self.config["DEFAULT"].get("LLM_OPTIONS", "Groq")
        return [item.strip() for item in raw.split(",") if item.strip()]

    def get_usecase_options(self) -> list:
        raw = self.config["DEFAULT"].get(
            "USECASE_OPTIONS", "Basic Chatbot, Chatbot With Web, AI News"
        )
        return [item.strip() for item in raw.split(",") if item.strip()]