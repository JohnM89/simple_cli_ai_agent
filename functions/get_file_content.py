import os   
from constants import MAX_CHARS
#MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    
    path = os.path.join(working_directory, file_path)
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(os.path.abspath(path)):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(os.path.abspath(path), "r") as f:
            file_contents = f.read(MAX_CHARS)
            if len(file_contents) == MAX_CHARS:
                return f'{file_contents}[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_contents

    except Exception as e:
            return f'Error: {e}'

