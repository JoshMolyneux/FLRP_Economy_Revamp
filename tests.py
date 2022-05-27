import mariadb
import unittest
from . import config
from config import test_config
import utils


class phaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            connect = mariadb.connect(**test_config, autocommit=True)
        except mariadb.Error as e:
            print(f"There was an error connecting to MariaDB: {e}")
        cursor = connect.cursor()

        try:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS players (
                    _Key int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    _Money int(11) NOT NULL DEFAULT 0,
                    _Inventory mediumtext DEFAULT NULL,
                    _Invvalue int(11) NOT NULL DEFAULT 0)
                """
            )
        except mariadb.Error as e:
            print(f"There was an error creating tables: {e}")
        cursor.close()
        cursor = connect.cursor()
        try:
            utils.sql_write(
                """
                INSERT INTO players
                    (_Key, _Money, _Inventory, _Invvalue)
                VALUES
                    (1, 1500000, 'life_alert: 1; Cabbie: 1; Audi: 1; cw_m3super90: 4', 241000),
                    (2, 10000, 'chinese: 5', 1250),
                    (3, 52364323, 'bmwgtr: 1; uniform_fireman: 1', 100000),
                    (4, 199999, 'deliverytruckbox: 1; jagftype: 1; unrefined_ore: 23', 871725),
                    (5, 5000000, 'weapon_molotovschematics: 1; tides: 2; cw_makarov: 21', 260025),
                    (6, 749999, 'accessory_paperbaghat: 1', 40000),
                    (7, 499999, '', 0)
                """
            )
        except mariadb.Error as e:
            print(f"There was an error inserting data: {e}")
        cursor.close()

    @classmethod
    def tearDownClass(cls):
        try:
            connect = mariadb.connect(
                **test_config,
                autocommit=True
            )
        except mariadb.Error as e:
            print(f"There was an error connecting to MariaDB: {e}")

        cursor = connect.cursor()
        cursor.execute("DROP TABLE IF EXISTS players")
        cursor.close()
        connect.close()

    def setUp(self):
        connect = mariadb.connect(**test_config, autocommit=True)
        self.cursor = connect.cursor()

    def tearDown(self):
        self.cursor.close()

    def test_generic_all_rows_returned(self):
        actual = len(utils.sql_read("SELECT * FROM players"))
        expected = 7
        self.assertEqual(actual, expected)

    #def test_phase_1_


if __name__ == "__main__":
    unittest.main(verbosity=2)
