import os   

def write_file(working_directory, file_path, content):
    try:
        path = os.path.join(working_directory, file_path)
        
        if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

