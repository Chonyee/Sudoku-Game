import numpy as np
from dokusan import generators, renderers

def fixBoard(board):
  board = list(map(int, str(board)))
  fixedBoard = []
  for i in range(9):
    row = []
    for j in range(9):
      row.append(board[j])
    del board[0:9]
    fixedBoard.append(row)
  board = np.array(fixedBoard)
  return board

def genRandBoard():
  userinput = ''
  while userinput.lower() not in ['yes', 'no']:
    userinput = input("Generate random Sudoku board (yes/no)? ")

  if userinput.lower() == 'yes':
    board = generators.random_sudoku(avg_rank=150)

  if userinput.lower() == 'no':
    userinput = ''
    while userinput.lower() not in ['yes', 'y', 'no', 'n']:
      userinput = input("Input Sudoku board (yes/no)? ")

    if userinput.lower() == 'yes':
      for i in range(9):
        row = []
        for j in range(9):
          number = ''
          while number not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            number = str(input("Enter number for Row {} Column {}:".format(i+1, j+1)))
          row.append(int(number))
        board.append(row)
    if userinput.lower() == 'no':
      print("Generating new Sudoku board...")
      board = generators.random_sudoku(avg_rank=150)
  board = fixBoard(board)
  return board

def findZero(board):
  for row in range(9):
    for col in range(9):
      if board[row][col] == 0: return (row, col)
  return None

def valid(board, number, xy):
  for row in range(9):
    if board[row][xy[1]] == number and xy[0] != row:
      return False

  for col in range(9):
    if board[xy[0]][col] == number and xy[1] != col:
      return False

  boxRow = xy[0] // 3
  boxCol = xy[1] // 3

  for row in range(boxRow*3, boxRow*3 + 3):
    for col in range(boxCol*3, boxCol*3 + 3):
      if board[row][col] == number and (row, col) != xy:
        return False
  return True

def sudoku(board):
  zero = findZero(board)
  if not zero:
    return True
  else:
    row, col = zero

  for number in range(1,10):
    if valid(board, number, (row, col)):
      board[row][col] = number

      if sudoku(board): return True

      board[row][col] = 0
  return False

def printBoard(board):
  side = 9
  base = 3
  def expandLine(line):
    return line[0] + line[5 : 9].join([line[1 : 5] * (base - 1)] * base)+ line[9 : 13]
  line0  = expandLine("╔═══╤═══╦═══╗")
  line1  = expandLine("║ . │ . ║ . ║")
  line2  = expandLine("╟───┼───╫───╢")
  line3  = expandLine("╠═══╪═══╬═══╣")
  line4  = expandLine("╚═══╧═══╩═══╝")

  symbol = " 1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  nums   = [[""] + [symbol[n] for n in row] for row in board]
  print(line0)
  for r in range(1, side + 1):
    print("".join(n + s for n, s in zip(nums[r - 1], line1.split("."))))
    print([line2 ,line3 ,line4][(r % side == 0) + (r % base == 0)])

def validateNumber(row, col):
  while True:
    number = input("Enter number for Row {} Column {}: ".format(row, col))
    if number.isdigit():
      if int(number) > 0 and int(number) < 10:
        return int(number)
      
def validateRow():
  while True:
    row = input("Enter which row you would like to enter a number for: ")
    if row.isdigit():
      if int(row) > 0 and int(row) < 10:
        return int(row)
      
def validateCol():
  while True:
    col = input("Enter which column you would like to enter a number for: ")
    if col.isdigit():
      if int(col) > 0 and int(col) < 10:
        return int(col)

def playGame():
  playBoard = genRandBoard()
  solvedBoard = np.copy(playBoard)
  sudoku(solvedBoard)
  printBoard(playBoard)


  while (playBoard.all != solvedBoard.all):
    row = validateRow()
    col = validateCol()
    
    if playBoard[row-1][col-1] == 0:
      number = validateNumber(row, col)
      if number == solvedBoard[row-1][col-1]:
        print("Correct!")
        playBoard[row-1][col-1] = number
      else: print("Wrong, try again..")
    else: print("\nNumber in the spot is already filled!")
    printBoard(playBoard)

  pause = input("Board Solved!")