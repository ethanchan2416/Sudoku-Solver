import itertools
import time

# Define unit: 9 values. Each row, column or block of the 9x9 matrix is a unit.
# Define slice: 3 values. Each row or column in a block is a slice.
# Define Testset in fcn input argument: Any 9x9 row, column or block matrix.
# Define BlkMatrix in fcn input argument: Any 9x9 block matrix, usually TestMatrix.

# Using RowMatrix indexing permutations from row1 top to bottom, Blk test on rows 3, 6, 9:
#   Answer at position [34, 29, 40, 1, 41, 0, 38, 3, 21]
#   Best Runtime out of 100: 1.412269 sec.

# Using RowMatrix indexing permutations from row1 top to bottom, Blk test on rows 2, 3, 5, 6, 8, 9:
#   Best Runtime out of 100: 0.480465 sec.


# -------------------- Driver Function for sudoku.py --------------------


# Driver function for sudoku.py
# 2 input arguments needed: Testset (matrix you wanna solve), Type ('row' or 'column')
# Return: Answer (solved matrix), run_time (program runtime)
def solve_sudoku(Testset, Type):
    if Type == 'row':
        RowMatrix = Testset
        BlkMatrix = row_to_blk(Testset)
    elif Type == 'blk':
        RowMatrix = blk_to_row(Testset)
        BlkMatrix = Testset
    # start timer
    start_time = time.clock()
    # algorithm starts here
    PVPerMatrix = possible_vals_of_each_blank(BlkMatrix)
    PermuOfMatrix = possible_permutations_of_matrix(PVPerMatrix)
    IPermuOfMatrix = integrate_permu_into_testset_matrix(PermuOfMatrix, RowMatrix)
    Answer = find_solution_from_permus(IPermuOfMatrix)
    # stop timer
    run_time = round(time.clock() - start_time, ndigits=6)
    # format output
    print_answer(Answer)
    print(f'Is sudoku solved? {sudoku_is_solved(row_to_blk(Answer))}')
    print(f'runtime = {run_time} seconds\n')

    return Answer, run_time

# -------------------- functs to re-organize sudoku order --------------------


# Converts BlkMatrix to RowMatrix
def blk_to_row(BlkMatrix):
    RowMatrix = []
    slice_start = 0

    for sets in range(3):  # run through how many sets --> finish three sets
        for row in range(3):  # inter-row index --> finish a set (three rows)
            RowVector = []
            for idx_slice in range(3):  # inner-row index --> finish a row
                which_block = 3 * row + idx_slice
                Slice = BlkMatrix[which_block][slice_start:slice_start + 3]
                RowVector.append(Slice)
            RowVector = tuple(itertools.chain(*RowVector))  # flattens array
            RowMatrix.append(RowVector)
        slice_start += 3

    RowMatrix = sort_array_order(RowMatrix)

    return RowMatrix


# Converts BlkMatrix to ColMatrix
def blk_to_col(BlkMatrix):
    ColMatrix = []

    for sets in range(3):  # run through how many sets --> finish three sets
        # first run: 0 3 6, then run 1 4 7, then run 2,5,8
        slice_index = [0, 3, 6] if sets is 0 else [1, 4, 7] if sets is 1 else [2, 5, 8]
        for i in range(3):  # inter-column index --> finish a set (three columns)
            ColVector = []
            for j in range(3):  # inner-column index --> finish a column
                which_block = 3 * j + i
                Slice = []
                Slice.append(BlkMatrix[which_block][slice_index[0]])
                Slice.append(BlkMatrix[which_block][slice_index[1]])
                Slice.append(BlkMatrix[which_block][slice_index[2]])
                ColVector.append(Slice)
            ColVector = tuple(itertools.chain(*ColVector))  # flattens array
            ColMatrix.append(ColVector)

    ColMatrix = sort_array_order(ColMatrix)

    return ColMatrix


# Converts RowMatrix to BlkMatrix
def row_to_blk(RowMatrix):
    BlkMatrix = []
    for sets in range(3):
        slice_start = sets * 3
        for i in range(3):
            BlkVector = []
            for j in range(3):
                which_row = i * 3 + j
                Slice = RowMatrix[which_row][slice_start:slice_start + 3]
                BlkVector.append(Slice)
            BlkVector = tuple(itertools.chain(*BlkVector))
            BlkMatrix.append(BlkVector)

    BlkMatrix = sort_array_order(BlkMatrix)

    return BlkMatrix


