import os

def get_file_names(include, exclude, folder_path='distances/'):
    files = os.listdir(folder_path)
    final_files = []

    if include != '*':
        for file_name in files:
            if reduce(lambda x, y: x and y, [x in file_name for x in include]):
                final_files.append(file_name)
    else:
        final_files = files[:]

    files = []
    if exclude != None:
        for file_name in final_files:
            if reduce(lambda x, y: x or y, [x in file_name for x in exclude]):
                files.append(file_name)

    for f in files:
        final_files.remove(f)

    return final_files
