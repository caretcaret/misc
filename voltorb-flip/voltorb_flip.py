class Grid(list):
    def __init__(self, width, height, iterable=None):
        if iterable is None:
            iterable = [None] * (width * height)
        assert(len(iterable) == width * height)
        super().__init__(iterable)
        self.width = width
        self.height = height

    def __getitem__(self, index):
        if type(index) == int:
            return super().__getitem__(index)
        row, col = index
        return self[row * self.width + col]

    def __setitem__(self, index, value):
        if type(index) == int:
            return super().__setitem__(index, value)
        row, col = index
        self[row * self.width + col] = value
        return value

    def __str__(self):
        out = ""
        for row in range(self.height):
            for col in range(self.width):
                if self[row, col] is None:
                    out += ' ? '
                else:
                    out += ' {} '.format(self[row, col])
            out += '\n'
        return out + '\n'

    def __hash__(self):
        return hash(tuple(self))


class VoltorbFlip(Grid):
    def __init__(self, col_sums, row_sums, known=None):
        super().__init__(len(col_sums), len(row_sums), known)
        self.col_points, self.col_voltorbs = zip(*col_sums)
        self.row_points, self.row_voltorbs = zip(*row_sums)

    def known_row_points(self, row):
        total = 0
        for col in range(self.width):
            total += self[row, col] or 0
        return total

    def known_row_voltorbs(self, row):
        total = 0
        for col in range(self.width):
            total += 1 if self[row, col] == 0 else 0
        return total

    def known_col_points(self, col):
        total = 0
        for row in range(self.height):
            total += self[row, col] or 0
        return total

    def known_col_voltorbs(self, col):
        total = 0
        for row in range(self.height):
            total += 1 if self[row, col] == 0 else 0
        return total

    def find(self, ucp=None, ucv=None, urp=None, urv=None):
        # unknown column points, unknown column voltorbs, unknown row points, unknown row voltorbs
        ucp = ucp or [self.col_points[col] - self.known_col_points(col) for col in range(self.width)]
        ucv = ucv or [self.col_voltorbs[col] - self.known_col_voltorbs(col) for col in range(self.width)]
        urp = urp or [self.row_points[row] - self.known_row_points(row) for row in range(self.height)]
        urv = urv or [self.row_voltorbs[row] - self.known_row_voltorbs(row) for row in range(self.height)]
        # depth first search
        # if any unknowns are negative, there are no possible configurations
        if any([x < 0 for x in ucp + ucv + urp + urv]):
            return set()
        # if there are undetermined tiles left, make the first one determined
        if None in self:
            possible = set()
            index = self.index(None)
            row, col = index // self.width, index % self.width
            # replace tile at index with voltorb
            self[index] = 0
            # update unknowns, find, revert updates
            ucv[col] -= 1
            urv[row] -= 1
            possible |= self.find(ucp, ucv, urp, urv)
            ucv[col] += 1
            urv[row] += 1
            # replace tile at index with 1, 2, 3
            for points in [1, 2, 3]:
                self[index] = points
                # update unknowns, find, revert updates
                ucp[col] -= points
                urp[row] -= points
                possible |= self.find(ucp, ucv, urp, urv)
                ucp[col] += points
                urp[row] += points
            # revert tile to None for other recursive calls
            self[index] = None
            return possible
        # if there are no undetermined tiles, unknown points, unknown voltorbs left, self is valid
        elif all(x == 0 for x in ucp + ucv + urp + urv):
            return set([Grid(self.width, self.height, self)])
        # if all tiles are determined but there are leftover points/voltorbs, self is not valid
        else:
            return set()

    def __str__(self):
        out = ""
        for row in range(self.height):
            for col in range(self.width):
                if self[row, col] is None:
                    out += ' ? '
                else:
                    out += '[{:1}]'.format(self[row, col])
            out += ' {:02} {:2}\n'.format(self.row_points[row], self.row_voltorbs[row])
        for cp in self.col_points:
            out += '{:02} '.format(cp)
        out += '\n'
        for cv in self.col_voltorbs:
            out += '{:2} '.format(cv)
        out += '\n'
        return out


