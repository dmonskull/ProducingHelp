import os

def get_folder_structure(folder_path):
    folder_structure = {}
    for root, dirs, files in os.walk(folder_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            folder_structure[dir_path] = len(os.listdir(dir_path))
    return folder_structure

def generate_text(folder_name, folder_structure):
    text_content = f"# {folder_name}\n\n"
    
    for folder, file_count in folder_structure.items():
        folder_name_only = os.path.basename(folder)
        text_content += f"{folder_name_only} : {file_count}\n"
    
    return text_content

def main():
    folder_path = input("Enter the path of the folder: ").strip().strip('"')
    
    if not os.path.isdir(folder_path):
        print("Invalid folder path. Please try again.")
        return
    
    use_folder_name = input("Do you want to use the folder name as the drumkit name? (1 for yes, 2 for no): ").strip()
    if use_folder_name == '1':
        folder_name = os.path.basename(folder_path)
    elif use_folder_name == '2':
        folder_name = input("Enter the name of the drumkit: ").strip()
    else:
        print("Invalid choice. Please try again.")
        return
    
    folder_structure = get_folder_structure(folder_path)
    
    text_content = generate_text(folder_name, folder_structure)
    
    output_file = os.path.join(folder_path, "drumkit_description.txt")
    with open(output_file, "w") as f:
        f.write(text_content)
    
    print(f"Description file created: {output_file}")

if __name__ == "__main__":
    main()
