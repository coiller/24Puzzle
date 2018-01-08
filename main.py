import copy
import random
import time


class Node(object):

    def __init__(self, data, depth):
        Node.is_legal_data(data)
        self.data = data
        self.depth = depth

    def __eq__(self, other):
        return self.data == other.data and isinstance(other, Node)

    def __str__(self):
        s = '\n'.join("  ".join(['%02d' % (self.data[row][column])
                                 for column in
                                 range(len(self.data[row]))])
                      for row in
                      range(len(self.data)))
        return "".join(["当前步数：{}\n".format(self.depth + 1), s])

    def __repr__(self):
        return '\n'.join("  ".join(['%02d' % (self.data[row][column])
                                    for column in
                                    range(len(self.data[row]))])
                         for row in
                         range(len(self.data)))

    def __getitem__(self, item):
        return self.data[item]

    @classmethod
    def copy(cls, node):
        '''return a deep copy of self.data, self.depth'''
        return Node(copy.deepcopy(node.data), copy.deepcopy(node.depth))

    @classmethod
    def get_blank_position(cls, p_node):
        '''get the position of 0. range from (0, 0) to (4 , 4)'''
        for row in range(len(p_node.data)):
            for column in range(len(p_node.data[row])):
                if p_node.data[row][column] == 0:
                    return row, column

    @classmethod
    def is_legal_data(cls, data):
        '''check if the data is 2-dimension data'''
        temp_list = list()
        assert len(data) == 5
        for x in data:
            assert len(x) == 5
            for y in x:
                temp_list.append(y)
        temp_list.sort()
        assert temp_list == list(range(25))

    @classmethod
    def can_move(cls, p_node, direction_str):
        '''return if p_node can move to the specified direction
            U for up, D for down, L for left, R for right'''
        if direction_str == "U":
            return not Node.get_blank_position(p_node)[0] == 0
        elif direction_str == "D":
            return not Node.get_blank_position(p_node)[0] == 4
        elif direction_str == "L":
            return not Node.get_blank_position(p_node)[1] == 0
        elif direction_str == "R":
            return not Node.get_blank_position(p_node)[1] == 4
        else:
            SystemError("no such direction: {}".format(direction_str))

    @classmethod
    def move(cls, p_node, direction_str):
        '''move the blank of p_node to the specified direction
            U for up, D for down, L for left, R for right'''
        x, y = Node.get_blank_position(p_node)
        if direction_str == "U":
            p_node[x][y], p_node[x - 1][y] = p_node[x - 1][y], p_node[x][y]
        elif direction_str == "D":
            p_node[x][y], p_node[x + 1][y] = p_node[x + 1][y], p_node[x][y]
        elif direction_str == "L":
            p_node[x][y], p_node[x][y - 1] = p_node[x][y - 1], p_node[x][y]
        elif direction_str == "R":
            p_node[x][y], p_node[x][y + 1] = p_node[x][y + 1], p_node[x][y]
        else:
            SystemError("no such direction: {}".format(direction_str))

    @classmethod
    def random_node(cls, depth=0, max_dis=100):
        '''generate random node, default depth = 0'''
        dis = max_dis + 1
        while (dis > max_dis):
            gen_list = list(range(25))
            target_data = []
            for i in range(5):
                temp = []
                for j in range(5):
                    choice = random.choice(gen_list)
                    temp.append(choice)
                    gen_list.remove(choice)
                target_data.append(temp)
            dis = Node.get_dis(Node(target_data, depth))
        return Node(target_data, depth)

    @classmethod
    def get_parity(cls, p_node):
        '''return the parity, false to odd, true to oven'''
        temp = []
        for row in range(len(p_node.data)):
            for column in range(len(p_node.data[row])):
                temp.append(p_node.data[row][column])
        temp.remove(0)
        parity_count = 0
        for i in range(len(temp)):
            for j in range(i):
                if temp[j] > temp[i]:
                    parity_count += 1

    @classmethod
    def get_dis(cls, p_nod):
        '''return the manhattan distence'''
        dis = 0
        for row in range(len(p_nod.data)):
            for column in range(len(p_nod.data[row])):
                if p_nod.data[row][column] == 0:
                    continue
                dis = dis + abs(row - int(p_nod.data[row][column] / 5)) +\
                    abs(column - p_nod.data[row][column] % 5)
        return dis

    @classmethod
    def heuristic_funtion(cls, p_node, target_node,
                          factor_a=1, factor_b=1):
        '''return the value of F(x) = a*G(x) + b*H(x)
            where G(x) is the depth, a is factor,
            and H(x) is the expectation, b is factor'''
        # counter = 0
        # for row in range(len(p_node.data)):
        #     for column in range(len(p_node.data[row])):
        #         if p_node.data[row][column] != target_node.data[row][column]:
        #             counter += 1
        # return factor_a * p_node.depth + factor_b * counter
        return factor_a * p_node.depth + factor_b * Node.get_dis(p_node)

    @classmethod
    def get_node_heuristic(cls, opened_list, target_node,
                           factor_a, factor_b):
        '''get the best node from opened_list accroding to heuristic funtion'''
        best_node_index = 0
        best_node_value = Node.heuristic_funtion(
            opened_list[0][1], target_node, factor_a, factor_b)
        for i in range(1, len(opened_list)):
            if opened_list[i][0] is None:
                temp_value = Node.heuristic_funtion(
                    opened_list[i][1], target_node, factor_a, factor_b)
                opened_list[i][0] = temp_value
            else:
                temp_value = opened_list[i][0]
            if best_node_value >= temp_value:
                best_node_index = i
                best_node_value = temp_value
        return opened_list.pop(best_node_index)[1]


