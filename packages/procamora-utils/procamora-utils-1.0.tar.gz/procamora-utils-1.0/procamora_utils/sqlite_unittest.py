#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import unittest
from pathlib import Path
from typing import NoReturn, Text, List, Dict, Any

from procamora_utils.interface_sqlite import *

# CUIDADO CON LAS MODIFICACIONES, LA COMPARACION SE HACE CON EL TAMAÑO (724)
dump_str: Text = '''BEGIN TRANSACTION;
DROP TABLE IF EXISTS "table1";
CREATE TABLE IF NOT EXISTS "table1" (
    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "value"	TEXT NOT NULL
);
DROP TABLE IF EXISTS "table2";
CREATE TABLE IF NOT EXISTS "table2" (
    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    "value2"	INTEGER NOT NULL
);
INSERT INTO "table1" VALUES (1,'Python');
INSERT INTO "table1" VALUES (2,'Java');
INSERT INTO "table1" VALUES (3,'C++');
INSERT INTO "table1" VALUES (4,'Bash');
INSERT INTO "table2" VALUES (1,2.7);
INSERT INTO "table2" VALUES (2,3.5);
INSERT INTO "table2" VALUES (3,3.6);
INSERT INTO "table2" VALUES (4,3.7);
INSERT INTO "table2" VALUES (5,3.8);
COMMIT;
'''


class TestSQLite(unittest.TestCase):
    def setUp(self: TestSQLite) -> NoReturn:
        self.dump: Path = Path('resources/unittest.sql')
        self.db: Path = Path('resources/unittest.db')

        # La libreria no tiene el dump ni la bd, por lo que tiene que crearlos la primera vez
        self.dump.write_text(dump_str)
        execute_script_sqlite(self.db, self.dump.read_text())

        self.expect1: List[Dict[Text, Any]] = [{'id': 1, 'value': 'Python'}, {'id': 2, 'value': 'Java'},
                                               {'id': 3, 'value': 'C++'}, {'id': 4, 'value': 'Bash'}]
        self.expect2: List[Dict[Text, Any]] = [{'id': 1, 'value2': 2.7}, {'id': 2, 'value2': 3.5},
                                               {'id': 3, 'value2': 3.6}, {'id': 4, 'value2': 3.7},
                                               {'id': 5, 'value2': 3.8}]
        self.insert: Text = 'Perl'

    def test_exist_db(self: TestSQLite):
        """
        Compruebo que se manda una excepcion si la BD no existe
        :return:
        """
        db: Path = Path('false.db')
        query: Text = "SELECT * FROM table1"
        self.assertRaises(OSError, conection_sqlite, db, query)

    # ontengo valores de tabla1
    def test_select_table1(self: TestSQLite):
        """
        Compruebo que obtiene correctamente todos los valores de la tabla1
        :return:
        """
        query: Text = "SELECT * FROM table1"
        response_query: List[Dict[Text, Any]] = conection_sqlite(self.db, query, is_dict=True)
        self.assertEqual(len(response_query), len(self.expect1), msg="table1 missing values are not expected")

    def test_select_table2(self: TestSQLite):
        """
        Compruebo que obtiene correctamente todos los valores de la tabla2
        :return:
        """
        query: Text = "SELECT * FROM table2"
        response_query: List[Dict[Text, Any]] = conection_sqlite(self.db, query, is_dict=True)
        self.assertEqual(len(response_query), len(self.expect2), msg="table2 missing values are not expected")

    def test_insert_table1(self: TestSQLite):
        """
        Compruebo que se puede insertar correctamente un elemento
        :return:
        """
        query: Text = f"INSERT INTO table1(value) VALUES ('{self.insert}')"
        conection_sqlite(self.db, query)

        query: Text = f"SELECT * FROM table1 WHERE value LIKE '{self.insert}'"
        response_query: List[Dict[Text, Any]] = conection_sqlite(self.db, query, is_dict=True)
        self.assertEqual(len(response_query), 1, msg="insert failed")

    def test_delete_table1(self: TestSQLite):
        """

        :return:
        """
        query: Text = f"DELETE FROM table1 WHERE value LIKE 'Python'"
        conection_sqlite(self.db, query)
        # Confirmacion de que se ha borrado, volviendo a comprar que esta la tabla ya NO esta como antes
        query: Text = "SELECT * FROM table1"
        response_query: List[Dict[Text, Any]] = conection_sqlite(self.db, query, is_dict=True)
        self.assertNotEqual(len(response_query), len(self.expect1), msg="table1 missing values are not expected")

    def test_dump(self: TestSQLite):
        # FIXME Comprobar que el tamaño no cambia nunca
        response = dump_database(self.db)
        self.assertEqual(len(response), 724, msg="dump missing values are not expected")

    def tearDown(self: TestSQLite) -> None:
        """
        Tras cada test restauramos la bd
        :return:
        """
        execute_script_sqlite(self.db, self.dump.read_text())


if __name__ == '__main__':
    unittest.main()
