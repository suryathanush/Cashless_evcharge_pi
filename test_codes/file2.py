# file2.py
import file1

# Access the shared_variable from file1
print(file1.shared_variable)

# Update the variable in file1
file1.update_variable()

# Access the updated shared_variable
print(file1.shared_variable)