# Rearranges array orders from [0, 3, 6, 1, 4, 7, 2, 5, 8] to [1, 2, 3, 4, 5, 6, 7, 8, 9]
def sort_array_order(Testset):
    CurrentOrder = (0, 3, 6, 1, 4, 7, 2, 5, 8)
    SortedMatrix = []

    for i in CurrentOrder:
        SortedMatrix.append(Testset[i])

    return tuple(SortedMatrix)


# -------------------- functs to determine if sudoku is solved --------------------
# Define All Solved: if row, column and block contains zero of each num from 1-9
# All Solved = Row Solved + Column Solved + Block Solved


# Return: True if sudoku is solved, False if unsolved
def sudoku_is_solved(BlkMatrix):
    RowMatrix = blk_to_row(BlkMatrix)
    ColMatrix = blk_to_col(BlkMatrix)

    def solved_condition(Testset):
        SolvednSorted = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for i in range(9):
            if set(Testset[i]) != SolvednSorted:
                return False
        return True

    if solved_condition(RowMatrix) is False:  # Row Solved?
        return False
    elif solved_condition(BlkMatrix) is False:  # Block Solved?
        return False
    elif solved_condition(ColMatrix) is False:  # Column Solved?
        return False
    else:  # All Solved
        return True


# -------------------- functs to solve sudoku --------------------


# Return: BlanksIdInMatrix (positions per blank), BlanksValInMatrix (possible values per blank acquired from set(1~9) - set(Testset[i]) )
def find_blanks(Testset):
    BlanksIdInMatrix = []
    BlanksValInMatrix = []
    SolvednSorted = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    for i in range(9):
        IdxPerUnit = (idx for idx, val in enumerate(Testset[i]) if val == 0)
        ValPerUnit = tuple(SolvednSorted - set(Testset[i]))
        BlanksIdInMatrix.append(IdxPerUnit)
        BlanksValInMatrix.append(ValPerUnit)

    return tuple(BlanksIdInMatrix), tuple(BlanksValInMatrix)


# Return: block_index(0~8)
def which_block(row, col):
    if row in {0, 1, 2}:
        big_row = 0
    elif row in {3, 4, 5}:
        big_row = 1
    else:
        big_row = 2
    if col in {0, 1, 2}:
        big_col = 0
    elif col in {3, 4, 5}:
        big_col = 1
    else:
        big_col = 2
    block_index = big_row * 3 + big_col

    return block_index


# Return: PVPerMatrix(contains initial possible values per blank that doesn't collide with row, col, blk)
def possible_vals_of_each_blank(BlkMatrix):
    RowMatrix = blk_to_row(BlkMatrix)
    RowBlanksId = find_blanks(RowMatrix)[0]
    ColBlanksVal = find_blanks(blk_to_col(BlkMatrix))[1]

    PVPerMatrix = []
    for row in range(9):
        PVPerRow = []
        for col in RowBlanksId[row]:
            PossibleValsInItsCol = set(ColBlanksVal[col])
            PossibleValsInItsRow = set(RowMatrix[row])
            PossibleValsInItsBlk = set(BlkMatrix[which_block(row, col)])
            PVPerBlank = tuple(PossibleValsInItsCol - PossibleValsInItsRow - PossibleValsInItsBlk)
            # print(PVPerBlank)
            PVPerRow.append(PVPerBlank)
        PVPerMatrix.append(tuple(PVPerRow))

    return tuple(PVPerMatrix)


# Just some coding trick
def loop_calibrator(PVPerMatrix, row):
    PermuOrderOfBlank = []
    zero = (0,)
    num_of_elements = len(PVPerMatrix[row])

    for i in range(9):
        if i < 9 - num_of_elements:
            PermuOrderOfBlank.append(zero)
        else:
            PermuOrderOfBlank.append(PVPerMatrix[row][num_of_elements + i - 9])

    return tuple(PermuOrderOfBlank)


