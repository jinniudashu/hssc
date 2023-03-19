import os

project_root = '/Users/miles/Documents/JiangNing/hssc/src'  # 项目根目录

output_file = os.path.join(project_root, 'extracted_code.txt')

with open(output_file, 'w') as output:
    for root, dirs, files in os.walk(project_root):
        if 'migrations' in dirs:
            dirs.remove('migrations')  # 忽略 migrations 目录

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_root)

                output.write(f"\n{'*' * 80}\n")
                output.write(f"File: {relative_path}\n")
                output.write(f"{'*' * 80}\n\n")

                with open(file_path, 'r') as input_file:
                    content = input_file.read()
                    output.write(content)

print(f"Extracted code saved to: {output_file}")
