#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = ['conection_sqlite', 'execute_script_sqlite', 'dump_database']

import logging
import sqlite3
import sys
from pathlib import Path  # nueva forma de trabajar con rutas
from threading import Lock
from typing import Dict, Any, List, Union, Tuple, Optional, Text

from procamora_utils.logger import get_logging

logger: logging = get_logging(False, 'sqlite')


def conection_sqlite(database: Path, query: Text, mutex: Lock = None, is_dict: bool = False) \
        -> Union[List[Dict[Text, Any]], List[Tuple[Any, ...]], None]:
    if mutex is not None:
        mutex.acquire()  # bloqueamos acceso a db
    try:
        if database.exists():
            connection: sqlite3.Connection = sqlite3.connect(str(database))
            if is_dict:
                connection.row_factory = _dict_factory
            cursor: sqlite3.Cursor = connection.cursor()
            cursor.execute(query)

            data: Optional[List] = None
            if query.upper().startswith('SELECT'):
                data = cursor.fetchall()  # Traer los resultados de un select
            else:
                connection.commit()  # Hacer efectiva la escritura de datos

            cursor.close()
            connection.close()
            return data
        else:
            logger.critical(f'Database {database} not exits')
            raise OSError(f'Database {database} not exits')
    except sqlite3.OperationalError as e:
        logger.critical(f'LOCK DB in query: {query}, sorry...')
        logger.critical(e)
        if mutex is not None:
            mutex.release()  # liberamos mutex
        sys.exit(-1)
    finally:
        if mutex is not None:
            mutex.release()  # liberamos mutex


def _dict_factory(cursor: sqlite3.Cursor, row: Tuple[Text]) -> Dict[Text, Text]:
    d: Dict = dict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def execute_script_sqlite(database: Path, script: Text) -> None:
    connection: sqlite3.Connection = sqlite3.connect(str(database))
    cursor: sqlite3.Cursor = connection.cursor()
    cursor.executescript(script)
    connection.commit()
    cursor.close()
    connection.close()


def dump_database(database: Path) -> Optional[Text]:
    """
    Hace un dump de la base de datos y lo retorna
    :param database: ruta de la base de datos
    :return dump: volcado de la base de datos
    """
    if database.exists():
        connection: sqlite3.Connection = sqlite3.connect(str(database))
        a: Text = '\n'.join(connection.iterdump())
        return str(a)
    return None
