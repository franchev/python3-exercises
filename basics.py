import datetime
print("The date and time is", datetime.datetime.now())

# using variables
x = datetime.datetime.now()
print(x)

# different data type
# integer
x = 10
# float
y = 10.1
# string
z = "hello"
# list
values = [10, 20, 30]
# range
rangeList = list(range(1,10)) 
print(rangeList)
# range using a step
rangeStepList = list(range(1, 10, 2))
print(rangeStepList)

# the help function example help(str.upper)
# to print a list of functions
print(dir(__builtins__))

# Here a list, then print how many time the value 10.0 occurred
student_grades = [9.1, 8.8, 10.0, 7.7, 6.8, 8.0, 10.0, 8.1, 10.0, 9.9]
print(student_grades.count(10.0))

# Example of dictionary -> key and values. Keys must be unique
student_grades_dic = {"Mary": 9.1, "Sim": "8.8", "John": 7.5}

# Tuple a list with a parenthesis, it is not immutable
monday_temperatures = (1, 4, 5)

# modifying a list
student_grades.append(10.5)
#monday_temperatures.clear()  # completely clears the list

# accessing sliced items from a list
monday_temperatures[1:4]
# get first 2 items
monday_temperatures[0:2] # or monday_temperatures[:2]
# Get from 3rd item to the end
monday_temperatures[3:]

# get last item
monday_temperatures[-1]


