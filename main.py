import sudoku
from sudoku import *

TestMatrix = blk_to_row(sudoku.TestMatrix)
WorldHardestRow = blk_to_row(WorldHardest)

TestSet = (TestMatrix, SdkEasyRow, SdkMediumRow, SdkHardRow, SdkEvilRow, WorldHardestRow)

for testset in TestSet:
  solve_sudoku(testset, 'row')
