import os
import subprocess
from CoreBot import *


def write_code(file_name, input):

    start_index = input.find("```python") + len("```python")  # Include the newline after the marker
    end_index = input.rfind("```")  # Find the last occurrence of the backticks

    # Slice the string to only include the code
    code = input[start_index:end_index]

    with open(file_name, 'w') as f:
        f.write(
        code
            )
    try:
        result = subprocess.run(['python3', file_name], capture_output=True, text=True)
        # Check the output and errors
        if result.stdout:
            return f'This was printed: {result.stdout}'
        if result.stderr:
            return f'An error happened: {result.stderr}'
    except Exception as e:
        return f"An error occurred while executing the script: {e}"


#Pauses the program until the user provides input. This can be external testing, redesigning, etc
def get_user_input():
    pass

#Finishes execution, prevents further calls to the API
def finish_programming():
    pass

#Full iterative development
def iterative_development(design_goal, file_name, label, max_itr=3):
    #initialize AI and prompt
    AI = AI_Programmer(design_goal=design_goal)
    new_code = AI.generate_response(label, "Write the python code for the program. Your output should only include code and comments, anything else will interfer with executing the code. DO NOT SAY ANYTHING BUT CODE.")

    for i in range(max_itr):
        output = write_code(file_name, new_code)
        print(output)
        new_code = AI.generate_response(label, output)
        if "I am done coding" in new_code:
            print("Exited successfully")
            break
    AI.write_memory(label=label)


design_goal = "Your purpose is to write code for a pytorch neural network, including a training loop."

iterative_development(design_goal, "test1.py", label="test1")

    
