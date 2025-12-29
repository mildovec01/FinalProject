# Example of SyntaxError --> missing colon after defined function
def greet(name)
    print("Hello", name)



# Example of SyntaxError --> unclosed bracket
print("Hello"
      


# Example of IdentationError --> wrong identing
def foo():
print("bad indent")



# Example of NameError --> variable isnt set before printing
print(x)



# Example of TypeError --> incompatible types
print(5 + "5")



# Example of ValueError --> set unexpected type
x = int(abc)
print(x)



# Example of ZeroDivisionError --> dividing by zero
print(10 / 0)



#Example of IndexError --> expected higher element, but the valid range is short
arr = [1, 2, 3]
print(arr[5])



# Example of KeyError --> the key isnt set
d = {"a": 1}
print(d[b])



# Example of AttributeError --> unexpected code
x = 123
print(x.upper())



# Example of EOFError --> empty input
name = input("Your name: ")
print(name)
# This type of error is rare in real life.
# It wont work in the Code Tutor, because input() waits for the input and the web app will in the most cases lag
# You can keep it here and use it in your own code or program to try this error
