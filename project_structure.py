import os

def print_directory_structure(path, indent=""):
    try:
        items = os.listdir(path)
        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                print(indent + "├── " + item + "/")
                print_directory_structure(item_path, indent + "│   ")
            else:
                print(indent + "├── " + item)
    except PermissionError:
        print(indent + "├── (Permission denied)")

if __name__ == "__main__":
    project_root = "."  # Current directory
    print(os.path.basename(project_root) + "/")
    print_directory_structure(project_root)