class FlipDistribution(Grid):
    def __init__(self, vf):
        super().__init__(vf.width, vf.height)
        sample_space = vf.find()
        self.samples = len(sample_space)
        for board in sample_space:
            for row in range(vf.height):
                for col in range(vf.width):
                    if self[row, col] is None:
                        self[row, col] = [0, 0, 0, 0]
                    self[row, col][board[row, col]] += 1

    def __str__(self):
        out = "Sample space size: {}\nDistribution:\n".format(self.samples)
        for row in range(self.height):
            for col in range(self.width):
                percentages = [outcomes / self.samples for outcomes in self[row, col]]
                out += '[0:{:.3f} 1:{:.3f} 2:{:.3f} 3:{:.3f}]'.format(*percentages)
            out += '\n'
        return out


if __name__ == '__main__':
    v = VoltorbFlip([(5, 1), (5, 1), (5, 1), (4, 2), (6, 1)],
                    [(5, 1), (3, 2), (5, 1), (4, 1), (8, 1)])
    print(v)
    print(FlipDistribution(v))
    v[4, 4] = 3
    print(v)
    print(FlipDistribution(v))
    v[0, 0] = 2
    print(v)
    print(FlipDistribution(v))
    v[4, 1] = 2
    print(v)
    print(FlipDistribution(v))
    v[2, 2] = 2
    print(v)
    print(FlipDistribution(v))
    v[4, 3] = 2
    print(v)
    print(FlipDistribution(v))

