from google import genai
from google.genai import types
from constants import WORKING_DIRECTORY

def build_schemas(list_of_avalible_functions):
    schemas = {}
    for dict in list_of_avalible_functions:
        if "contents" in dict:
            schemas[f'schema_{dict["name"]}'] = types.FunctionDeclaration(
                name=f'{dict["name"]}',
                description=f'{dict["description"]}',
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={

                        f'{dict["file_path"]}': types.Schema(
                            type=types.Type.STRING,
                            description=f'{dict["file_path_description"]}',
                        ),
                        f'{dict["contents"]}': types.Schema(
                            type=types.Type.STRING,
                            description=f'{dict["content_description"]}',
                        ),
                    },
                ),
            )
        elif "args" in dict:
            schemas[f'schema_{dict["name"]}'] = types.FunctionDeclaration(
                name=f'{dict["name"]}',
                description=f'{dict["description"]}',
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={

                        f'{dict["file_path"]}': types.Schema(
                            type=types.Type.STRING,
                            description=f'{dict["file_path_description"]}',
                        ),
                        f'{dict["args"]}': types.Schema(
                            type=types.Type.ARRAY,
                            items=types.Schema(
                                type=types.Type.STRING,
                                description=f'{dict["args_description"]}',
                            ),
                            description=f'{dict["args_description"]}',
                        ),

                    },
                ),
            ) 
        else:
            schemas[f'schema_{dict["name"]}'] = types.FunctionDeclaration(
                name=f'{dict["name"]}',
                description=f'{dict["description"]}',
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                    f'{dict["file_path"]}': types.Schema(
                            type=types.Type.STRING,
                            description=f'{dict["file_path_description"]}',
                        ),
                    },
                ),
            )
    return schemas

def call_function(function_call_part, function_names, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    if function_call_part.name in function_names:
        function_result = function_names[function_call_part.name](working_directory=WORKING_DIRECTORY, **function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error":f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

