__author__ = 'Martijn Schut'

class Inventory(object):
    def __init__(self, inv_size, creature):
        self.creature = creature
        self.inv_size = inv_size
        self.items = [None for i in range(10)]

    def sort(self):
        self.items = sorted(self.items, key=lambda x: (x is None, x))

    def get_len(self):
        return len(self.items)

    def get_fill(self):
        count = 0
        for x in range(0, len(self.items)):
            if self.items[x] is not None:
                count += 1
        return count

    def get_items(self):
        return self.items

    def add(self, item):
        for i in range (0, len(self.items)):
            if self.items[i] is None:
                self.items[i] = item
                break

    def remove(self, item):
        for i in range (0, len(self.items)):
            if self.items[i] == item:
                self.items[i] = None
                print self.items
                break

    def get_item_at_index(self, index):
        return self.items[index]

    def is_full(self):
        size = 0
        for i in range (0, len(self.items)):
            if (self.items[i] != None):
                size += 1

        return size == len(self.items)

    def get_edible_items(self):
        e_items = []
        for x, item in enumerate(self.items):
            if item is not None:
                if item.nutrition != 0 or item.taste is not None:
                    e_items.append(item)

        while len(e_items) < self.inv_size:
            e_items.append(None)

        return e_items

    def get_wearable_items(self):
        w_items = []
        for x, item in enumerate(self.items):
            if item is not None:
                if item.wearable:
                    w_items.append(item)

        while len(w_items) < self.inv_size:
            w_items.append(None)

        return w_items

    def get_equipable_items(self):
        q_items = []
        for x, item in enumerate(self.items):
            if item is not None:
                if item.holdable:
                    q_items.append(item)

        while len(q_items) < self.inv_size:
            q_items.append(None)

        return q_items