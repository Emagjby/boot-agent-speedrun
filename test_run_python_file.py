from functions.run_python_file import run_python_file

if __name__ == "__main__":
    print("Result for running 'main.py' without arguments:")
    print(run_python_file("calculator", "main.py"))
    print("\n\n")

    print("Result for running 'main.py' with argument '3 + 5':")
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("\n\n")

    print("Result for running 'tests.py':")
    print(run_python_file("calculator", "tests.py"))
    print("\n\n")

    print("Result for running '../main.py':")
    print(run_python_file("calculator", "../main.py"))
    print("\n\n")

    print("Result for running 'nonexistent.py':")
    print(run_python_file("calculator", "nonexistent.py"))
    print("\n\n")

    print("Result for running 'lorem.txt':")
    print(run_python_file("calculator", "lorem.txt"))
    print("\n\n")
