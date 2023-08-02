from math import sqrt
import random
import numpy as np

# will reformat the matrix to enhance readability
def formatMatrix(matrix):
    if type(matrix[0]) == list:
        formatted = ""
        for i in range(len(matrix)):
            formatted += " ["
            for k in range(len(matrix)):
                formatted += str(round(matrix[i][k],1)) + " "
            formatted += "]\n"
        return ("[" + formatted[1:len(formatted)-1]+"]")
    else:
        return matrix

# creating a square matrix out a list of n numbers
# update to handle non-square matrices
def create_matrix(lst):
    chunked = []
    # assuming arr is a square array,
    # the # of rows/columns == sqrt(length of arr)
    rows_and_columns = int(sqrt(len(lst)))
    # split the arr into equal size sub-arrays
    for i in range(0, len(lst), rows_and_columns):
        chunked.append(lst[i: i + rows_and_columns])
    return chunked

# for 1d vectors x square matrix
def multiply_matrices2(vector, matrix):
    multiplied = []
    nm = len(vector)
    for r in range(nm):
        for c in range(nm):
            total = 0
            for t in range(nm):
                m1 = vector[t]
                m2 = matrix[t][c]
                total += m1 * m2
            multiplied.append(total)
    return multiplied[0:len(vector)]

# assumes the two square matrices are equal in dimensions
def multiply_matrices1(matrix1, matrix2):
    multiplied = []
    # the dimension number
    nm = len(matrix1[0])
    # setting up the sublists based on the dimensions of m1 and m2
    # will run for as many sublists
    for i in range(nm):
        multiplied.append([])
    # given both matrices are n x m
    # this iterates from r=0 to r=n
    # m1 stays in the same row, m2 stays in same column 
    for r in range(nm):
        # this iterates from c=0 to c=m
        for c in range(nm):
            # these first two loops are only to get the individual positions of multiplied
            # this next loop is to calculate the values
            total = 0
            for t in range(nm):
                # changes column
                m1 = matrix1[r][t]
                # changes row
                m2 = matrix2[t][c]
                # calculates the sum of all multiplications
                total += m1 * m2
            # adds total to the row in multiplied
            # because individual positions don't exist (it is empty)
            multiplied[r].append(total)
    # numpy reshape to print out as matrix
    return multiplied
        
# calculates a matrix**power
def power_matrix_calculator(matrix, power):
    # save original matrix to keep multiplying
    original_matrix = matrix
    # loop runs for power-1 because one function call == power of 2
    for i in range(power-1):
        # call func with updated matrix and its original self
        matrix = multiply_matrices1(matrix, original_matrix)
    return matrix

# determines if a matrix is regular
# a matrix is regular if M^n has all positive entries
# where n is pos whole # and not zero
# test all powers which are <= (n-1)^2 + 1 where M is nxn
# ex. M is 3x3, m <= (3-1)^2+1 = 5
# only one of the powers have to be True
def matrixIsRegular(matrix):
    n = len(matrix)
    for i in range(1, pow(n-1,2)+2):
        matrixNth = power_matrix_calculator(matrix,i)
        regular = []
        for row in matrixNth:
            for column in row:
                if column > 0:
                    regular.append(True)
                else:
                    regular.append(False)
        if False not in regular:
            return True
    return False

# determines if a matrix is close to equilibrium
# if a matrix is regular, it has an equilibrium
# tells us when T^n is n dist from T^n-1, where dist is n
# tells us which power it stopped at
# tells us what the matrix is at that power
# the first row is the equilibrium vector because all the values will be the same in the long run
def equilibriumMatrixPower(matrix, dist):
    if matrixIsRegular(matrix):
        power = 2
        while True:
            # subtract matrix^n from matrix^n-1, get abs value
            # if all values of subtracted matrix are <= dist, break from loop and return the power
            matrixNth = power_matrix_calculator(matrix,power)
            matrixNthMinus1 = power_matrix_calculator(matrix,power-1)
            
            val = []
            for i in range(len(matrixNth)):
                for k in range(len(matrixNth)):
                    if matrixNth[i][k]-matrixNthMinus1[i][k] <= dist:
                        val.append(True)
                    else:
                        val.append(False)
            if False in val:
                power += 1
            else:
                return power
    return 0

# acts as the user control center, user enters space-seperated numbers
def userControlCenter():
    print("A) Multiply Matrices\nB) Power Calculator\nC) Find Equilibrium\nD) Validate Regular Matrix")
    choice = input("Select a choice: ").upper()
    if choice == "A":
        print()
        print("Creating 2 matrices...")
        try:
            print("A) 1D Vector x nD Matrix\nB) nD Matrix x nD Matrix")
            choice2 = input("Select a choice: ").upper()
            if choice2 == "A":
                numbers1 = input("Enter n numbers in which n is equal to the number of rows for your second matrix:\n")
                vector = [float(i) for i in numbers1.split(" ")]
                numbers2 = input("Enter numbers seperated by 1 space, must be a squarable number of numbers:\n")
                matrix = create_matrix([float(i) for i in numbers2.split(" ")])
                print()
                print(formatMatrix(multiply_matrices2(vector,matrix)))
            if choice2 == "B":
                numbers1 = input("Enter numbers seperated by 1 space, must be a squarable number of numbers:\n")
                matrix1 = create_matrix([float(i) for i in numbers1.split(" ")])
                numbers2 = input("Enter numbers seperated by 1 space, must be a squarable number of numbers:\n")
                matrix2 = create_matrix([float(i) for i in numbers2.split(" ")])
                print()
                print(formatMatrix(multiply_matrices1(matrix1,matrix2)))    
        except:
            print("An error occurred. Please re-enter your numbers according to the specified criteria.")
    if choice == "B":
        try:
            print()
            print("Creating a matrix...")
            numbers = input("Enter numbers seperated by 1 space, must be a squarable number of numbers:\n")
            matrix = create_matrix([float(i) for i in numbers.split(" ")])
            power = int(input("To what number do you want to raise your matrix to? "))
            print()
            print(formatMatrix(power_matrix_calculator(matrix,power)))
        except:
            print("An error occurred. Please re-enter your numbers according to the specified criteria.")
    if choice == "C":
        try:
            print()
            print("Creating a matrix...")
            numbers = input("Enter numbers seperated by 1 space, must be a squarable number of numbers:\n")
            matrix = create_matrix([float(i) for i in numbers.split(" ")])
            dist = input("What distance do you want to test for? ")
            e = equilibriumMatrixPower(matrix,float(dist))
            if e!=0:
                print("Power is:", e)
                print("Limit of matrix:\n" + str(formatMatrix(power_matrix_calculator(matrix, e))))
            else:
                print("Matrix does not have an equilibrium.")
        except:
            print("An error occurred. Please re-enter your numbers according to the specified criteria.")
    if choice == "D":
        try:
            print()
            print("Creating a matrix...")
            numbers = input("Enter numbers seperated by 1 space, must be a squarable number of numbers:\n")
            matrix = create_matrix([float(i) for i in numbers.split(" ")])
            print()
            isRegular = matrixIsRegular(matrix)
            if isRegular:
                print("This matrix is regular.")
            else:
                print("This matrix is not regular.")
        except:
            print("An error occurred. Please re-enter your numbers according to the specified criteria.")
userControlCenter()


# find the limit as time goes on (ex. if 10 digits produced, if 8 of them match the previous matrix, we've reached it)
# finding the maximum difference between matrix, it returns the power
# as n goes bigger it grows closer to a specific matrix
