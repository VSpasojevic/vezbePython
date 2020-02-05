import sys

print("__name__ value:", __name__)

print("Hello from module")

def main():
    print("Hello from main()")
    myfoo("blah blah msg...")

def myfoo(arg1):
    print("Hello from foo()")
    print("arg1 value: ", arg1)

if __name__ == '__main__':
    print("Hello from executable module")
    main()