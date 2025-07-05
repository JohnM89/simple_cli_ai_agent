import os   
import subprocess

def run_python_file(working_directory, file_path, args=None):
    path = os.path.abspath(os.path.join(working_directory, file_path))
    
    try:
        if not path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(path):
            return f'Error: File "{file_path}" not found.'
        
        if file_path[-3:] != '.py':
            return f'Error: "{file_path}" is not a Python file.'
        commands = ['python', path]
        if args != None:
            commands.extend(args)
        print(commands)
        subprocess_output = subprocess.run(commands, shell=False, capture_output=True, timeout=30, cwd=os.path.abspath(working_directory))
        stdout = f'STDOUT: {subprocess_output.stdout}'
        stderr = f'STDERR: {subprocess_output.stderr}'
        output = []
        if subprocess_output.stdout:
            output.append(f'STDOUT: \n{subprocess_output.stdout}')
        if subprocess_output.stderr:
            output.append(f'STDERR: \n{subprocess_output.stderr}')
        if subprocess_output.returncode != 0:
            output.append(f'Process exited with code {subprocess_output.returncode}')
        if not subprocess_output.stdout:
            return 'No output produced'
        return "\n".join(output)

    except Exception as e:

            return f'Error: executing Python file: {e}'
