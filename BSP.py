from math import sqrt
from random import *

class Room:
    def __init__(self, r, c, h, w):
        self.row = r
        self.col = c
        self.height = h
        self.width = w

class Generator:
    def __init__(self, width, height):
        self.boundary = 16
        self.width = width
        self.height = height
        self.branches = []
        self.dungeon = []
        self.rooms = []

        for h in range(self.height):
            row = []
            for w in range(self.width):
                y = randint(0, 7)
                if(y == 0):
                    row.append(7)

                elif(y == 1):
                    row.append(2)

                elif(y == 2):
                    row.append(4)

                else:
                    row.append(1)

            self.dungeon.append(row)

    def printmap(self):#For testing
        out = []
        for r in range(self.height):
            row = ""
            for c in range(self.width):
                row += str(self.dungeon[r][c])
            print(row)

    def shorizontal(self, minrow, mincol, maxrow, maxcol):
        split = (minrow + maxrow) // 2 + choice((-2, -1, 0, 1, 2))
        self.rsplit(minrow, mincol, split, maxcol)
        self.rsplit(split + 1, mincol, maxrow, maxcol)

    def svertical(self, minrow, mincol, maxrow, maxcol):
        split = (mincol + maxcol) // 2 + choice((-2, -1, 0, 1, 2))
        self.rsplit(minrow, mincol, maxrow, split)
        self.rsplit(minrow, split + 1, maxrow, maxcol)

    def rsplit(self, minrow, mincol, maxrow, maxcol):
        segheight = maxrow - minrow
        segwidth = maxcol - mincol

        if(segheight < self.boundary and segwidth < self.boundary):
            self.branches.append((minrow, mincol, maxrow, maxcol))
        elif(segheight < self.boundary and segwidth >= self.boundary):
            self.svertical(minrow, mincol, maxrow, maxcol)
        elif(segheight >= self.boundary and segwidth < self.boundary):
            self.shorizontal(minrow, mincol, maxrow, maxcol)
        else:
                if(random() < 0.5):
                    self.shorizontal(minrow, mincol, maxrow, maxcol)
                else:
                    self.svertical(minrow, mincol, maxrow, maxcol)

    def adjcheck(self, room1, room2):
        adjrows = []
        adjcols = []
        for r in range(room1.row, room1.row + room1.height):
            if(r >= room2.row and r < room2.row + room2.height):
                adjrows.append(r)

        for c in range(room1.col, room1.col + room1.width):
            if(c >= room2.col and c < room2.col + room2.width):
                adjcols.append(c)

        return (adjrows, adjcols)

    def distancecheck(self, room1, room2):
        centre1 = (room1.row + room1.height // 2, room1.col + room1.width // 2)
        centre2 = (room2.row + room2.height // 2, room2.col + room2.width // 2)

        return sqrt((centre1[0] - centre2[0]) ** 2 + (centre1[1] - centre2[1]) ** 2)

    def findclosestgroup(self, groups, rdictionary):
        shortdis = 99999
        start = None
        sgroup = None
        nearest = None

        for group in groups:
            for room in group:
                key = (room.row, room.col)
                for other in rdictionary[key]:
                    if(not other[0] in group and other[3] < shortdis):
                        shortdis = other[3]
                        start = room
                        nearest = other
                        sgroup = group

        self.mcorridor(start, nearest)

        ogroup = None
        for group in groups:
            if(nearest[0] in group):
                ogroup = group
                break

        sgroup += ogroup
        groups.remove(ogroup)

    def crooms(self):
        groups = []
        rdictionary = {}
        for room in self.rooms:
            key = (room.row, room.col)
            rdictionary[key] = []
            for other in self.rooms:
                okey = (other.row, other.col)
                if(key == okey): continue
                adj = self.adjcheck(room, other)
                if(len(adj[0]) > 0):
                    rdictionary[key].append((other, adj[0], 'rows', self.distancecheck(room, other)))
                elif(len(adj[1]) > 0):
                    rdictionary[key].append((other, adj[1], 'cols', self.distancecheck(room, other)))

            groups.append([room])

        while(len(groups) > 1):
            self.findclosestgroup(groups, rdictionary)

    def mcorridor(self, room1, room2):
        if(room2[2] == 'rows'):
            row = choice(room2[1])
            if(room1.col + room1.width < room2[0].col):
                start_col = room1.col + room1.width
                endcol = room2[0].col
            else:
                start_col = room2[0].col + room2[0].width
                endcol = room1.col
            for c in range(start_col, endcol):
                self.dungeon[row][c] = 0
                self.dungeon[row + 1][c] = 0

            if(endcol - start_col >= 4):
                self.dungeon[row][start_col] = 0
                self.dungeon[row][endcol - 1] = 0
            elif start_col == endcol - 1:
                self.dungeon[row][start_col] = 0
        else:
            col = choice(room2[1])
            if(room1.row + room1.height < room2[0].row):
                start_row = room1.row + room1.height
                endrow = room2[0].row
            else:
                start_row = room2[0].row + room2[0].height
                endrow = room1.row

            for r in range(start_row, endrow):
                self.dungeon[r][col] = 0
                self.dungeon[r][col + 1] = 0

            if(endrow - start_row >= 4):
                self.dungeon[start_row][col] = 0
                self.dungeon[endrow - 1][col] = 0
            elif start_row == endrow - 1:
                self.dungeon[start_row][col] = 0

    def mrooms(self):
        for branch in self.branches:
            if(random() > 0.80): continue
            sectionwidth = branch[3] - branch[1]
            sectionheight = branch[2] - branch[0]

            rwidth = round(randrange(60, 100) / 100 * sectionwidth)
            rheight = round(randrange(60, 100) / 100 * sectionheight)

            if(sectionheight > rheight):
                rstartrow = branch[0] + randrange(sectionheight - rheight)
            else:
                rstartrow = branch[0]

            if(sectionwidth > rwidth):
                rstartcol = branch[1] + randrange(sectionwidth - rwidth)
            else:
                rstartcol = branch[1]

            self.rooms.append(Room(rstartrow, rstartcol, rheight, rwidth))
            for r in range(rstartrow, rstartrow + rheight):
                for c in range(rstartcol, rstartcol + rwidth):
##                    x = randint(0, 25)
##                    if(x == 0):
##                        self.dungeon[r][c] = 6
##                    else:
##                        self.dungeon[r][c] = 0
                    self.dungeon[r][c] = 0

    def postGen(self):
        for y in range(len(self.dungeon)):
            for x in range(len(self.dungeon[0])):
                if(x + 1 < len(self.dungeon[0]) and y + 1 < len(self.dungeon)):
                    if(self.dungeon[y - 1][x - 1] != 0 and self.dungeon[y - 1][x] != 0 and self.dungeon[y - 1][x + 1] != 0 and self.dungeon[y][x - 1] != 0 and self.dungeon[y][x + 1] != 0 and self.dungeon[y + 1][x - 1] != 0 and self.dungeon[y + 1][x] != 0 and self.dungeon[y + 1][x + 1] != 0):
                        self.dungeon[y][x] = 21

                elif(x + 1 < len(self.dungeon[0]) and y + 1 >= len(self.dungeon)):
                    if(self.dungeon[y - 1][x - 1] != 0 and self.dungeon[y - 1][x] != 0 and self.dungeon[y - 1][x + 1] != 0 and self.dungeon[y][x - 1] != 0 and self.dungeon[y][x + 1] != 0):
                        self.dungeon[y][x] = 21

                elif(x + 1 >= len(self.dungeon[0]) and y + 1 < len(self.dungeon)):
                    if(self.dungeon[y - 1][x - 1] != 0 and self.dungeon[y - 1][x] != 0 and self.dungeon[y][x - 1] != 0 and self.dungeon[y + 1][x - 1] != 0 and self.dungeon[y + 1][x] != 0):
                        self.dungeon[y][x] = 21

                else:
                    if(self.dungeon[y - 1][x - 1] != 0 and self.dungeon[y - 1][x] != 0 and self.dungeon[y][x - 1] != 0):
                        self.dungeon[y][x] = 21

    def generatemap(self):
        self.rsplit(1, 1, self.height - 1, self.width - 1)
        self.mrooms()
        self.crooms()
        self.postGen()

    def returnmap(self):
        out = []
        for r in range(self.height):
            row = []
            for c in range(self.width):
                row.append(self.dungeon[r][c])
            out.append(row)

        return out
