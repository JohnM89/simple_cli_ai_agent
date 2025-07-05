

from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .write_file import write_file
from .run_python_file import run_python_file


function_names = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

list_of_avalible_functions = [{
    "name":"get_files_info",
    "description":"Lists files in the specified directory along with their sizes, constrained to the working directory.",
    "file_path":"directory",
    "file_path_description":"The directory argument to list files from, relative to the working directory. If not provided, lists files in the working directory itself (see directory)."
},{
                                "name":"get_file_content",
                                "description":"Read file contents",
                                "file_path":"file_path",
                                "file_path_description":"Read the contents of the file at the file_path provided"
                                },{
                                "name":"run_python_file",
                                "description":"Execute Python files with optional arguments",
                                "args": "args",
                                "args_description": "the (optional) args to invoke file execution with",                               
                                "file_path":"file_path",
                                "file_path_description":"Run python file at file path with args (if args)"
                                },{
                                "name":"write_file",
                                "description":"Write or overwrite files",

                                "file_path":"file_path",
                                "contents": "content",
                                "content_description": "content of the requested content to write",
                                "file_path_description":"path to write to or overwrite file(s)"

                                }]

