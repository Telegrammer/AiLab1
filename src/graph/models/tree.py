from dataclasses import dataclass
from email.errors import NonPrintableDefect


@dataclass
class NodeInfo:
    children: list[str]

    def add(self, child: str):
        if child not in self.children:
            self.children.append(child)

    def remove(self, child: str):
        self.children.pop(self.children.index(child))




class TreeModel:
    def __init__(self):
        self.__nodes_info: dict[str, NodeInfo] = {}
        self.__nodes: set[str] = set()

    @classmethod
    def from_list(cls, edges_list: list[tuple[str, str]]):
        instance = cls()
        for edge in edges_list:
            instance.add_edge(edge[0], edge[1])
        return instance

    def add_edge(self, start_node: str, end_node: str) -> None:
        if start_node == end_node:
            raise ValueError("Вершины одинаковые")

        if start_node not in self.__nodes_info.keys():
            self.__nodes_info[start_node] = NodeInfo([end_node])
            self.__nodes.add(start_node)
        else:
            self.__nodes_info[start_node].add(end_node)

        self.__nodes.add(end_node)

    def have_parents(self, current: str) -> bool:
        for node in self.__nodes:
            if node == current:
                continue

            if node in self.__nodes_info.keys() and current in self.__nodes_info[node].children:
                return True
        return False

    def remove_edge(self, start_node: str, end_node: str):
        if start_node not in self.__nodes or end_node not in self.__nodes:
            raise ValueError("Одной из вершин не существует")

        if end_node not in self.__nodes_info[start_node].children:
            raise ValueError("Вершины не связаны")

        self.__nodes_info[start_node].remove(end_node)

        if len(self.__nodes_info[start_node].children) == 0:
            self.__nodes_info.pop(start_node)

        if not self.have_parents(start_node) and not self.have_children(start_node):
            self.__nodes.remove(start_node)

        if not self.have_parents(end_node) and end_node not in self.__nodes_info.keys():
            self.__nodes.remove(end_node)



    def have_edge(self, start_node: str, end_node: str) -> bool:
        if start_node not in self.__nodes_info.keys():
            return False

        return end_node in self.__nodes_info[start_node].children


    def get_nodes(self) -> set[str]:
        return self.__nodes

    def get_node_info(self, node: str) -> list[str]:
        return self.__nodes_info[node].children

    def have_children(self, node: str):
        return node in self.__nodes_info.keys()


    def __str__(self):
        return f"Вершины: {self.__nodes}\nСвязи: {self.__nodes_info}"