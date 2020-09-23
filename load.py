#!/usr/bin/env python
"""plugin that lists every body you discovered in the system you're scanning,
with their type (ww, elw, gg) and a mention if they're terraformable."""

import logging
import os

# This could also be returned from plugin_start3()
plugin_name = os.path.basename(os.path.dirname(__file__))

# Logger per found plugin, so the folder name is included in
# the logging format.
logger = logging.getLogger(f'{appname}.{plugin_name}')
if not logger.hasHandlers():
    level = logging.INFO  # So logger.info(...) is equivalent to print()

    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_channel.setLevel(level)
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')  # noqa: E501
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)


def plugin_start3(plugin_dir: str) -> str:
    """
    Plugin startup method.
    :param plugin_dir:
    :return: 'Pretty' name of this plugin.
    """
    logger.info(f'Folder is {plugin_dir}')

    return plugin_name


def plugin_stop() -> None:
    """
    Plugin stop method.
    :return:
    """
    logger.info('Stopping')


def journal_entry(cmdrname: str, is_beta: bool, system: str, station: str, entry: dict, state: dict) -> None:
    """
    Handle the given journal entry.
    :param cmdrname:
    :param is_beta:
    :param system:
    :param station:
    :param entry:
    :param state:
    :return: None
    """
    logger.debug(f'cmdr = "{cmdrname}", is_beta = "{is_beta}", system = "{system}", station = "{station}"')
    this.mt.store(entry['timestamp'], cmdrname, system, station, entry['event'])