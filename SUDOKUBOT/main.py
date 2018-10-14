import sys
import copy
# from termcolor import colored

# open log for documenting moves
command_log = open("sudoku_bot.log", "w")
# global_area = ""
# global_row_position = 0
# global_col_position = 0
# global_command = ""

# Puzzle starts out with range of values 1-9 in each square, as all values are possible in an empty board
puzzle = [[range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10)], 
            [range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10)], 
            [range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10)], 
            [range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10)], 
            [range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10)], 
            [range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10)], 
            [range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10)], 
            [range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10)], 
            [range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10), range(1, 10)]]

# Encodes, predefined values, and solved
puzzle_mask = range(81)
# Mask codes: 0 == unsolved, 1 == const/predef, 2 == solved

# Creates a sudoku puzzle from a list of numbers
def create_puzzle(num_list):
    row_count = 0
    col_count = 0
    index_count = 0
    for number in num_list:

        if number != 0:
            puzzle[row_count][col_count] = [number]
            puzzle_mask[index_count] = 1
        else:
            puzzle[row_count][col_count] = range(1, 10)
            puzzle_mask[index_count] = 0

        if (col_count == 8):
            col_count = 0
            row_count += 1
        else:
            col_count += 1

        index_count += 1

# Removes possibilities in a line of squares (either a row or col)
def check_line(line):
    # Removing constant values from non_constant bins
    removals = []
    for bn in line:
        # Collects constant values
        if ( len(bn) == 1 ):
            removals.append(bn[0])

    # Removes constants
    for bn in line:
        if ( len(bn) > 1 ):
            for removal in removals:
                if removal in bn:
                    command_log.write("rm -> n: " + str(removal) + " from bn " + str(line.index(bn)) + "\n")
                    bn.remove(removal)

    # If a number is only at a single index, that index is set to that number exclusively
    for num in range(1, 10):
        num_count = 0
        index = 0
        for bn in line:
            if num in bn:
                num_count += 1
                index = line.index(bn)
        if ( num_count == 1 ):
            line[index] = [num]


# Returns a list of all values in a given column for checking
def col_to_line(col_index):
    line = []
    for row in puzzle:
        line.append(row[col_index])
    return line

# Returns a list of all values in a given square for checking
def square_to_line(square_index):
    line = []
    starting_row = (square_index/3)*3
    starting_col = (square_index%3)*3

    for row in [starting_row, starting_row + 1, starting_row + 2]:
        for col in [starting_col, starting_col + 1, starting_col + 2]:
            line.append(puzzle[row][col])
    
    return line


def full_check():
    i = 0
    for row in puzzle:
        sq = square_to_line(i)
        check_line(sq)

        col = col_to_line(i)
        check_line(col)

        check_line(row)
        i += 1
    
    region_rowcol_solve()

def region_rowcol_solve():
    # Use possibilities that are in single rows or cols to eliminate possibilities in other squares
    # The single row/col check should be done on all squares, removing possibilities from all other squares in the same row/col.    
    for i in range(9):
        square = square_to_line(i)
        for num in range(1, 10):
            rows = set()
            cols = set()
            bin_index = 0
            for bn in square:
                if ( num in bn ):
                    rows.add( bin_index/3 + (i/3)*3 )
                    cols.add( bin_index%3 + (i%3)*3 )
                bin_index += 1

            if ( len(rows) == 1 ):                
                row = puzzle[rows.pop()]
                bin_index = 0
                for bn in row:
                    # bin is not in region with vector, and number is in bin
                    if ( (bin_index/3 != i%3) and (num in bn) and len(bn) > 1 ):
                        bn.remove(num)
                    bin_index += 1

            if ( len(cols) == 1 ):
                col = col_to_line(cols.pop())
                bin_index = 0
                for bn in col:
                    # bin is not in region with vector, and number is in bin
                    if ( (bin_index/3 != i/3) and (num in bn) and len(bn) > 1 ):
                        bn.remove(num)
                    bin_index += 1


def print_puzzle(display_code):
    
    mask_counter = 0
    for row in puzzle:
        for col in row:
            sys.stdout.write("[")
            if (len(col) > 1):
                if (display_code):
                    sys.stdout.write(" ")
                else:
                    sys.stdout.write(str(col))
            else:
                sys.stdout.write(str(col[0]))
                
                # Colours predefined squares white
                # if ( puzzle_mask[mask_counter] == 1 ):
                    # sys.stdout.write( colored(str(col[0]), 'white') )

                # Colours solved squares green
                # if ( puzzle_mask[mask_counter] == 2 ):
                    # sys.stdout.write( colored(str(col[0]), 'green') )

                # Colours newly solved squares red, sets their mask to solved
                if ( puzzle_mask[mask_counter] == 0 ):
                    command_log.write("sol -> r: " + str(puzzle.index(row)) + " c: " + str(row.index(col)) + " n: " + str(col[0]) + "\n" )
                    # sys.stdout.write( colored(str(col[0]), 'red') )
                    puzzle_mask[mask_counter] = 2
                    
                    
            sys.stdout.write("]")
            mask_counter += 1
        print " "
    
    print " "

def check_solution():

    for i in range(9):
        if ( (not check_solution_line(col_to_line(i))) or (not check_solution_line(puzzle[i])) or (not check_solution_line(square_to_line(i))) ):
            return 0

    return 1
        

