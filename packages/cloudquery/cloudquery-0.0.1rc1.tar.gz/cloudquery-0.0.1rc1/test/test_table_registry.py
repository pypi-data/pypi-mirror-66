from unittest import TestCase
from unittest.mock import patch

import cloudquery.table_registry
import cloudquery.schema


class ChildSchema(cloudquery.schema.BaseSchema):
    def __init__(self):
        self.var = 't1'


class MetaClass(object):
    child_schema = ChildSchema
    base_schema = cloudquery.schema.BaseSchema


class MockClassOne(object):
    pass


class MockClassTwo(object):
    @classmethod
    def get_table_name(cls):
        return 't2'


class MockClassThree(object):
    @classmethod
    def get_table_name(cls):
        return 't3'


class TestTableRegistry(TestCase):
    @patch('cloudquery.table_registry.registry', [MetaClass])
    def test_get_tables(self):
        tables = cloudquery.table_registry.get_tables()

        self.assertEqual(len(tables), 1)
        self.assertEqual(tables[0].var, 't1')

    @patch('cloudquery.table_registry.get_tables')
    def test_get_obj_by_table_name(self, mock_tables):
        mock_tables.return_value = [
            MockClassOne, MockClassTwo, MockClassThree
        ]

        obj = cloudquery.table_registry.get_obj_by_table_name('t3')
        self.assertEqual(obj.get_table_name(), 't3')

