import sys
sys.path.append("..")
import mariadb
import unittest
import test_utils as utils
from econ_revamp import phase1, phase2, phase3, connect, get_all_players
from config import test_db_details


class phaseTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.connect = connect(test=True)

        cls.cursor = cls.connect.cursor()

        try:
            cls.cursor.execute(
                """CREATE TABLE IF NOT EXISTS players (
                    _Key int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    _Money int(11) NOT NULL DEFAULT 0,
                    _Inventory mediumtext DEFAULT NULL,
                    _Invvalue int(11) NOT NULL DEFAULT 0)
                """
            )
        except mariadb.Error as e:
            print(f"There was an error creating tables: {e}")
        cls.cursor.close()
        cls.cursor = cls.connect.cursor()
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
        cls.cursor.close()
        cls.connect.close()

    @classmethod
    def tearDownClass(cls):
        cls.connect = connect(test=True)
        cls.cursor = cls.connect.cursor()
        cls.cursor.execute("DROP TABLE IF EXISTS players")
        cls.cursor.close()
        cls.connect.close()

    def setUp(self):
        self.connect = connect(test=True)
        self.cursor = self.connect.cursor()

    def tearDown(self):
        self.cursor.close()

    def test_generic_all_rows_returned(self):
        users = get_all_players('*', test=True)
        actual = len(users[0])
        expected = 7
        self.assertEqual(actual, expected)

    def test_phase_1_user_has_inventory(self):
        self.cursor.execute("SELECT _Inventory FROM players WHERE _Key = 7")
        result = self.cursor.fetchone()
        actual = phase1.user_has_inventory(result[0])
        expected = False
        self.assertEqual(actual, expected)

    def test_phase_1_inventory_split_into_separate_items(self):
        self.cursor.execute("SELECT _Inventory FROM players WHERE _Key = 4")
        result = self.cursor.fetchone()
        actual = phase1.convert_inventory_into_items(result[0])
        expected = [['deliverytruckbox', '1'], ['jagftype', '1'], ['unrefined_ore', '23']]
        self.assertEqual(actual, expected)

    def test_phase_1_refund_user(self):
        self.cursor.execute("SELECT _Inventory, _Money FROM players")
        result = self.cursor.fetchone()
        items = phase1.convert_inventory_into_items(result[0])
        #self.cursor.execute()


if __name__ == "__main__":
    unittest.main(verbosity=2)
