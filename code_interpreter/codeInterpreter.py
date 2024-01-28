from fastapi import FastAPI, HTTPException
from llama_hub.tools.code_interpreter import CodeInterpreterToolSpec
from pydantic import BaseModel, Field

app = FastAPI()


class CodeRequest(BaseModel):
    code: str = Field(..., description='Code string')


@app.post('/execute',
          summary='Execute Python code.',
          description='Executes arbitrary Python code and returns the stdout and stderr.',
          response_description='The standard output and standard error of the executed code.')
def execute_code(code_request: CodeRequest):
    try:
        tool_spec = CodeInterpreterToolSpec()
        return tool_spec.code_interpreter(code_request.code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
