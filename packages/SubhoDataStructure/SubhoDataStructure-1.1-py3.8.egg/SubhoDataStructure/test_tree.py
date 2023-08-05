from unittest import TestCase
from SubhoDataStructure.binary_tree import Tree

class TestTree(TestCase):
    def test_add(self):
        print('Tesing add method...')
        bin_tree = Tree()
        self.assertEqual(0, bin_tree.add(5))
        self.assertEqual(1, bin_tree.add(3))
        self.assertEqual(2, bin_tree.add(7))
        self.assertEqual(1, bin_tree.add(2))
        self.assertEqual(2, bin_tree.add(4))
        self.assertEqual(1, bin_tree.add(6))
        self.assertEqual(2, bin_tree.add(8))

    def test_pre_order(self):
        print('Tesing pre_order method...')
        bin_tree = Tree()
        for i in [5, 3, 7, 2, 4, 6, 8]:
            bin_tree.add(i)
        bin_tree.pre_order()
        tmp_lst = [5, 3, 2, 4, 7, 6, 8]
        for i, j in enumerate(bin_tree.stack):
            self.assertEqual(tmp_lst[i], j.val)

    def test_in_order(self):
        print('Tesing in_order method...')
        bin_tree = Tree()
        for i in [5, 3, 7, 2, 4, 6, 8]:
            bin_tree.add(i)
        bin_tree.in_order()
        tmp_lst = [2, 3, 4, 5, 6, 7, 8]
        for i, j in enumerate(bin_tree.stack):
            self.assertEqual(tmp_lst[i], j.val)

    def test_post_order(self):
        print('Tesing post_order method...')
        bin_tree = Tree()
        for i in [5, 3, 7, 2, 4, 6, 8]:
            bin_tree.add(i)
        bin_tree.post_order()
        tmp_lst = [2, 4, 3, 6, 8, 7, 5]
        for i, j in enumerate(bin_tree.stack):
            self.assertEqual(tmp_lst[i], j.val)

    def test_show(self):
        print('Tesing show method...')
        bin_tree = Tree()
        self.assertRaises(ValueError, lambda : bin_tree.show(order='any_order'))

    def test_size(self):
        print('Testing size method...')
        bin_tree = Tree()
        for i in range(10):
            bin_tree.add(i)
        self.assertEqual(10, bin_tree.size())

        bin_tree = Tree()
        for i in range(5):
            bin_tree.add(1)
        self.assertEqual(1, len(bin_tree))

    def test_find(self):
        print('Testing find method...')
        bin_tree = Tree()
        self.assertRaises(ValueError, lambda : bin_tree.find(1))
        tmp_lst = [5, 3, 2, 4, 7, 6, 8]
        for i in tmp_lst:
            bin_tree.add(i)
        for i in tmp_lst:
            self.assertEqual(i, bin_tree.find(i).val)
        self.assertEqual(None, bin_tree.find(50))
        self.assertEqual(None, bin_tree.find(30))

    def test_copy(self):
        print('Testing copy method...')
        bin_tree = Tree()
        tmp_lst = [5, 3, 2, 4, 7, 6, 8]
        for i in tmp_lst:
            bin_tree.add(i)
        tmp = bin_tree.copy()
        tmp.pre_order()
        for i, j in zip(tmp_lst, tmp.stack):
            self.assertEqual(i, j.val)

if __name__ == '__main__':
    TestTree()
