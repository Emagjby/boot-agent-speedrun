from functions.get_files_info import get_files_info

if __name__ == "__main__":
    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print("\n\n")

    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print("\n\n")

    print("Result for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))
    print("\n\n")

    print("Result for '../' directory:")
    print(get_files_info("calculator", "../"))
    print("\n\n")
