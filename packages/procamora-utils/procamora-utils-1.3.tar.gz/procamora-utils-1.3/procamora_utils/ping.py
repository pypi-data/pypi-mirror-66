#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import platform
import subprocess
from typing import NoReturn, Text, List

from procamora_utils.ip import IP
from procamora_utils.logger import get_logging

logger: logging = get_logging(False, 'ping')


def ping(hostname: IP) -> bool:
    # Posibles opciones: 'Linux', 'Darwin', 'Java', 'Windows'
    command: Text
    if platform.uname()[0] == 'Linux':
        command = f'ping -c 1 {hostname.get_addr()}'
    elif platform.uname()[0] == 'Windows':
        command = f'ping -n 1 {hostname.get_addr()}'
    else:
        logger.error(f'{platform.uname()[0]} operating system temporarily not supported')
        raise OSError(f'{platform.uname()[0]} operating system temporarily not supported')

    logger.debug(command)

    a: subprocess.CompletedProcess = subprocess.run(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 0 -> Ejecucion correcta (online)
    # 1 -> Error (ofline)
    response: bool = False
    if a.returncode == 0:
        response = True

    # and then check the response...
    if response:
        logger.debug(f'{hostname.get_addr()} is up!!')
    else:
        logger.debug(f'{hostname.get_addr()} is down :(')
    return response


def main() -> NoReturn:
    ips: List[IP] = [IP(ip="127.0.0.1"), IP(ip="192.168.0.103"), IP(fqdn="google.es"), IP(fqdn="google.false")]

    for ip in ips:
        texto: bool = ping(ip)
        if texto:
            logger.info("{} up".format(ip.get_addr()))
        else:
            logger.info("{} down".format(ip.get_addr()))


if __name__ == '__main__':
    main()
