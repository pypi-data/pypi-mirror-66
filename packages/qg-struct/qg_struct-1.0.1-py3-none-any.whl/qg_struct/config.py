import json
from qg_aio_eureka.client import EurekaClient
import random
import aiohttp
import asyncio
from importlib import import_module
import traceback
import sys
import os
import logging
import signal

config = {}

try:
    profile = 'dev' if 'dev' in sys.argv else 'prod'
    bootstrap = import_module('bootstrap')
    app_name = bootstrap.app_name
    ip = bootstrap.ip
    port = bootstrap.port
    config_server_name = bootstrap.config_server_name
    eureka_url = bootstrap.eureka_url
    register = bootstrap.register
    version = bootstrap.version if 'version' in dir(bootstrap) else '0.0.1'
except:
    print('引导文件导入错误')
    traceback.print_exc()
eureka = EurekaClient(app_name=app_name, port=port, ip_addr=ip,
                      eureka_url=eureka_url)


async def get_config(config_server_name=config_server_name, profile=profile, register=register):

    if register:
        await eureka.register()

        def close(*arg):
            asyncio.get_event_loop().run_until_complete(eureka.deregister())
            os._exit(1)
        signal.signal(signal.SIGINT, close)
        signal.signal(signal.SIGTERM, close)
        try:
            signal.signal(signal.SIGKILL, close)
        except:
            pass
        signal.signal(signal.SIGILL, close)

        async def heart():
            while True:
                await asyncio.sleep(20)
                try:
                    await eureka.renew()
                except:
                    print('连不上eureka')
                    traceback.print_exc()
                    try:
                        await eureka.register()
                    except:
                        print('注冊eureka失败')
                        traceback.print_exc()
        asyncio.ensure_future(heart())
    config_app = await eureka.get_app(config_server_name)
    config_instances = config_app['application']['instance']
    config_instance = random.choice(config_instances)
    url = '{homepage}{app_name}-{profile}.json'.format(
        homepage=config_instance['homePageUrl'], app_name=app_name, profile=profile)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            settings = await resp.json()

    return dict(**settings, version=version, profile=profile, app_name=app_name, ip=ip, port=port, config_server_name=config_server_name, eureka_url=eureka_url, register=register)


async def get_app_homepage(name, is_thread=False):
    if is_thread:
        eureka2 = EurekaClient(app_name=app_name, port=port, ip_addr=ip,
                              eureka_url=eureka_url)
        app = eureka2.get_app_sync(name)
    else:
        app = await eureka.get_app(name)
    if not app:
        return None
    config_instances = app['application']['instance']
    config_instance = random.choice(config_instances)
    logging.debug('调度服务 {} 地址 {}'.format(name, config_instance['homePageUrl']))
    return config_instance['homePageUrl']



async def load_config():
    settings = await get_config()
    with open('config.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(settings, ensure_ascii=False,
                           indent=4, separators=(',', ':')))
    print('加载配置成功')
    for i in settings:
        config[i] = settings[i]

loop = asyncio.get_event_loop()
loop.run_until_complete(load_config())
