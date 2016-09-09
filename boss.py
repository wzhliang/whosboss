import sys


class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

    def find(self, name):
        if self.name == name:
            return self
        if len(self.children) == 0:
            return None
        for ch in self.children:
            if ch.name == name:
                return ch
        for ch in self.children:
            found = ch.find(name)
            if found:
                return found

    def add_children(self, name):
        n = Node(name)
        n.parent = self
        self.children.append(n)

    def dump(self):
        print(self.name)
        print(",".join([x.name for x in self.children]))
        for ch in self.children:
            ch.dump()

    def __repr__(self):
        return "Node({})({})".format(self.name, len(self.children))


class Finder:
    def __init__(self):
        self.root = None
        self.names = []

    def process_line(self, l):
        boss, worker = l.split()
        if self.root is None or boss not in self.names:
            man = Node(boss)
            man.add_children(worker)
            if self.root is None:
                self.root = man
        else:
            self.root.find(boss).add_children(worker)
        self.names.append(boss)
        self.names.append(worker)

    def do_it(self, fn):
        with open(fn) as fp:
            lines = fp.readlines()
            # first line skipped
            self.name1 = lines[1].strip()
            self.name2 = lines[2].strip()
            for line in lines[3:]:
                self.process_line(line.strip())

        one = self.root.find(self.name1)
        two = self.root.find(self.name2)
        print(self._find_common_boss(one, two))

    def _find_common_boss(self, who1, who2):
        if who1.find(who2.name):
            return who1.name
        if who2.find(who1.name):
            return who2.name
        name = self._find_common_boss(who1.parent, who2)
        if name:
            return name
        name = self._find_common_boss(who2.parent, who1)
        if name:
            return name
        return None


if __name__ == '__main__':
    Finder().do_it(sys.argv[1])
