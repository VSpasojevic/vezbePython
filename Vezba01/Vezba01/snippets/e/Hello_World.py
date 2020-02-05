import sys

print("__name__ value:", __name__)

print("Hello from module")

def main():
    print("Hello from main()")
    myfoo()

def myfoo():
    print("Hello from foo()")

if __name__ == '__main__':
    print("Hello from executable module")
    main()