"""Output:

 ?  ?  ?  ?  ?  05  1
 ?  ?  ?  ?  ?  03  2
 ?  ?  ?  ?  ?  05  1
 ?  ?  ?  ?  ?  04  1
 ?  ?  ?  ?  ?  08  1
05 05 05 04 06 
 1  1  1  2  1 

Sample space size: 825
Distribution:
[0:0.159 1:0.642 2:0.199 3:0.000][0:0.159 1:0.642 2:0.199 3:0.000][0:0.159 1:0.642 2:0.199 3:0.000][0:0.335 1:0.422 2:0.244 3:0.000][0:0.189 1:0.651 2:0.160 3:0.000]
[0:0.335 1:0.665 2:0.000 3:0.000][0:0.335 1:0.665 2:0.000 3:0.000][0:0.335 1:0.665 2:0.000 3:0.000][0:0.589 1:0.411 2:0.000 3:0.000][0:0.407 1:0.593 2:0.000 3:0.000]
[0:0.159 1:0.642 2:0.199 3:0.000][0:0.159 1:0.642 2:0.199 3:0.000][0:0.159 1:0.642 2:0.199 3:0.000][0:0.335 1:0.422 2:0.244 3:0.000][0:0.189 1:0.651 2:0.160 3:0.000]
[0:0.152 1:0.848 2:0.000 3:0.000][0:0.152 1:0.848 2:0.000 3:0.000][0:0.152 1:0.848 2:0.000 3:0.000][0:0.364 1:0.636 2:0.000 3:0.000][0:0.182 1:0.818 2:0.000 3:0.000]
[0:0.196 1:0.201 2:0.602 3:0.000][0:0.196 1:0.201 2:0.602 3:0.000][0:0.196 1:0.201 2:0.602 3:0.000][0:0.378 1:0.109 2:0.513 3:0.000][0:0.033 1:0.000 2:0.255 3:0.713]

 ?  ?  ?  ?  ?  05  1
 ?  ?  ?  ?  ?  03  2
 ?  ?  ?  ?  ?  05  1
 ?  ?  ?  ?  ?  04  1
 ?  ?  ?  ? [3] 08  1
05 05 05 04 06 
 1  1  1  2  1 

Sample space size: 588
Distribution:
[0:0.153 1:0.605 2:0.241 3:0.000][0:0.153 1:0.605 2:0.241 3:0.000][0:0.153 1:0.605 2:0.241 3:0.000][0:0.321 1:0.403 2:0.276 3:0.000][0:0.219 1:0.781 2:0.000 3:0.000]
[0:0.340 1:0.660 2:0.000 3:0.000][0:0.340 1:0.660 2:0.000 3:0.000][0:0.340 1:0.660 2:0.000 3:0.000][0:0.592 1:0.408 2:0.000 3:0.000][0:0.388 1:0.612 2:0.000 3:0.000]
[0:0.153 1:0.605 2:0.241 3:0.000][0:0.153 1:0.605 2:0.241 3:0.000][0:0.153 1:0.605 2:0.241 3:0.000][0:0.321 1:0.403 2:0.276 3:0.000][0:0.219 1:0.781 2:0.000 3:0.000]
[0:0.153 1:0.847 2:0.000 3:0.000][0:0.153 1:0.847 2:0.000 3:0.000][0:0.153 1:0.847 2:0.000 3:0.000][0:0.367 1:0.633 2:0.000 3:0.000][0:0.173 1:0.827 2:0.000 3:0.000]
[0:0.201 1:0.282 2:0.517 3:0.000][0:0.201 1:0.282 2:0.517 3:0.000][0:0.201 1:0.282 2:0.517 3:0.000][0:0.398 1:0.153 2:0.449 3:0.000][0:0.000 1:0.000 2:0.000 3:1.000]

[2] ?  ?  ?  ?  05  1
 ?  ?  ?  ?  ?  03  2
 ?  ?  ?  ?  ?  05  1
 ?  ?  ?  ?  ?  04  1
 ?  ?  ?  ? [3] 08  1
05 05 05 04 06 
 1  1  1  2  1 

Sample space size: 142
Distribution:
[0:0.000 1:0.000 2:1.000 3:0.000][0:0.176 1:0.824 2:0.000 3:0.000][0:0.176 1:0.824 2:0.000 3:0.000][0:0.444 1:0.556 2:0.000 3:0.000][0:0.204 1:0.796 2:0.000 3:0.000]
[0:0.296 1:0.704 2:0.000 3:0.000][0:0.352 1:0.648 2:0.000 3:0.000][0:0.352 1:0.648 2:0.000 3:0.000][0:0.606 1:0.394 2:0.000 3:0.000][0:0.394 1:0.606 2:0.000 3:0.000]
[0:0.155 1:0.845 2:0.000 3:0.000][0:0.162 1:0.528 2:0.310 3:0.000][0:0.162 1:0.528 2:0.310 3:0.000][0:0.296 1:0.324 2:0.380 3:0.000][0:0.225 1:0.775 2:0.000 3:0.000]
[0:0.134 1:0.866 2:0.000 3:0.000][0:0.155 1:0.845 2:0.000 3:0.000][0:0.155 1:0.845 2:0.000 3:0.000][0:0.380 1:0.620 2:0.000 3:0.000][0:0.176 1:0.824 2:0.000 3:0.000]
[0:0.415 1:0.585 2:0.000 3:0.000][0:0.155 1:0.155 2:0.690 3:0.000][0:0.155 1:0.155 2:0.690 3:0.000][0:0.275 1:0.106 2:0.620 3:0.000][0:0.000 1:0.000 2:0.000 3:1.000]

[2] ?  ?  ?  ?  05  1
 ?  ?  ?  ?  ?  03  2
 ?  ?  ?  ?  ?  05  1
 ?  ?  ?  ?  ?  04  1
 ? [2] ?  ? [3] 08  1
05 05 05 04 06 
 1  1  1  2  1 

Sample space size: 98
Distribution:
[0:0.000 1:0.000 2:1.000 3:0.000][0:0.204 1:0.796 2:0.000 3:0.000][0:0.163 1:0.837 2:0.000 3:0.000][0:0.429 1:0.571 2:0.000 3:0.000][0:0.204 1:0.796 2:0.000 3:0.000]
[0:0.306 1:0.694 2:0.000 3:0.000][0:0.388 1:0.612 2:0.000 3:0.000][0:0.327 1:0.673 2:0.000 3:0.000][0:0.592 1:0.408 2:0.000 3:0.000][0:0.388 1:0.612 2:0.000 3:0.000]
[0:0.173 1:0.827 2:0.000 3:0.000][0:0.235 1:0.765 2:0.000 3:0.000][0:0.143 1:0.408 2:0.449 3:0.000][0:0.214 1:0.235 2:0.551 3:0.000][0:0.235 1:0.765 2:0.000 3:0.000]
[0:0.143 1:0.857 2:0.000 3:0.000][0:0.173 1:0.827 2:0.000 3:0.000][0:0.143 1:0.857 2:0.000 3:0.000][0:0.367 1:0.633 2:0.000 3:0.000][0:0.173 1:0.827 2:0.000 3:0.000]
[0:0.378 1:0.622 2:0.000 3:0.000][0:0.000 1:0.000 2:1.000 3:0.000][0:0.224 1:0.224 2:0.551 3:0.000][0:0.398 1:0.153 2:0.449 3:0.000][0:0.000 1:0.000 2:0.000 3:1.000]

[2] ?  ?  ?  ?  05  1
 ?  ?  ?  ?  ?  03  2
 ?  ? [2] ?  ?  05  1
 ?  ?  ?  ?  ?  04  1
 ? [2] ?  ? [3] 08  1
05 05 05 04 06 
 1  1  1  2  1 

Sample space size: 44
Distribution:
[0:0.000 1:0.000 2:1.000 3:0.000][0:0.205 1:0.795 2:0.000 3:0.000][0:0.114 1:0.886 2:0.000 3:0.000][0:0.477 1:0.523 2:0.000 3:0.000][0:0.205 1:0.795 2:0.000 3:0.000]
[0:0.273 1:0.727 2:0.000 3:0.000][0:0.409 1:0.591 2:0.000 3:0.000][0:0.273 1:0.727 2:0.000 3:0.000][0:0.636 1:0.364 2:0.000 3:0.000][0:0.409 1:0.591 2:0.000 3:0.000]
[0:0.114 1:0.886 2:0.000 3:0.000][0:0.205 1:0.795 2:0.000 3:0.000][0:0.000 1:0.000 2:1.000 3:0.000][0:0.477 1:0.523 2:0.000 3:0.000][0:0.205 1:0.795 2:0.000 3:0.000]
[0:0.114 1:0.886 2:0.000 3:0.000][0:0.182 1:0.818 2:0.000 3:0.000][0:0.114 1:0.886 2:0.000 3:0.000][0:0.409 1:0.591 2:0.000 3:0.000][0:0.182 1:0.818 2:0.000 3:0.000]
[0:0.500 1:0.500 2:0.000 3:0.000][0:0.000 1:0.000 2:1.000 3:0.000][0:0.500 1:0.500 2:0.000 3:0.000][0:0.000 1:0.000 2:1.000 3:0.000][0:0.000 1:0.000 2:0.000 3:1.000]

[2] ?  ?  ?  ?  05  1
 ?  ?  ?  ?  ?  03  2
 ?  ? [2] ?  ?  05  1
 ?  ?  ?  ?  ?  04  1
 ? [2] ? [2][3] 08  1
05 05 05 04 06 
 1  1  1  2  1 

Sample space size: 44
Distribution:
[0:0.000 1:0.000 2:1.000 3:0.000][0:0.205 1:0.795 2:0.000 3:0.000][0:0.114 1:0.886 2:0.000 3:0.000][0:0.477 1:0.523 2:0.000 3:0.000][0:0.205 1:0.795 2:0.000 3:0.000]
[0:0.273 1:0.727 2:0.000 3:0.000][0:0.409 1:0.591 2:0.000 3:0.000][0:0.273 1:0.727 2:0.000 3:0.000][0:0.636 1:0.364 2:0.000 3:0.000][0:0.409 1:0.591 2:0.000 3:0.000]
[0:0.114 1:0.886 2:0.000 3:0.000][0:0.205 1:0.795 2:0.000 3:0.000][0:0.000 1:0.000 2:1.000 3:0.000][0:0.477 1:0.523 2:0.000 3:0.000][0:0.205 1:0.795 2:0.000 3:0.000]
[0:0.114 1:0.886 2:0.000 3:0.000][0:0.182 1:0.818 2:0.000 3:0.000][0:0.114 1:0.886 2:0.000 3:0.000][0:0.409 1:0.591 2:0.000 3:0.000][0:0.182 1:0.818 2:0.000 3:0.000]
[0:0.500 1:0.500 2:0.000 3:0.000][0:0.000 1:0.000 2:1.000 3:0.000][0:0.500 1:0.500 2:0.000 3:0.000][0:0.000 1:0.000 2:1.000 3:0.000][0:0.000 1:0.000 2:0.000 3:1.000]

[Finished in 7.4s]
"""