def check_solution_line( line ):
    # Sum of all integers fom [1, 9] is 45
    check_sum = 45
    bn_sum = 0
    for bn in line:
        if ( len(bn) > 1 ):
            return 0
        bn_sum += bn[0]
    # Checks if the sum of all the numbers in a row, col or region are equal to the checksum
    # which is the sum of all integers from [1, 9]
    if ( bn_sum != check_sum ):
        return 0

    return 1

# def get_min_poss():
#     min_poss = 9
#     row = 0
#     col = 0

#     min_row = 0
#     min_col = 0
#     for row in puzzle:
#         for bn in row:
#             if ( len(bn) < min_poss ):
#                 min_poss = len(bn)
#                 min_row = row
#                 min_col = col
#             col += 1
#         row += 1
    
#     return (min_poss, min_row, min_col)

# def guess_num():
#     start_point = get_min_poss()
#     return 0

def solve_puzzle( puzzle_list ):
    command_log.write("\n\n\nSTARTING SOLVE ON NEW PUZZLE\n\n")
    create_puzzle( puzzle_list )

    # Keeps running checks til the puzzle is solved
    solved = 0
    prev_mask = copy.copy(puzzle_mask)
    print_puzzle(1)
    while (not solved):        
        full_check()
        print_puzzle(1)
        # Check if puzzle is solved by looking at mask codes
        solved = 1
        diff = 0
        prev_mask_index = 0 
        for code in puzzle_mask:
            if (code == 0):
                solved = 0
            if (prev_mask[prev_mask_index] != code):
                diff = 1
            prev_mask_index += 1
        prev_mask = copy.copy(puzzle_mask)

        if (not diff):
            print "UNSOLVABLE!"
            print_puzzle(0)
            return
            # guess_num()

    if ( check_solution() ):
        print "SOLVED!\n\n"
    else :
        print "ERROR!\n\n"



puzzle_list_2018_07_29 = [0,0,9,0,0,2,0,0,0,0,0,1,0,0,0,8,0,0,0,6,0,3,0,0,0,4,1,6,0,0,0,8,0,9,0,0,0,0,0,4,2,5,0,0,0,0,0,3,0,6,0,0,0,8,3,5,0,0,0,7,0,2,0,0,0,8,0,0,0,4,0,0,0,0,0,5,0,0,6,0,0]
solve_puzzle(puzzle_list_2018_07_29)

puzzle_list_2018_07_31 = [0,0,5,7,0,2,0,0,0,0,8,0,0,0,4,1,0,0,2,3,0,0,5,0,0,0,0,4,0,0,2,0,0,8,0,0,0,0,7,0,8,0,3,0,0,0,0,6,0,0,1,0,0,7,0,0,0,0,7,0,0,1,5,0,0,4,9,0,0,0,8,0,0,0,0,1,0,8,4,0,0]
solve_puzzle(puzzle_list_2018_07_31)   

puzzle_list_2018_08_01 = [0,6,1,9,0,0,0,0,0,9,0,0,0,3,0,4,5,0,5,0,0,2,0,1,0,0,0,8,0,9,0,1,2,0,0,0,0,3,0,5,6,0,2,0,0,0,0,2,3,0,7,9,0,0,0,9,0,0,5,8,0,2,6,0,8,0,0,0,0,7,3,0,0,0,0,0,0,0,5,0,0]
solve_puzzle(puzzle_list_2018_08_01)

puzzle_list_2018_08_08 = [0,0,0,4,0,0,6,0,1,0,0,4,8,5,0,0,0,0,0,0,5,0,0,0,3,0,0,3,2,0,0,0,0,0,0,0,7,9,0,0,1,0,0,6,2,0,0,0,0,0,0,0,3,8,0,0,2,0,0,0,9,0,0,0,0,0,0,8,6,4,0,0,9,0,3,0,0,1,0,0,0]
solve_puzzle(puzzle_list_2018_08_08) 

puzzle_list_2018_08_09 = [0,0,0,5,6,8,0,0,0,0,0,4,0,0,0,7,0,0,0,0,3,0,0,0,1,0,0,0,8,7,1,3,9,6,2,0,0,3,0,0,0,0,0,5,0,0,6,0,0,2,0,0,1,0,0,1,0,0,5,0,0,6,0,0,9,0,0,0,0,0,7,0,0,0,5,6,7,1,9,0,0]
solve_puzzle(puzzle_list_2018_08_09)

puzzle_list_2018_09_07 = [0,5,0,0,9,0,0,0,2,1,7,0,0,0,6,0,0,0,0,0,0,0,4,7,0,0,0,0,0,0,0,2,0,5,3,0,8,0,1,0,0,0,2,0,6,0,2,5,0,1,0,0,0,0,0,0,0,8,5,0,0,0,0,0,0,0,1,0,0,0,7,8,6,0,0,0,7,0,0,9,0]
solve_puzzle(puzzle_list_2018_09_07)

hardest_sudoku_puzzle = [8,0,0,0,0,0,0,0,0,0,0,3,6,0,0,0,0,0,0,7,0,0,9,0,2,0,0,0,5,0,0,0,7,0,0,0,0,0,0,0,4,5,7,0,0,0,0,0,1,0,0,0,3,0,0,0,1,0,0,0,0,6,8,0,0,8,5,0,0,0,1,0,0,9,0,0,0,0,4,0,0]
solve_puzzle(hardest_sudoku_puzzle)
command_log.close()



