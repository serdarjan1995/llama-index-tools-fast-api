"""agent search tool spec."""

from typing import Optional

from llama_index.readers.schema.base import Document
from llama_index.tools.tool_spec.base import BaseToolSpec


class AgentSearchToolSpec(BaseToolSpec):
    """agent search tool spec."""

    spec_functions = ["load_data"]

    def __init__(self, api_base: Optional[str] = None, api_key: Optional[str] = None, ):
        """Initialize with parameters."""
        import_err_msg = (
            "`agent-search` package not found, please run `pip install agent-search`"
        )
        try:
            import agent_search  # noqa: F401
        except ImportError:
            raise ImportError(import_err_msg)

        from agent_search import SciPhi

        self._client = SciPhi(api_base=api_base, api_key=api_key)

    def load_data(
            self,
            query: str,
            search_provider: str = "bing",
            llm_model: str = "SciPhi/Sensei-7B-V1",
    ):
        """
        Load data from AgentSearch, hosted by SciPhi.

        Args:
            query (str): Query string.
            search_provider (str): Search provider. Defaults to "bing"
            llm_model (str): LLM model to be used. Defaults to "SciPhi/Sensei"

        Returns:
            List[Document]: A list of documents.

        """
        rag_response = self._client.get_search_rag_response(
            query=query, search_provider=search_provider, llm_model=llm_model
        )
        return [Document(text=rag_response.pop("response"), metadata=rag_response)]
