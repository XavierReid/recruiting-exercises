import unittest
from InventoryAllocator import InventoryAllocator


class TestInventoryAllocator(unittest.TestCase):
    def setUp(self):
        self.allocator = InventoryAllocator()

    def test_exact_inventory_match(self):
        order, warehouses = {"apple": 1}, [
            {"name": "owd", "inventory": {"apple": 1}}]
        output = self.allocator.process_order(order, warehouses)
        self.assertEqual(output, [{"owd": {"apple": 1}}])

    def test_not_enough_inventory(self):
        order, warehouses = {"apple": 1}, [
            {"name": "owd", "inventory": {"apple": 0}}]
        output = self.allocator.process_order(order, warehouses)
        self.assertEqual(output, [])

    def test_split_item_across_warehouses(self):
        order, warehouses = {"apple": 10}, [
            {"name": "owd", "inventory": {"apple": 5}}, {"name": "dm", "inventory": {"apple": 5}}]
        output = self.allocator.process_order(order, warehouses)
        self.assertEqual(output, [{"owd": {"apple": 5}}, {"dm": {"apple": 5}}])

    def test_empty_order(self):
        order, warehouses = {}, [
            {"name": "owd", "inventory": {"apple": 0}}]
        output = self.allocator.process_order(order, warehouses)
        self.assertTrue(not order)
        self.assertEqual(output, [])

    def test_empty_warehouses(self):
        order, warehouses = {"apple": 1}, []
        output = self.allocator.process_order(order, warehouses)
        self.assertTrue(not warehouses)
        self.assertEqual(output, [])

    def test_invalid_inputs(self):
        order, warehouses = 404, "warehouses"
        self.assertNotIsInstance(order, dict)
        self.assertNotIsInstance(warehouses, list)
        output = self.allocator.process_order(order, warehouses)
        self.assertEqual(output, [])

    def test_only_one_invalid_inputs(self):
        order, warehouses = {"apple": 10}, "warehouses"
        self.assertIsInstance(order, dict)
        self.assertNotIsInstance(warehouses, list)
        output = self.allocator.process_order(order, warehouses)
        self.assertEqual(output, [])

    def test_multiple_items_in_order(self):
        order = {"apple": 5, "banana": 5, "orange": 5}
        warehouses = [{"name": "owd", "inventory": {"apple": 5, "orange": 10}}, {
            "name": "dm", "inventory": {"banana": 5, "orange": 10}}]
        output = self.allocator.process_order(order, warehouses)
        self.assertEqual(
            output, [{'owd': {'apple': 5, 'orange': 5}}, {'dm': {'banana': 5}}])

    def test_almost_fulfilled_order(self):
        order = {"apple": 5}
        warehouses = [{"name": "owd", "inventory": {"apple": 2}}, {
            "name": "dm", "inventory": {"apple": 0}}, {"name": "fs", "inventory": {"apple": 1}}]
        output = self.allocator.process_order(order, warehouses)
        self.assertEqual(output, [])

    def test_multiple_warehouses_satisfy(self):
        order = {"apple": 1, "banana": 4, "pear": 4, "orange": 1}
        warehouses = [{"name": "a", "inventory": {"apple": 1, "banana": 2}}, {"name": "b", "inventory": {
            "banana": 2, "pear": 2}}, {"name": "c", "inventory": {"pear": 1, "apple": 2}},
            {"name": "d", "inventory": {"orange": 1, "banana": 2, "pear": 3}}]
        output = self.allocator.process_order(order, warehouses)
        expected = [{"a": {"apple": 1, "banana": 2}}, {"b": {"banana": 2, "pear": 2}}, {
            "c": {"pear": 1}}, {"d": {"orange": 1, "pear": 1}}]
        self.assertTrue(output, expected)


if __name__ == '__main__':
    unittest.main()
