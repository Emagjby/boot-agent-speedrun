from functions.get_file_content import get_file_content

if __name__ == "__main__":
    print("Result for main.py:")
    print(get_file_content("calculator", "main.py"))
    print("\n\n")

    print("Result for pkg/calculator.py:")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print("\n\n")

    print("Result for /bin/cat:")
    print(get_file_content("calculator", "/bin/cat"))
    print("\n\n")

    print("Result for pkg/does_not_exist.py:")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))
    print("\n\n")
