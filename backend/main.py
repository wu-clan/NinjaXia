#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path

import uvicorn

from backend.ninja_xia import settings
from backend.ninja_xia.asgi import application
from backend.xia.common.log import log

app = application

if __name__ == '__main__':
    try:
        log.info(
            """\n
 ████     ██ ██             ██           ██     ██ ██          
░██░██   ░██░░             ░░           ░░██   ██ ░░           
░██░░██  ░██ ██ ███████     ██  ██████   ░░██ ██   ██  ██████  
░██ ░░██ ░██░██░░██░░░██   ░██ ░░░░░░██   ░░███   ░██ ░░░░░░██ 
░██  ░░██░██░██ ░██  ░██   ░██  ███████    ██░██  ░██  ███████ 
░██   ░░████░██ ░██  ░██ ██░██ ██░░░░██   ██ ░░██ ░██ ██░░░░██ 
░██    ░░███░██ ███  ░██░░███ ░░████████ ██   ░░██░██░░████████
░░      ░░░ ░░ ░░░   ░░  ░░░   ░░░░░░░░ ░░     ░░ ░░  ░░░░░░░░                                                                                                 
            """
        )
        uvicorn.run(app=f'{Path(__file__).stem}:app', host=settings.UVICORN_HOST, port=settings.UVICORN_PORT,
                    reload=settings.UVICORN_RELOAD)
    except Exception as e:
        log.error(f'NinjaXia start filed ❗❗❗: {e}')
    finally:
        raise SystemError('❗ 请使用 wsgi 模式启动， asgi 模式未适配')  # noqa
