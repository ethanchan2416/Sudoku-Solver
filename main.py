import sudoku

TestMatrix = ((0, 8, 0, 0, 5, 0, 2, 0, 0),
              (0, 0, 0, 7, 0, 0, 0, 9, 0),
              (0, 3, 0, 0, 0, 2, 0, 0, 0),
              (0, 7, 2, 3, 0, 6, 1, 0, 0),
              (0, 0, 0, 0, 0, 5, 0, 2, 0),
              (5, 0, 3, 0, 1, 0, 8, 0, 0),
              (0, 0, 0, 0, 0, 0, 0, 1, 0),
              (9, 0, 0, 0, 4, 8, 0, 0, 7),
              (0, 0, 0, 9, 2, 0, 4, 0, 0))

print('Manually enter testset, PRESS 1')
print('Use sample testset, PRESS 2\n')
choice = input('Enter choice: ')
print()
if choice is '1':
    testset = sudoku.input_testset()
elif choice is '2':
    testset = TestMatrix
sudoku.solve_sudoku(testset, 'row')
