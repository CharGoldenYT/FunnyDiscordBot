import json, os

print("Reading the message from message.json")

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

def read_message()->str:
    if os.path.exists("message.json"):
        with open("message.json", "r") as f:
            data = json.load(f)
            vars = [[key, value] for key, value in data.get("variables", {}).items()]
            return parseMessage(data.get("message", "No message found in message.json"), vars)
    else:
        print("message.json not found!")
        vars = inputLoop("Enter the message you want to send, type exit to cancel: ")
        baseMessage = vars[0][0]
        vars.pop(0) # Remove the base message from the variables list
        return parseMessage(baseMessage, vars)


def parseMessage(msg: str, vars: list[list[str]])->str:
    for item in vars:
        msg = msg.replace(item[0], item[1])
    return msg

print("Setting up the bot")

botkey:str = ""
channelID:int = 0

file = open("botkey.txt", "r")
botkey = file.read()
file.close()
file = open("channelID.txt", "r")
channelID = int(file.read())
file.close()

print("Starting bot, then sending the message defined with delay")

msg = read_message().replace("<br>", "\n") # Allow for newlines in the message, since json doesn't allow for actual newlines in strings, they have to be escaped with \n, so we replace those with actual newlines before sending the message.
print(f"Message to send: {msg}")
from bot import DiscordBot
bot = DiscordBot(botkey, msg, channelID)
bot.run()