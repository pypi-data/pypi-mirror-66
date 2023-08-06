from typing import List
from unified_message_relay.Core import UMRLogging
from unified_message_relay.Core.UMRType import ChatAttribute, ChatType
from aiocqhttp import MessageSegment
from unified_message_relay.Core.UMRDriver import driver_lookup_table
from umr_coolq_driver import driver as QQ

logger = UMRLogging.get_logger('Plugin.QQ-recall')


# @register_command(cmd=['face'], description='test QQ face')
async def command(chat_attrs: ChatAttribute, args: List):
    if not args:
        return False
    if len(args) != 2:
        return False

    dst_driver_name = args[0]
    dst_chat_id = int(args[1])

    dst_driver = driver_lookup_table.get(dst_driver_name)
    if not dst_driver:
        return

    assert isinstance(dst_driver, QQ.QQDriver)

    context = dict()
    if chat_attrs.chat_type == ChatType.UNSPECIFIED:
        return
    context['message_type'] = f"{chat_attrs.chat_type}"
    context['message'] = list()
    if chat_attrs.chat_type == ChatType.PRIVATE:
        context['user_id'] = dst_chat_id
    else:
        context[f'{chat_attrs.chat_type}_id'] = abs(dst_chat_id)

    for i in range(256):
        context['message'].append(MessageSegment.text(f'Emoji {i}: '))
        context['message'].append(MessageSegment.face(i))
        context['message'].append(MessageSegment.text('\n'))

    await dst_driver.bot.send(context, context['message'])
