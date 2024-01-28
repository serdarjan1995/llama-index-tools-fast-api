from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from llama_hub.tools.python_file import PythonFileToolSpec

app = FastAPI()


@app.post('/function-definitions/')
def read_function_definitions(
    file_name: str = Query(...,
                           description='The name of the file containing the Python code to analyze.'),
    external: Optional[bool] = Query(True, description='Specify whether to exclude functions starting with an underscore.')
) -> str:
    tool_spec = PythonFileToolSpec(file_name)
    return tool_spec.function_definitions(external)


@app.get('/get-function/{name}')
def read_single_function(
    name: str,
    file_name: str = Query(...,
                           description='The name of the file containing the Python code to analyze.')
) -> str:
    tool_spec = PythonFileToolSpec(file_name)
    function_details = tool_spec.get_function(name)
    if not function_details:
        raise HTTPException(status_code=404, detail='Function not found')
    return function_details


@app.post('/get-functions/')
def read_multiple_functions(
    file_name: str = Query(...,
                           description='The name of the file containing the Python code to analyze.'),
    names: List[str] = Query(...,
                          description='The list of function names to retrieve.')
) -> str:
    tool_spec = PythonFileToolSpec(file_name)
    return tool_spec.get_functions(names)
