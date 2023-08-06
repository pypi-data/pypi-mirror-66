import logging

from .parser import PARSER_DICT
from .send_messages import send_message
from .config import Config

logger = logging.getLogger(__name__)


class FindHome(object):
    log = logging.getLogger(__name__)

    def __init__(self, config_filename: str = None):
        self.config = Config(config_filename)

        try:
            self._info_dict = {k: func() for k, func in PARSER_DICT.items()}
            self.log.info(f'Initialized info dict.')
            self.to_admin(f'Program is started!')
        except Exception as err:
            self.log.exception(err)
            self.to_admin(f'An error occurred while parsing sites: {err}.')
            raise Exception(err)

    def check(self):
        for k, func in PARSER_DICT.items():
            try:
                new_info = func()
                self.log.info(f'Parsed site {k}.')
            except Exception as err:
                self.log.exception(err)
                self.to_admin(f'An error occurred while parsing sites: {err}.')
                continue
            if self._info_dict[k] != new_info:
                self.broadcast(new_info)
                self._info_dict[k] = new_info

    def broadcast(self, msg: str):
        self.log.info(f'Broadcasting message: {msg}.')
        try:
            send_message(msg, self.config.server_mail, self.config.password, self.config.recipients,
                         self.config.port, self.config.hostname)
            self.log.info('Message was sent.')
        except Exception as err:
            self.log.exception(err)
            self.to_admin(f'An error occurred while trying to broadcast: {err}.')

    def to_admin(self, msg: str):
        try:
            self.log.info(f'Sending an email to admin: {msg}.')
            send_message(msg, self.config.server_mail, self.config.password, [self.config.admin_email],
                         self.config.port, self.config.hostname)
        except Exception as err:
            self.log.exception(err)
