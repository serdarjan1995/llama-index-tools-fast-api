from fastapi import FastAPI, Query
from llama_hub.tools.wikipedia import WikipediaToolSpec

app = FastAPI(
    title="Wikipedia API",
    description="API for retrieving and searching content from Wikipedia.",
)


@app.get('/wikipedia/load_page', summary='Load Content from Wikipedia Page', tags=['Wikipedia'])
async def read_page(page: str = Query(..., description='Title of the Wikipedia page to load.'),
                    lang: str = Query('en', description='Language of the Wikipedia page.')) -> str:
    tool_spec = WikipediaToolSpec()
    content = tool_spec.load_data(page=page, lang=lang)
    return content


@app.get('/wikipedia/search', summary='Search Wikipedia and Load First Result', tags=['Wikipedia'])
async def search_wiki(query: str = Query(..., description='Search query for Wikipedia.'),
                      lang: str = Query('en', description='Language to perform the Wikipedia search in.')) -> str:
    tool_spec = WikipediaToolSpec()
    content = tool_spec.search_data(query=query, lang=lang)
    return content
