#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from ipaddress import AddressValueError, ip_interface
from typing import Text, NoReturn

from procamora_utils.logger import get_logging

logger: logging = get_logging(False, 'ip')


@dataclass
class IP:
    REGEX_FQDN: Text = r"(?=^.{4,253}$)(^((?!-)[a-zA-Z0-9-]{0,62}[a-zA-Z0-9]\.)+[a-zA-Z]{2,63}$)"
    ip: Text = None
    fqdn: Text = None

    valid_ip: ip_interface = None

    def __post_init__(self: IP) -> NoReturn:
        """
        Metodo post_inicio encargado de comprobar que la informacion proporcionada es valida
        :return:
        """
        bool_fqnd: bool = False
        bool_ip: bool = False

        if self.fqdn is not None:
            if not re.search(self.REGEX_FQDN, self.fqdn):
                raise AttributeError(f'{self.fqdn} is not valid FQDN')
            else:
                bool_fqnd = True

        if self.ip is not None:
            try:
                self.valid_ip = ip_interface(self.ip)  # throw exception if invalid ip
            except ValueError as e:
                raise AttributeError(f'{e}')
            bool_ip = True

        if not bool_fqnd and not bool_ip:
            raise AttributeError('An IP address or FQDN must be introduced.')

    def get_ip(self: IP) -> Text:
        """
        Metodo para obtener la direccion IP en caso de existir, sino envia una excepcion
        :return:
        """
        if self.valid_ip is None:
            raise AttributeError('IP address is None.')
        return str(self.valid_ip.ip)

    def get_fqdn(self: IP) -> Text:
        """
        Metodo para obtener el FQDN en caso de existir, sino envia una excepcion
        :return:
        """
        if self.fqdn is None:
            raise AttributeError('FQDN is None.')
        return self.fqdn

    def get_addr(self: IP) -> Text:
        """
        Metodo para obtener el FQDN en caso de existir, sino obtiene la direccion IP
        Es recomensable usar este metodo por ser el generico.
        :return:
        """
        if self.fqdn is not None:
            return self.fqdn
        else:
            return str(self.valid_ip.ip)

    def __str__(self: IP) -> Text:
        return f'IP(ip=\'{self.valid_ip}\', fqnd=\'{self.fqdn}\')'


if __name__ == "__main__":
    # print(IP(fqdn='google.es').get_ip())
    print(IP(fqdn='google.es').get_fqdn())
    print(IP(fqdn='google.es').get_addr())

    print(IP(ip='fb7::2').get_ip())
    # print(IP(ip=IPv4Interface('192.168.4.56')).get_fqdn())
    print(IP(ip='fb7::56').get_addr())

    print(IP(ip='192.168.4.56', fqdn='google.es').get_ip())
    print(IP(ip='192.168.4.56', fqdn='google.es').get_fqdn())
    print(IP(ip='192.168.4.56', fqdn='google.es').get_addr())
