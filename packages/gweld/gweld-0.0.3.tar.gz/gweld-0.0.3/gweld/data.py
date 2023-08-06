class Data:
    def __init__(self, data=[], labels=[]):
        self.data = list(data)
        self.labels = labels

    def __repr__(self):
        return f'Data({self.data!r})'

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    @property
    def max(self):
        if len(self.data):
            return max(self.data)
        else:
            return 1

    @property
    def min(self):
        if len(self.data):
            return min(self.data)
        else:
            return 0
