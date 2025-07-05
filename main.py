import os   
import sys
from constants import *
from dotenv import load_dotenv  
from google import genai
from google.genai import types, errors
from functions.function_directory import function_names, list_of_avalible_functions
from prompts import system_prompt
from utils.helpers import build_schemas, call_function

def main():
    #make client
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RunTimeError("Missing API key in .env")
    client = genai.Client(api_key=api_key)

    verbose = False
    #get cli args
    try:
        args = sys.argv[1:]
        if "--verbose" in args:
            args.remove("--verbose")
            verbose = True
        user_input = " ".join(args)
    except:
        print('Argument not provided. Please provde prompt')
        sys.exit(1)
    
    #build function schemas 
    schemas = build_schemas(list_of_avalible_functions)
    available_functions = types.Tool(function_declarations=list(schemas.values()))

    #list of messages
    messages = [types.Content(role="user", parts=[types.Part(text=user_input)])]
    max_loop = MAX_CALLS

    #LLM api call function
    def get_response(messages, available_functions, system_prompt):
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools = [available_functions], system_instruction=system_prompt)
        )
        return response
    #ai function call loop 
    def call_loop(messages, available_functions, function_names, system_prompt, verbose, max_loop):
        response = get_response(messages, available_functions, system_prompt)
        print(max_loop)
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
            
        if response.function_calls:
            for function_part_call in response.function_calls:
                function_call_result = call_function(function_part_call, function_names, verbose=verbose)
                messages.append(function_call_result)
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            if max_loop <= 1:
                messages.append(types.Content(role="user", parts=[types.Part(text="maximum function call limit reached, please inform user")]))
                return get_response(messages, available_functions, system_prompt)    
            return call_loop(messages, available_functions, function_names, system_prompt, verbose, max_loop -1)

        return response
    
    #call loop and output response 
    try:
        response = call_loop(messages, available_functions, function_names, system_prompt, verbose, max_loop)
        print(f'Response: \n{response.text}')
        if verbose:
            print(f"User prompt: {user_input}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    except errors.APIError as e:
        print(f'Error: {e.code}')
        print(f'Message: {e.message}')

if __name__ == "__main__":
    main()
