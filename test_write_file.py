from functions.write_file import write_file

if __name__ == "__main__":
    print("Result for writing to 'lorem.txt':")
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print("\n\n")

    print("Result for writing to 'pkg/morelorem.txt':")
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print("\n\n")

    print("Result for writing to '/tmp/temp.txt':")
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
    print("\n\n")
