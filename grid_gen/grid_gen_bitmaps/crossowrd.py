import os
class Variable():

    ACROSS = "across"
    DOWN = "down"

    def __init__(self, i, j, direction, length,is_first=False):
        """Create a new variable with starting point, direction, and length."""
        self.i = i
        self.j = j
        self.direction = direction
        self.length = length
        self.cells = []
        self.constraints=[]
        self.is_first=is_first # as for larger grids the minimum allowed word score is 8 thus need to reduce their domain.
        for k in range(self.length):
            ni=self.i + (k if self.direction == Variable.DOWN else 0)
            nj=self.j + (k if self.direction == Variable.ACROSS else 0)

            self.cells.append(
                (ni,nj)
            )

    def __hash__(self):
        return hash((self.i, self.j, self.direction, self.length))

    def __eq__(self, other):
        return (
            (self.i == other.i) and
            (self.j == other.j) and
            (self.direction == other.direction) and
            (self.length == other.length)
        )

    def __str__(self):
        return f"({self.i}, {self.j}) {self.direction} : {self.length} : {self.is_first}"

    def __repr__(self):
        direction = repr(self.direction)
        return f"Variable({self.i}, {self.j}, {direction}, {self.length})"
    
def print_grid(grid):
    n=len(grid)
    m=max(len(line) for line in grid)
    for i in range(0,n):
        for j in range(0,m):
            print(grid[i][j],end=' ')
        print()
    print("\n\n")
    

class Crossword():

    def __init__(self,format):
        # grid_file_folder="../assets/Output_no_tw/"
        # files=os.listdir(grid_file_folder)
        # structure_file=os.path.join(grid_file_folder, files[0])
        structure_file=format

        with open(structure_file) as f:
            raw_contents = f.read().splitlines()
            contents=[] 
            for line in raw_contents:
                sanitized_line=""
                for char in line:
                    if(ord(char) == 65279):
                        continue
                    sanitized_line+=char
                contents.append(sanitized_line)
            self.height = len(contents)
            self.width = min(len(line) for line in contents)    
            print(self.height,self.width)
            self.grid = []
            for i in range(self.height):
                row = []
                for j in range(self.width): 
                    if(ord(contents[i][j]) == 65279):
                        continue
                    if contents[i][j] != '.':
                        row.append('_')
                    else:
                        row.append(contents[i][j])
                self.grid.append(row)

        # Save vocabulary list
        print_grid(self.grid)
        # with open(words_file) as f:
        #     self.words = set(f.read().upper().splitlines())

        # Determine variable set
        self.variables = set()
        cnt=0
        for i in range(self.height):
            for j in range(self.width):

                # Vertical words
                starts_word = (
                    self.grid[i][j]!='.'
                    and (i == 0 or self.grid[i - 1][j]=='.')
                )
                if starts_word:
                    word=""
                    length = 0
                    for k in range(i , self.height):
                        if self.grid[k][j]!='.':
                            word+=self.grid[k][j]
                            length+=1
                        else:
                            break
                    if length > 1 and '_' in word:
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.DOWN,
                            length=length
                        ))

                # Horizontal words
                starts_word = (
                    self.grid[i][j]!='.'
                    and (j == 0 or self.grid[i][j - 1]=='.')
                )
                if starts_word:
                    length = 0
                    word=""
                    for k in range(j, self.width):
                        if self.grid[i][k]!='.':
                            word+=self.grid[i][k]
                            length += 1
                        else:
                            break
                    if length > 1:
                        is_first=False
                        cnt+=1
                        if '_' in word:
                            if self.height>9 and cnt<8:
                                is_first=True
                            self.variables.add(Variable(
                                i=i, j=j,
                                direction=Variable.ACROSS,
                                length=length,
                                is_first=is_first
                            ))                        

        # Compute overlaps for each word
        # For any pair of variables v1, v2, their overlap is either:
        #    None, if the two variables do not overlap; or
        #    (i, j), where v1's ith character overlaps v2's jth character
        self.overlaps = dict()
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2:
                    continue
                cells1 = v1.cells
                cells2 = v2.cells
                intersection = set(cells1).intersection(cells2)
                if not intersection:
                    self.overlaps[v1, v2] = None
                else:

                    intersection = intersection.pop()
                    r,c=intersection
                   
                    if self.grid[r][c]!='_':
                        print(v1,v2)
                        print(r,c)
                        continue
                    self.overlaps[v1, v2] = (
                        cells1.index(intersection),
                        cells2.index(intersection)
                    )


    def neighbors(self, var):
        """Given a variable, return set of overlapping variables."""
        return set(
            v for v in self.variables
            if v != var and self.overlaps[v, var]
        )
