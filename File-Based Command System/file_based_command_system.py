import os

def create_file(filename):
    """Create a new file."""
    with open(filename, 'w') as f:
        pass
    print(f"File '{filename}' created.")

def write_file(filename, content):
    """Write content to a file."""
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Content written to '{filename}'.")

def read_file(filename):
    """Read and print content from a file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()
        print(f"Content of '{filename}':\n{content}")
    else:
        print(f"File '{filename}' does not exist.")

def delete_file(filename):
    """Delete a file."""
    if os.path.exists(filename):
        os.remove(filename)
        print(f"File '{filename}' deleted.")
    else:
        print(f"File '{filename}' does not exist.")

def process_commands(command_file):
    """Process commands from a file."""
    with open(command_file, 'r') as f:
        for line in f:
            parts = line.strip().split(' ', 2)
            command = parts[0]
            args = parts[1:]

            if command == 'create_file':
                create_file(*args)
            elif command == 'write_file':
                write_file(*args)
            elif command == 'read_file':
                read_file(*args)
            elif command == 'delete_file':
                delete_file(*args)
            else:
                print(f"Unknown command: {command}")

if __name__ == "__main__":
    command_file = 'commands.txt'
    process_commands(command_file)

"""
>> Command File
create_file test.txt
write_file test.txt Hello, world!
read_file test.txt
delete_file test.txt
"""
