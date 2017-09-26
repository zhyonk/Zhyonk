# _author_='zhyonk'
# -*- coding:utf-8 -*-
from werobot import WeRoBot

robot = WeRoBot(enable_session=False,
                token='l492LBlIFo2040n04mNwFBOZ0289v90l',
                APP_ID='wx3fcb154832732b75',
                APP_SECRET='6961c68cc55aad7fc460a03fb08b281c')
client = robot.client


@robot.handler
def hello(message):
    return 'Hello world'