class NodeUtils(object):
    '''some utils about the node'''

    @classmethod
    def show_resolve_path(cls, final_node):
        '''show the path from start to final'''
        cursor = final_node
        temp = []
        while hasattr(cursor, "prev"):
            temp.append(cursor)
            cursor = cursor.prev
        temp.append(cursor)
        while not len(temp) == 0:
            yield temp.pop()


def heuristic_search(
        p_startpoint, p_endpoint, factor_a=1, factor_b=1, vale=100):
    # 深拷贝
    startpoint = copy.deepcopy(p_startpoint)
    endpoint = copy.deepcopy(p_endpoint)
    # 检查奇偶性
    if Node.get_parity(startpoint) != Node.get_parity(endpoint):
        return list()
    # 数据结构初始化
    opened_nodes = [[None, startpoint], ]
    closed_nodes = []
    while True:
        if opened_nodes == []:
            print('Warning:Vale is too small!')
            return list()
        current_node = Node.get_node_heuristic(
            opened_nodes, endpoint, factor_a, factor_b)
        # 分析节点, 如果是目标节点则结束搜索
        if current_node == endpoint:
            return list(NodeUtils.show_resolve_path(current_node))
        # 如果不是目标节点，存入搜索历史
        closed_nodes.append(current_node)
        # 拓展节点
        for direction_str in ["U", "D", "L", "R"]:
            if Node.can_move(current_node, direction_str):
                new_node = Node.copy(current_node)
                Node.move(new_node, direction_str)
                if new_node not in closed_nodes:
                    if Node.heuristic_funtion(new_node, endpoint,
                                              factor_a, factor_b) <= vale:
                        opened_nodes.append([None, new_node])
                new_node.depth += 1
                new_node.prev = current_node
    # 搜索不到时返回空列表
    return list()


def backward(p_endpoint, steps=50):
    # 生成由目标节点任意倒退steps步的初始节点
    current_node = copy.deepcopy(p_endpoint)
    for step in range(steps):
        direction_str = random.choice(["U", "D", "L", "R"])
        if Node.can_move(current_node, direction_str):
            Node.move(current_node, direction_str)
        else:
            step -= 1
    return current_node


def main():
    # 指定生成节点
    # startpoint = Node([
    #     [0, 1, 2, 3, 4],
    #     [5, 6, 7, 8, 9],
    #     [10, 11, 12, 13, 14],
    #     [15, 16, 17, 18, 19],
    #     [20, 21, 22, 23, 24],
    # ], 0)
    endpoint = Node([
        [0, 1, 2, 3, 4],
        [5, 6, 7, 8, 9],
        [10, 11, 12, 13, 14],
        [15, 16, 17, 18, 19],
        [20, 21, 22, 23, 24],
    ], 0)
    startpoint = backward(endpoint, steps=200)

    # # 随机生成有效节点
    # while True:
    #     startpoint = Node.random_node(max_dis=50)
    #     # endpoint = Node.random_node()
    #     if Node.get_parity(startpoint) == Node.get_parity(endpoint):
    #         break

    # 输出初始节点信息
    print('起始状态:\n{}'.format(startpoint.__repr__()))
    print('结束状态:\n{}'.format(endpoint.__repr__()))

    # 启发式搜索
    t1 = time.time()
    result_list = heuristic_search(
        startpoint, endpoint, factor_a=1, factor_b=11, vale=300)
    if result_list:
        print('[启发式搜索] 共耗时{:.3}s.'.format(time.time() - t1), end="")
        print('(共{}步):'.format(len(result_list)))
        for x in result_list:
            print(str(x))
    else:
        print('max depth reached. search failed.')


if __name__ == '__main__':
    main()
