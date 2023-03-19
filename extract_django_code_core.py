import os

def extract_django_code(project_root):
    models_file_path = os.path.join(project_root, 'core', 'models.py')
    views_file_path = os.path.join(project_root, 'core', 'views.py')
    urls_file_path = os.path.join(project_root, 'core', 'urls.py')
    settings_file_path = os.path.join(project_root, 'hssc', 'settings.py')

    output_file_path = os.path.join(project_root, 'extracted_code_core.txt')

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write('==== models.py ====\n\n')
        with open(models_file_path, 'r', encoding='utf-8') as models_file:
            output_file.write(models_file.read())

        output_file.write('\n\n==== views.py ====\n\n')
        with open(views_file_path, 'r', encoding='utf-8') as views_file:
            output_file.write(views_file.read())

        output_file.write('\n\n==== urls.py ====\n\n')
        with open(urls_file_path, 'r', encoding='utf-8') as urls_file:
            output_file.write(urls_file.read())

        output_file.write('\n\n==== settings.py ====\n\n')
        with open(settings_file_path, 'r', encoding='utf-8') as settings_file:
            output_file.write(settings_file.read())

if __name__ == '__main__':
    project_root = '/Users/miles/Documents/JiangNing/hssc/src'
    extract_django_code(project_root)
