import yaml
import pathlib
import os
from typing import Dict, List, Optional
from typing_extensions import Literal
from unified_message_relay.Core import UMRLogging
from unified_message_relay.Core.UMRMessageHook import register_hook
from unified_message_relay.Core.UMRCommand import register_command, quick_reply
from unified_message_relay.Core.UMRType import UnifiedMessage, ChatAttribute, Privilege
from unified_message_relay.Core.UMRExtension import BaseExtension, register_extension
from unified_message_relay.Core import UMRConfig


logger = UMRLogging.get_logger('Plugin.WaterMeter')


# Telegram water meter filter
# supports keyword filter, forward source filter(chat id based)

class TelegramWaterMeterConfig(UMRConfig.BaseExtensionConfig):
    Extension: Literal['TelegramWaterMeter']
    Keyword: Optional[List[str]]
    ChatID: Optional[List[int]]


UMRConfig.register_extension_config(TelegramWaterMeterConfig)


class TelegramWaterMeter(BaseExtension):
    def __init__(self):
        super().__init__()

    async def post_init(self):
        await super().post_init()

        self.config: TelegramWaterMeterConfig = \
            UMRConfig.config.ExtensionConfig.setdefault(__name__,
                                                        TelegramWaterMeterConfig(
                                                            Extension='TelegramWaterMeter',
                                                            Keyword=[],
                                                            ChatID=[]))

        @register_hook(src_driver='Telegram')
        async def message_hook_func(message: UnifiedMessage) -> bool:
            # filter source
            if message.chat_attrs.forward_from and message.chat_attrs.forward_from.chat_id in self.config.ChatID:
                await quick_reply(message.chat_attrs, 'Message blocked by rule (channel)')
                return True

            # filter keyword
            raw_text = message.text
            for keyword in self.config.Keyword:
                if keyword in raw_text:
                    await quick_reply(message.chat_attrs, f'Message blocked by rule (keyword: {keyword})')
                    return True

            return False

        @register_command(cmd=['block_channel', 'bc'], platform='Telegram', description='register block channel',
                          privilege=Privilege.BOT_ADMIN)
        async def command(chat_attrs: ChatAttribute, args: List):
            if not chat_attrs.reply_to:
                await quick_reply(chat_attrs, 'Message not specified, please reply to a message')
                return False
            reply_chat_attrs = chat_attrs.reply_to
            if not reply_chat_attrs.forward_from:  # definitely not a channel
                await quick_reply(chat_attrs, 'Message is not a forward')
                return False
            if reply_chat_attrs.forward_from.chat_id >= 0:
                await quick_reply(chat_attrs, 'Message is not from channel')
                return False
            channel_id = reply_chat_attrs.forward_from.chat_id
            if channel_id in self.config.ChatID:
                await quick_reply(chat_attrs, 'Channel already exists')
            else:
                self.config.ChatID.append(reply_chat_attrs.forward_from.chat_id)
                UMRConfig.save_config()
                await quick_reply(chat_attrs, f'Success, added channel {reply_chat_attrs.forward_from.name}')

        @register_command(cmd=['block_keyword', 'bk'], platform='Telegram', description='register block keyword',
                          privilege=Privilege.BOT_ADMIN)
        async def command(chat_attrs: ChatAttribute, args: List):
            if not args:
                await quick_reply(chat_attrs, 'Empty keyword list')
                return False

            old_keywords = set(self.config.Keyword)
            new_keywords = set(args)

            exists_keywords = old_keywords & new_keywords
            added_keywords = new_keywords - exists_keywords
            if added_keywords:
                self.config.Keyword = list(old_keywords | new_keywords)
                UMRConfig.save_config()
                if exists_keywords:
                    await quick_reply(chat_attrs, f'Success, added keywords: {", ".join(added_keywords)}\n'
                                                  f'exists keywords: {", ".join(exists_keywords)}')
                await quick_reply(chat_attrs, f'Success, added keywords: {", ".join(added_keywords)}')
            else:
                await quick_reply(chat_attrs, f'All keyword exists: {", ".join(exists_keywords)}')


register_extension(TelegramWaterMeter())
