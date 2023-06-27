import subprocess


FILENAME = "outputs/test1.py"
Running = True

'''Writes code to a file'''
def write_code(code):
    print("Writing code")
    with open(FILENAME, 'w') as f:
        f.write(code)
    try:
        result = subprocess.run(['python3', FILENAME], capture_output=True, text=True)
        # Check the output and errors
        if result.stdout:
            return f'This was the output of the script: {result.stdout}'
        if result.stderr:
            return f'An error happened while executing the script: {result.stderr}'
    except Exception as e:
        return f"An exception occurred while executing the script: {e}"


#Pauses the program until the user provides input. This can be external testing, redesigning, etc
def get_user_input(message):
    user_input = input(message)
    print(user_input)
    return user_input

#Finishes execution, prevents further calls to the API
def finish_programming():
    global Running 
    Running = False
    return "The code is tested and ready to use!"

    
