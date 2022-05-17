#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uvicorn
from path import Path

from backend.common.log import log
from backend.ninja_xia import settings
from backend.ninja_xia.asgi import application

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
