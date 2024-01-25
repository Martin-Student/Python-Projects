


def add(n1, n2):
    return n1 + n2

def substract(n1, n2):
    return n1 - n2

def multiply(n1, n2):
    return n1 * n2

def divide(n1, n2):
    return n1 / n2

operations = {
    "+": add,
    "-": substract,
    "*": multiply,
    "/": divide
}



num1 = int(input("What's the first number?: "))
sym = input("What's the operation? ")
num2 = int(input("What's the second number?: "))
num3 = 0
for key in operations:
    if key == "+" and sym == "+":
        print(add(num1, num2))
    elif key == "-" and sym == "-":
        print(substract(num1, num2))
    elif key == "*" and sym == "*":
        print(multiply(num1, num2))
    elif key == "/" and sym == "/":
        print(divide(num1, num2))
