# -*- coding: utf-8 -*-
from . import BaseRESTAPI
from .. import TOKEN_TYPE_NONE


class HookBot(BaseRESTAPI):

    def send_msg(self, hook_id, text, title=''):
        """发送消息

        机器人 | 如何在群聊中使用机器人？
        """
        return self._post(
            'bot/hook/{}'.format(hook_id),
            data={
                'title': title,
                'text': text
            },
            token_type=TOKEN_TYPE_NONE
        )
