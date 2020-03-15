import itertools
import time
#import sudoku as sdk
#from sudoku import *

test_data = [
    [0, 8, 0, 0, 0, 0, 0, 3, 0], [0, 5, 0, 7, 0, 0, 0, 0, 2], [2, 0, 0, 0, 9, 0, 0, 0, 0],
    [0, 7, 2, 0, 0, 0, 5, 0, 3], [3, 0, 6, 0, 0, 5, 0, 1, 0], [1, 0, 0, 0, 2, 0, 8, 0, 0],
    [0, 0, 0, 9, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 8, 9, 2, 0], [0, 1, 0, 0, 0, 7, 4, 0, 0],
]

# 是否整理好的判別句
# mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# result = [2, 3, 4, 1, 5, 6, 9, 8, 7]
# if mylist == result:
#     print(True)
# else:
#     print(False)
# result.sort()
# print(result)

# range incrementing for arraying
# for i in range(2, 11, 2):
#     print(i)

# arraying argument
# mylist = mylist[:5]
# print(mylist[:5])
# print(mylist)

# test row arraying
# row_count = 0
# for a in range(3):
#     for i in range(3):
#         RowVector = []
#         for j in range(3):
#             block_index = 3 * i + j
#             BlockSlice = test_data[block_index][row_count:row_count + 3]
#             RowVector.append(BlockSlice)
#         RowVector = list(itertools.chain(*RowVector))  # flattens array
#         print(RowVector)
#     print()
#     row_count += 3

# test column arraying
# for a in range(3):  # run through how many sets --> finish three sets
#     # first run: 0 3 6, then run 1 4 7, then run 2,5,8
#     slice_index = [0, 3, 6] if a is 0 else [1, 4, 7] if a is 1 else [2, 5, 8]
#     print(slice_index)
#     for i in range(3):  # inter-column index --> finish a set (three columns)
#         RowVector = []
#         for j in range(3):  # inner-column index --> finish a column
#             block_index = 3 * j + i
#             BlockSlice = []
#             BlockSlice.append(test_data[block_index][slice_index[0]])
#             BlockSlice.append(test_data[block_index][slice_index[1]])
#             BlockSlice.append(test_data[block_index][slice_index[2]])
#             RowVector.append(BlockSlice)
#         RowVector = list(itertools.chain(*RowVector))  # flattens array
#         print(RowVector)
#     print()

# itertools islice, takewhile, permutations
# permutations
# index = 0
# for indices in itertools.permutations(mylist, r=None):
#     print(indices)
#     index += 1
# print(index)

# islice
# slice036 = list(itertools.islice(mylist, 0, None, 3))
# print(slice036)

# column array
# order = [0, 3, 6, 1, 4, 7, 2, 5, 8]
# for run in range(3):

#     slice_index = [0, 3, 6] if run is 0 else [1, 4, 7] if run is 1 else [2, 5, 8]
#     print(slice_index)

#     for i in order:
#         if i == 6 or i == 7 or i == 8:
#             RowVector = []
#             RowVector.append(BlockSlice)
#             print(RowVector)
#             BlockSlice = []
#         BlockSlice.append(test_data[i][slice_index[0]])
#         BlockSlice.append(test_data[i][slice_index[1]])
#         BlockSlice.append(test_data[i][slice_index[2]])

# time program
# start_time = time.clock()
# print(time.clock() - start_time, "seconds")

# TestMatrix = sudoku.TestMatrix
# print(TestMatrix, '\n')
# TestMatrix1 = TestMatrix.copy()
# print(TestMatrix1, '\n')
# TempRowMatrix = sudoku.listed_by_row(TestMatrix1)
# print(TempRowMatrix, '\n')


# def solved_condition(RowOrColOrBlkMatrix):
#     SolvednSorted = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#     for i in range(9):
#         RowOrColOrBlkMatrix[i].sort()
#         if RowOrColOrBlkMatrix[i] != SolvednSorted:
#             return False
#     return True


# solved_condition(TempRowMatrix)
# print(TempRowMatrix, '\n')
# print(TestMatrix, '\n')

Test1234 = [[1, 3, 2, 4],
            [2, 4, 1, 3],
            [3, 2, 4, 1],
            [4, 1, 3, 2]]
Rows1234 = [[1, 0, 0, 4],
            [0, 4, 1, 0],
            [3, 0, 4, 0],
            [0, 1, 0, 2]]
Blk1234 = [[1, 0, 0, 4],
           [0, 4, 1, 0],
           [3, 0, 0, 1],
           [4, 0, 0, 2]]
RowBlanksId = [[1, 2], [0, 3], [1, 3], [0, 2]]
RowBlanksVal = [[2, 3], [2, 3], [1, 2], [3, 4]]
ColBlanksVal = [[2, 4], [2, 3], [2, 3], [1, 3]]
'''
# solution 1
for x in range(4): # per row
    for y in RowBlanksId[x]: # per blank
        for vals in itertools.permutations(RowBlanksVal[x],r=2):
            print(vals)
            if vals[y] in ColBlanksVal[y] == True:
                continue
            else:
                pass
        print()
'''
'''
# solution 2
def testset_vals_fit_in_columns(x, Vals):
    num_of_blanks_per_row = len(RowBlanksId[x])
    for y in range(num_of_blanks_per_row):
        if Vals[y] in ColBlanksVal[y] == True: # testset and column shares value
            return False

SolvingMatrix = Blanks1234.copy()
for x in range(4): # per row
    for Vals in itertools.permutations(RowBlanksVal[x],r=None): # per testset combination
        print(Vals)
        if testset_vals_fit_in_columns(x, Vals) == False:
            continue
        else:
            Vals = list(Vals)
            for idx, val in reversed(list(enumerate(SolvingMatrix[x]))):
                if val == 0:
                    SolvingMatrix[x][idx] = Vals[-1]
                    Vals.pop()
            # print(SolvingMatrix)
'''

PVPerMatrix = (((2, 3), (2, 3)), ((2), (3)), ((2), (1)), ((4), (3)))
a = [2, 3, 2, 3]
'''
height = len(PVPerMatrix)
for row in range(height):
    for col1 in range():
'''