# Yield: Permu (each possible permutation per row without inital given values inserted)
# Child function of possible_permutations_of_matrix()
def per_possible_permutation_per_row(PVPerMatrix, row):
    PermuOrderOfBlank = loop_calibrator(PVPerMatrix, row)
    Permu = []
    for c1 in PermuOrderOfBlank[0]:
        if c1 != 0:
            Permu.append(c1)
        for c2 in PermuOrderOfBlank[1]:
            if c2 != 0:
                if c2 not in Permu:
                    Permu.append(c2)
                else:
                    continue
            for c3 in PermuOrderOfBlank[2]:
                if c3 != 0:
                    if c3 not in Permu:
                        Permu.append(c3)
                    else:
                        continue
                for c4 in PermuOrderOfBlank[3]:
                    if c4 != 0:
                        if c4 not in Permu:
                            Permu.append(c4)
                        else:
                            continue
                    for c5 in PermuOrderOfBlank[4]:
                        if c5 != 0:
                            if c5 not in Permu:
                                Permu.append(c5)
                            else:
                                continue
                        for c6 in PermuOrderOfBlank[5]:
                            if c6 != 0:
                                if c6 not in Permu:
                                    Permu.append(c6)
                                else:
                                    continue
                            for c7 in PermuOrderOfBlank[6]:
                                if c7 != 0:
                                    if c7 not in Permu:
                                        Permu.append(c7)
                                    else:
                                        continue
                                for c8 in PermuOrderOfBlank[7]:
                                    if c8 != 0:
                                        if c8 not in Permu:
                                            Permu.append(c8)
                                        else:
                                            continue
                                    for c9 in PermuOrderOfBlank[8]:
                                        if c9 != 0:
                                            if c9 not in Permu:
                                                Permu.append(c9)
                                            else:
                                                continue

                                        yield tuple(Permu)

                                        if len(Permu) != 0:
                                            Permu.pop()
                                    if len(Permu) != 0:
                                        Permu.pop()
                                if len(Permu) != 0:
                                    Permu.pop()
                            if len(Permu) != 0:
                                Permu.pop()
                        if len(Permu) != 0:
                            Permu.pop()
                    if len(Permu) != 0:
                        Permu.pop()
                if len(Permu) != 0:
                    Permu.pop()
            if len(Permu) != 0:
                Permu.pop()
        if len(Permu) != 0:
            Permu.pop()


# Return: PermuOfMatrix (Permu --> PermuPerRow --> PermuOfMatrix)
# Father function of per_possible_permutation_per_row()
def possible_permutations_of_matrix(PVPerMatrix):
    PermuOfMatrix = []

    for row in range(9):
        PermuPerRow = []
        for Permu in per_possible_permutation_per_row(PVPerMatrix, row):
            PermuPerRow.append(Permu)
        PermuPerRow = tuple(PermuPerRow)
        PermuOfMatrix.append(PermuPerRow)

    return tuple(PermuOfMatrix)


# Return: IntegratedRow (each possible permutation per row with inital given values integrated)
# Child function of integrate_permu_into_testset_matrix()
def per_integrated_permu_per_row(Permu, RowVector, row):
    IntegratedRow = list(RowVector).copy()
    PermuOperator = list(Permu).copy()
    for idx, val in reversed(tuple(enumerate(IntegratedRow))):
        if val == 0:
            IntegratedRow[idx] = PermuOperator.pop()

    return tuple(IntegratedRow)


# Return: IPermuOfMatrix (IntegratedRow --> IPermuPerRow --> IPermuOfMatrix)
# Father function of per_integrated_permu_per_row()
def integrate_permu_into_testset_matrix(PermuOfMatrix, RowMatrix):
    IPermuOfMatrix = []

    for row in range(9):
        RowVector = RowMatrix[row]
        IPermuPerRow = []
        for Permu in PermuOfMatrix[row]:
            IntegratedRow = per_integrated_permu_per_row(Permu, RowVector, row)
            IPermuPerRow.append(IntegratedRow)
        IPermuPerRow = tuple(IPermuPerRow)
        IPermuOfMatrix.append(IPermuPerRow)

    return tuple(IPermuOfMatrix)


# Return: True if cols in PassedSolution in find_solution_from_permus() so far are valid, else False
def cols_are_valid(PassedSolution):
    height = len(PassedSolution)  # height of passed testset at the moment

    def col_per_idx_is_valid():
        PassedPerColIdx = set()
        for row in range(height):
            val = PassedSolution[row][col]
            if val not in PassedPerColIdx:
                PassedPerColIdx.add(val)
            else:
                return False

    for col in range(9):
        if col_per_idx_is_valid() is False:
            return False
    return True


# Return: True if blks in PassedSolution in find_solution_from_permus() so far are valid, else False
def blks_are_valid(PassedSolution):
    PassedSolution_height = len(PassedSolution)
    if PassedSolution_height is 2 or 5 or 8:
        untested_rows = 2
        starting_row = PassedSolution_height - untested_rows  # height - 2 = start from last set of blks
    else:
        untested_rows = 3
        starting_row = PassedSolution_height - untested_rows  # height - 3 = start from last set of blks

    def per_blk_is_valid():
        PassedPerBlk = set()
        for row in range(untested_rows):
            RowSlice = PassedSolution[starting_row + row][big_col * 3: big_col * 3 + 3]
            # print(RowSlice)
            if PassedPerBlk.isdisjoint(RowSlice):
                PassedPerBlk = PassedPerBlk.union(RowSlice)
                # print(PassedPerBlk)
            else:
                return False

    for big_col in range(3):
        # print(big_col)
        if per_blk_is_valid() is False:
            return False
    return True


