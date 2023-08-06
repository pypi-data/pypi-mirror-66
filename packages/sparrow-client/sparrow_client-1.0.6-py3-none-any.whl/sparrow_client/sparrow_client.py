import logging
from typing import Union

from .core.queue.sparrow_client_queue import SparrowClientQueue
from .core.slack_command import SlackCommandManager
from .core.sparrow_exception import CommandNotFound
from .core.sparrow_message import SparrowData

logger = logging.getLogger(__name__)


def send_slack(channel: str, message: Union[str, list, dict], title: str = "", color: str = ""):
    """
    Args:
        channel: 메시지를 전송할 channel의 이름
        message: 메시지의 본문
        title: 메시지의 타이틀
        color: slack 메시지의 quote 컬러
    """
    total_len = 0
    sparrow_datas = []
    text_buffer = []

    if isinstance(message, list):
        for item in message:
            text = f">`{item}` \n"
            text_buffer.append(text)
    elif isinstance(message, dict):
        for key, value in message:
            text = f">`{key}`: *{value}*` \n"
            text_buffer.append(text)
    else:
        text_buffer.append(message)

    texts = []
    if len(text_buffer) > 1:
        for text in text_buffer:
            text_len = len(text)
            if total_len + text_len > 4000:
                sparrow_data = SparrowData(channel=channel, title_text=title, color=color, body_text=''.join(texts))
                sparrow_datas.append(sparrow_data)
                total_len = 0
                texts = []
            total_len += text_len
            texts.append(text)
    else:
        texts = text_buffer

    sparrow_data = SparrowData(channel=channel, title_text=title, color=color, body_text=''.join(texts))
    sparrow_datas.append(sparrow_data)

    for sparrow_data in sparrow_datas:
        SparrowClientQueue().push(sparrow_data)

    return


def execute_command(sparrow_data: SparrowData):
    """ 사용자가 입력한 명령어가 존재하는 명령어인지 확인 후, 해당 명령어에 대한 response의 결과를 슬랙으로 전송
    """
    cmd = SlackCommandManager.get_command(sparrow_data.command)

    if cmd is None:
        logging.exception("command not found")
        raise CommandNotFound(sparrow_data.command)

    message = cmd.response(
        user_command=sparrow_data.command,
        channel=sparrow_data.channel,
        username=sparrow_data.username
    )
    send_slack(channel=sparrow_data.channel, message=message, color=cmd.color)
    return
