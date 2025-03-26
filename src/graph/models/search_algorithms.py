from abc import ABC, abstractmethod

from .tree import TreeModel
from collections import deque


class SearchAlgorithm(ABC):


    def search(self, tree: TreeModel, start_node: str, end_node: str) -> tuple[int, list[str]]:
        steps_count = 1
        if start_node == end_node:
            return 1, [start_node]

        self.prepare(tree, start_node, end_node)

        while self.is_possible_to_iterate():
            self.iterate(tree, start_node, end_node)
            steps_count += 1

        found_way: tuple[int, list[str]] = self.recreate_way(tree, start_node, end_node)

        return steps_count, found_way


    @abstractmethod
    def prepare(self, tree: TreeModel, start_node: str, end_node: str):
        pass

    @abstractmethod
    def is_possible_to_iterate(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def iterate(self, tree: TreeModel, start_node: str, end_node: str) -> None:
        pass

    @abstractmethod
    def recreate_way(self, tree: TreeModel, start_node: str, end_node: str) -> list[str]:
        pass



class SearchBFS(SearchAlgorithm):

    def __init__(self):
        self.opened: deque[str] = deque()
        self.closed: set[str] = set()
        self.pointers: dict[str, str] = {}
        self.current: str = ""

    def prepare(self, tree: TreeModel, start_node: str, end_node: str):
        self.opened = deque(start_node)
        self.closed = set()
        self.pointers = {}
        self.current = start_node


    def is_possible_to_iterate(self) -> bool:
        return len(self.opened) != 0

    def iterate(self, tree: TreeModel, start_node: str, end_node: str):

        self.current = self.opened[0]

        if self.current not in self.closed:
            self.closed.add(self.current)

        if self.current == end_node:
            self.opened = deque()
            return

        self.opened.popleft()

        for child in tree.get_node_info(self.current):
            if child in self.closed:
                continue
            self.pointers[child] = self.current
            self.opened.append(child)

    def recreate_way(self, tree: TreeModel, start_node: str, end_node: str) -> list[str]:

        way = [end_node]
        self.current = end_node
        try:

            while self.pointers[self.current] != start_node:
                self.current = self.pointers[self.current]
                way.append(self.current)

            way.append(start_node)
            return way[::-1]


        except KeyError:
            return []


