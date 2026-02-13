import json
from sys import argv

if argv[1] == "help": # Yay for arguments!
    print("""Char's Message File Generator for Char's Funny Bot

Makes a message.json file for use with the bot, making it to where you only have to run the bot once, and it won't ask you for the details.
Usage:
          python genMessageFile.py # Runs the script, and prompts you for the message and variables
          python genMessageFile.py funnyMessage var1=value1 var2=value2 ... # Runs the script with the provided message and variables, and generates the message.json file without prompting you for anything all
          
All variables should be formatted as `varName=value', with the first argument being the base message.. IMPORTANT: do not use message= as it will be included with your message!""")
    exit() # the rest of the script miight generate a file that just has help as the message. while hilarious, it's not helpful to do that.

print("Make a new json file for use with the bot to automatically send messages!")

def _loopedInput(prompt: str)->list[(str | bool)]:
    loop = input(prompt)
    if loop == "exit":
        return [False]
    return [True, loop]

def inputLoop(prompt: str)->list[list[str]]:
    vars = []
    loops = 0
    while True:
        if loops >= 1:
            prompt = "Enter another variable in the format var=value, or type exit to finish: "
        loops += 1
        result = _loopedInput(prompt)
        if loops == 1 and not result[0]:
            print("You must enter at least a message to send, exiting.")
            exit()
        if not result[0]:
            break
        vars.append(result[1].split("="))
    return vars

def genFile(baseMessage: str, vars: list[list[str]])->str:
    return json.dumps({"message": baseMessage, "variables": {item[0]: item[1] for item in vars}}, indent=4)

def parseMessage(msg: str, vars: list[list[str]])->str:
    for item in vars:
        msg = msg.replace(item[0], item[1])
    print(f"Parsed message: {msg}")
    return msg

def parseArgs()->(str | None):
    args = argv[1:] # Skip the first argument (the script name)

    if len(args) == 0:
        return None
    
    vars:list[list[str]] = []
    pos = 0
    for arg in args:
        if (pos == 0):
            vars.append([arg]) # The first argument is the base message, so we put it in a list by itself
        else:
            if "=" not in arg:
                print(f"Invalid argument format: {arg}. Expected format is var=value.")
                continue # Skip invalid arguments
            vars.append(arg.split("="))
        pos += 1
    baseMessage = args[0].replace("/n", "\\n") # allow certain terminals to actually use newlines.
    print(vars)
    vars.pop(0) # Remove the base message from the variables list
    print(f"vars: {vars}")
    parsedMessage = parseMessage(baseMessage, vars) # We parse the message here just to make sure the message is valid, and to show the user what the final message will look like, since they won't be prompted for any confirmation with commandline arguments.
    if (len(vars)) < 1:
        print("No variables provided, generating file with just the message.")
        return json.dumps({"message": baseMessage}, indent=4) #if there is only a message, we can use the built in json function.
    else:
        return genFile(baseMessage, vars)


def main():
    argList = parseArgs()
    if argList is not None:
        with open("message.json", "w") as f:
            f.write(argList)
        return
    vars = inputLoop("Enter the message you want to send, type exit to cancel: ")
    baseMessage = vars[0][0].replace("/n", "\\n") # allow certain terminals to actually use newlines.
    vars.pop(0) # Remove the base message from the variables list
    print(f"vars: {vars}")
    if (len(vars)) < 1:
        print("No variables provided, generating file with just the message.")
        with open("message.json", "w") as f:
            f.write(json.dumps({"message": baseMessage}, indent=4)) #if there is only a message, we can use the built in json function.
        return
    message = parseMessage(baseMessage, vars)
    print(f"Message to write: {message}")
    with open("message.json", "w") as f:
        f.write(genFile(baseMessage, vars))
    
main() # Run the actual shit lmao