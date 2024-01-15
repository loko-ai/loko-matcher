import os
import json
import sys

import gradio
import uvicorn
from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from loko_extensions.business.decorator_fastapi import ExtractValueArgsFastAPI

from apps.app import DEMO
from business.matcher_extraction import extract_txt_matches
from extensions.create_component import include_tokens
from utils.matcher_utils import get_matcher_request_fmt

app = FastAPI()
GATEWAY = os.environ.get("GATEWAY", None)

@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    status_code = getattr(exc, "status_code", None) or 500
    e = str(exc)
    error_msg = dict(error=e)
    return JSONResponse(
        status_code=status_code,
        content=error_msg,
    )

@app.post('/extract_matches', response_class=JSONResponse)
@ExtractValueArgsFastAPI()
def loko_extract_matches(value, args):
    logger.debug(f'ARGS: {args}')
    logger.debug(f'JSON: {value}')
    rules = args.get("rules", None)
    include_tokens = args.get("include_tokens", True)
    text4matcher = get_matcher_request_fmt(text=value, rules=rules)
    matches = extract_txt_matches(text=text4matcher, include_tokens=include_tokens)
    return JSONResponse(matches)


#
# @app.post('/upload_file', response_class=JSONResponse)
# @ExtractValueArgsFastAPI(file=True)
# def f2(file, args):
#     logger.debug(f'ARGS: {args}')
#     logger.debug(f'JSON: {file.filename}')
#     file_content = file.file.read()
#     n = int(args.get('n', 10))
#     return JSONResponse(dict(msg=f"{'#'*n} You have uploaded the file: {file.filename}! {'#'*n}"))

if __name__ == "__main__":
    ui_custom_path = "/ui/"
    app = gradio.mount_gradio_app(app, DEMO, path=ui_custom_path)

    # gradio_app = gradio.routes.App.create_app(DEMO, dict(path=ui_custom_path))
    if GATEWAY:
        logger.debug("qui")
        uvicorn.run(app, host="0.0.0.0", port=8080, root_path="/routes/provamatcher")
    else:
        logger.debug("li")
        uvicorn.run(app, host="0.0.0.0", port=8080)
