class Node:
    def __init__(self, val):
        self.val = val;
        self.left_child = None
        self.right_child = None

class Tree:
    def __init__(self):
        self.root = None
        self.stack = []

    def add(self, val):
        """
        Add new value to the tree.

        :param val: value may be integer, float or node
        :return: if the value is added to the root then return 0,
        if the value is added to the left side of the parent node then return 1,
        if the value is added ot the right side of the parent node then return 2,
        and if the value is already in the tree then is return -1
        """
        if type(val) == Node:
            val = val.val
        if self.root == None:
            self.root = Node(val)
            return 0
        else:
            return self.__add(self.root, val)

    def __add(self, cur_node, val):
        if val < cur_node.val:
            if cur_node.left_child == None:
                cur_node.left_child = Node(val)
                return 1
            else:
                return self.__add(cur_node.left_child, val)
        if val > cur_node.val:
            if cur_node.right_child == None:
                cur_node.right_child = Node(val)
                return 2
            else:
                return self.__add(cur_node.right_child, val)
        else:
            return -1

    def pre_order(self):
        if self.root != None:
            self.stack = []
            self.cur_ord = 'pre_order'
            self.cur_ord = None
            self.__pre_order(self.root)
            return 1
        return 0

    def __pre_order(self, cur_node):
        self.stack.append(cur_node)
        if cur_node.left_child != None:
            self.__pre_order(cur_node.left_child)
        if cur_node.right_child != None:
            self.__pre_order(cur_node.right_child)

    def in_order(self):
        if self.root != None:
            self.stack = []
            self.cur_ord = 'in_order'
            self.__in_order(self.root)
            return 1
        return 0

    def __in_order(self, cur_node):
        if cur_node.left_child != None:
            self.__in_order(cur_node.left_child)
        self.stack.append(cur_node)
        if cur_node.right_child != None:
            self.__in_order(cur_node.right_child)


    def post_order(self):
        if self.root != None:
            self.stack = []
            self.cur_ord = 'post_order'
            self.__post_order(self.root)
            return 1
        return 0

    def __post_order(self, cur_node):
        if cur_node.left_child != None:
            self.__post_order(cur_node.left_child)
        if cur_node.right_child != None:
            self.__post_order(cur_node.right_child)
        self.stack.append(cur_node)

    def level_order(self):
        if self.root != None:
            self.stack = []
            self.cur_ord = 'level_order'

    def show(self, order = 'pre_order'):
        """
        show all the values of the tree.
        :param order: value may be "pre_order" or "in_order" or "post_order"
        """
        if order == 'pre_order':
            if self.cur_ord != order:
                self.pre_order()
        elif order == 'in_order':
            if self.cur_ord != order:
                self.in_order()
        elif order == 'post_order':
            if self.cur_ord != order:
                self.post_order()
        else:
            raise ValueError('Invalid order %s. valid options are {\"pre_order\", \"in_order\", \"post_order\"}'%(order))

        for node in self.stack:
            print(node.val, end = ' ')
        print()

    def size(self):
        if self.root == None:
            return 0
        else:
            self.pre_order()
            return len(self.stack)

    def __len__(self):
        return self.size()

    def find(self, val, return_parent = False):
        if self.root == None:
            raise ValueError ('Tree is empty!')
        else:
            if self.root.val == val:
                return self.root
            else:
                return self.__find(self.root, val, return_parent)

    def __find(self, cur_node, val, return_parent):
        if val < cur_node.val:
            if cur_node.left_child != None:
                if cur_node.left_child.val == val:
                    if return_parent:
                        return (cur_node.left_child, cur_node)
                    return cur_node.left_child
                else:
                    return self.__find(cur_node.left_child, val, return_parent)
            else:
                return None
        elif val > cur_node.val:
            if cur_node.right_child != None:
                if cur_node.right_child.val == val:
                    if return_parent:
                        return (cur_node.right_child, cur_node)
                    return cur_node.right_child
                else:
                    return self.__find(cur_node.right_child, val, return_parent)
            else:
                return None

    def copy(self):
        if self.root == None:
            raise ValueError ('Tree is empty!')
        else:
            self.tmp = Tree()
            self.tmp.root = Node(self.root.val)
            self.__copy(self.tmp.root, self.root)
            tmp = self.tmp
            del(self.tmp)
            return tmp

    def __copy(self, cur_trg_node, cur_src_node):
        if cur_src_node.left_child != None:
            cur_trg_node.left_child = Node(cur_src_node.left_child.val)
            self.__copy(cur_trg_node.left_child, cur_src_node.left_child)
        if cur_src_node.right_child != None:
            cur_trg_node.right_child = Node(cur_src_node.right_child.val)
            self.__copy(cur_trg_node.right_child, cur_src_node.right_child)