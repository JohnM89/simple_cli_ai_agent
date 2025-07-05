import os   

def get_files_info(working_directory, directory=None):

    if directory == None:
        directory = "."

    path = os.path.join(working_directory, directory)
    
    if not os.path.abspath(path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(os.path.abspath(path)):
        return f'Error: "{directory}" is not a directory'
    
    try:
        directory_list = []
        for file in os.scandir(os.path.abspath(path)):    
                format = f"\n- {file.name}: file_size={file.stat().st_size}, is_dir={file.is_dir()}"                 
                directory_list.append(format)          
        return " ".join(directory_list)
    
    except Exception as e:
        return f'Error: {e}'    
    