# Return: PassedSolution (Answer of sudoku)
def find_solution_from_permus(IPermuOfMatrix):
    PassedSolution = []

    for p1 in IPermuOfMatrix[0]:
        PassedSolution.append(p1)

        for p2 in IPermuOfMatrix[1]:
            PassedSolution.append(p2)
            if cols_are_valid(PassedSolution) is False or blks_are_valid(PassedSolution) is False:
                PassedSolution.pop()
                continue

            for p3 in IPermuOfMatrix[2]:
                PassedSolution.append(p3)
                if cols_are_valid(PassedSolution) is False or blks_are_valid(PassedSolution) is False:
                    PassedSolution.pop()
                    continue

                for p4 in IPermuOfMatrix[3]:
                    PassedSolution.append(p4)
                    if cols_are_valid(PassedSolution) is False:
                        PassedSolution.pop()
                        continue

                    for p5 in IPermuOfMatrix[4]:
                        PassedSolution.append(p5)
                        if cols_are_valid(PassedSolution) is False or blks_are_valid(PassedSolution) is False:
                            PassedSolution.pop()
                            continue

                        for p6 in IPermuOfMatrix[5]:
                            PassedSolution.append(p6)
                            if cols_are_valid(PassedSolution) is False or blks_are_valid(PassedSolution) is False:
                                PassedSolution.pop()
                                continue

                            for p7 in IPermuOfMatrix[6]:
                                PassedSolution.append(p7)
                                if cols_are_valid(PassedSolution) is False:
                                    PassedSolution.pop()
                                    continue

                                for p8 in IPermuOfMatrix[7]:
                                    PassedSolution.append(p8)
                                    if cols_are_valid(PassedSolution) is False or blks_are_valid(PassedSolution) is False:
                                        PassedSolution.pop()
                                        continue

                                    for p9 in IPermuOfMatrix[8]:
                                        PassedSolution.append(p9)
                                        if cols_are_valid(PassedSolution) is False or blks_are_valid(PassedSolution) is False:
                                            PassedSolution.pop()
                                            continue
                                        else:
                                            # print(PassedSolution)
                                            return tuple(PassedSolution)

                                            PassedSolution.pop()
                                    PassedSolution.pop()
                                PassedSolution.pop()
                            PassedSolution.pop()
                        PassedSolution.pop()
                    PassedSolution.pop()
                PassedSolution.pop()
            PassedSolution.pop()
        PassedSolution.pop()


# -------------------- fuction for input testset --------------------


def input_testset():
    print('<<Step 1>> Enter indices in 1st row from left to right')
    print('           Use SPACE to seperate')
    print('           Enter 0 for a blank indice')
    print('           eg. "0 8 0 0 5 0 2 0 0"\n')
    print('<<Step 2>> Repeat 1. from top to bottom\n')

    testset = []
    for i in range(9):
        row = input(f'Input row {i+1}: ')
        row = row.split()
        testset_row = []
        for idx, val in enumerate(row):
            val = eval(val)
            testset_row.append(val)
        testset.append(tuple(testset_row))

    print()
    return tuple(testset)


# -------------------- fuction for output formatting --------------------


def print_answer(PassedSolution):
    print('-------------------------')
    for i in range(9):
        for j in range(9):
            if j is 0:
                print('| ', end='')
            print(PassedSolution[i][j], sep='', end=' ')
            if j is 2 or j is 5:
                print('| ', end='')
            if j is 8:
                print('|\n', end='')
        if i is 2 or i is 5:
            print('-------------------------')
    print('-------------------------')


# -------------------------
# | 7 8 6 | 1 5 9 | 2 4 3 |
# | 2 4 5 | 7 8 3 | 6 9 1 |
# | 1 3 9 | 4 6 2 | 7 8 5 |
# -------------------------
# | 8 7 2 | 3 9 6 | 1 5 4 |
# | 6 1 4 | 8 7 5 | 3 2 9 |
# | 5 9 3 | 2 1 4 | 8 7 6 |
# -------------------------
# | 4 6 8 | 5 3 7 | 9 1 2 |
# | 9 2 1 | 6 4 8 | 5 3 7 |
# | 3 5 7 | 9 2 1 | 4 6 8 |
# -------------------------
