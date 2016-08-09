#!/usr/bin/env python3
# coding:utf-8

import asyncio
import myorm
from model import Blog, Comment, User

async def test(loop):
    await myorm.create_pool(loop, user='qqj1228', password='qqj1228', db='blogwebapp')
    b = Blog(user_id=6, user_name='test6', user_image='about:blank', title='test6 title', summary='test6 summary', content='test6 content')
    await b.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
