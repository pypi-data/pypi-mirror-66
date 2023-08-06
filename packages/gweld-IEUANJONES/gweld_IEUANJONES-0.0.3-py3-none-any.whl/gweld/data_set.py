from gweld import Data

class DataSet(Data):
    def __iadd__(self, other):
        if isinstance(other, Data):
            self.data.append(other)
        else:
            raise TypeError

        return self

    def __len__(self):
        return max([len(data) for data in self.data])

    @property
    def max(self):
        return max([max(data) for data in self.data])

    @property
    def min(self):
        return min([min(data) for data in self.data])
