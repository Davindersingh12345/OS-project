import os

def create_test_files():
    with open("file1.txt", "w") as file1:
        file1.write("This is a test file for Jerome.\n")
    with open("data.txt", "w") as file2:
        file2.write("Another test file.\n")

def secure_open(username, filename, mode):
    try:
        return os.open(filename, mode, 0o644)
    except OSError:
        return -1

def secure_read(fd, buffer_size):
    try:
        return os.read(fd, buffer_size)
    except OSError:
        return b""

def secure_write(fd, content):
    try:
        os.write(fd, content.encode())
    except OSError:
        print("Error writing to file.")

def main():
    create_test_files()
    
    username = input("Enter your username: ")
    fd = -1
    
    while True:
        print("\n1. Open File\n2. Read File\n3. Write to File\n4. Exit")
        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue
        
        if choice == 1:
            filename = input("Enter filename to open: ")
            if fd > 0:
                os.close(fd)
            fd = secure_open(username, filename, os.O_RDWR | os.O_CREAT)
            if fd < 0:
                print("Failed to open file.")

        elif choice == 2:
            if fd > 0:
                content = secure_read(fd, 256)
                if content:
                    print("File Content:\n" + content.decode())
                else:
                    print("File is empty or error reading file.")
            else:
                print("Open a file first!")

        elif choice == 3:
            if fd > 0:
                content = input("Enter content to write: ")
                secure_write(fd, content)
                print("Content written successfully.")
            else:
                print("Open a file first!")

        elif choice == 4:
            print("Exiting...")
            if fd > 0:
                os.close(fd)
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
