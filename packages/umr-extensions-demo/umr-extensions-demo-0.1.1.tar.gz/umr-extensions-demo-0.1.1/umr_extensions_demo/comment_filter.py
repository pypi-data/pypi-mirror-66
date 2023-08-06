from unified_message_relay.Core import UMRLogging
from unified_message_relay.Core.UMRMessageHook import register_hook
from unified_message_relay.Core.UMRCommand import quick_reply
from unified_message_relay.Core.UMRType import UnifiedMessage

logger = UMRLogging.get_logger('Plugin.Comment')


# Filter messages that start with //

@register_hook()
async def message_hook_func(message: UnifiedMessage) -> bool:
    # filter keyword
    raw_text = message.message
    if raw_text.startswith('//'):
        await quick_reply(message.chat_attrs, f'Message filtered')
        return True

    return False
