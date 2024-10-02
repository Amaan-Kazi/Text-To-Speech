import http.client
import os
import json

import pygame
from pygame import mixer
import pygame._sdl2 as sdl2

## Variables ##

msg = "Hello World"
cmd = "none"
ttsCount = 0

settings = {
    "VoiceRSS_API_Key": "MISSING",
    "Speed": 0,
    "Language": "en-us",
    "Voice": "John"
}


## Functions ##

def updateSettingsJSON():
    with open('settings.json', 'w') as settings_json:
        json.dump(settings, settings_json, indent=4)
        settings_json.close()

def printSettings():
    for setting, value in settings.items():
        print(f"{setting}: {value}")

def encodeMessage(message: str):
    message = message.replace(" ", "%20") # Replace space with %20
    message = message.replace(",", "%2C") # Replace , with %2C
    return message

def playSound(file: str, volume: float):
    try:
        mixer.music.load(file)
        mixer.music.set_volume(volume)
        mixer.music.play()
    except:
        print("ERROR: Unable to play sound [Restart if problem persists]")

def getLanguage():
    if (input("Language: ").lower() == "Hindi"):
        settings["Language"] = "hi-in"
        settings["Voice"] = "Kabir"
    else:
        settings["Language"] = "en-us"
        settings["Voice"] = "John"
    updateSettingsJSON()

def getSpeed():
    settings["Speed"] = int(input("Speed [-10 to 10]: "))
    if (settings["Speed"] < -10): settings["Speed"] = -10
    elif (settings["Speed"] > 10): settings["Speed"] = 10
    updateSettingsJSON()

def getKey():
    settings["VoiceRSS_API_Key"] = input("VoiceRSS API Key: ")
    updateSettingsJSON()


## START OF PROGRAM ##

os.system("cls")
print("Starting Text To Speech")

# If settings.json doesnt exist, then create new and ask user for API key
if (os.path.isfile("settings.json") == False):
    print("Settings file not found, Creating settings.json")
    print("Enter API Key from VoiceRSS [https://www.voicerss.org/registration.aspx], you can change it through $key command")

    settings["VoiceRSS_API_Key"] = input("API Key: ")
    updateSettingsJSON()

with open('settings.json', "r") as settings_json:
    print("Loaded settings from settings.json \n")
    settings = json.load(settings_json)
    printSettings()
    settings_json.close()

# Check audio devices and make sure virtual CABLE microphone is installed 
pygame.init()
cableDeviceFound = False
audioDevices = sdl2.get_audio_device_names(True)
pygame.quit()

print("\nCurrently Found Audio Devices:")
print("\n".join(audioDevices))

for device in audioDevices:
    if (device == "CABLE Output (VB-Audio Virtual Cable)"):
        print("\nVirtual Cable Output Device Found \nMake sure to enable listen to this device [https://www.cyberacoustics.com/how-to-get-microphone-playback-windows-10]")
        cableDeviceFound = True
        break
if cableDeviceFound == False:
    print("\nPlease install Virtual Cable Output Device [https://vb-audio.com/Cable/] \nMake sure to enable listen to this device [https://www.cyberacoustics.com/how-to-get-microphone-playback-windows-10]")

# Clear Console
input("Press enter to continue")
os.system("cls")

# Empty the previous tts
os.system("rmdir tts /S /Q") # Delete entire tts directory
os.system("md tts") # Create new empty folder tts


## MAIN PROGRAM ##

print("Text To Speech Enabled")
print("Outputting to virtual CABLE microphone")

print("Messages/Commands[$help]: ")

mixer.init(devicename="CABLE Input (VB-Audio Virtual Cable)")

while (cmd.lower() != "stop"):
    cmd = "none"
    msg = input("> ")

    # If message is empty then skip and check message again
    if (msg == ""):
        continue

    # If message starts with $ then check for valid commands
    if (msg.startswith("$") == False):
        cmd = "None"
        file = "tts/" + "tts" + str(ttsCount) + ".wav"

        try:
            # API Connection
            connection = http.client.HTTPSConnection("api.voicerss.org")
            connection.request("GET", "/?key=" + str(settings["VoiceRSS_API_Key"]) + "&src=" + str(encodeMessage(msg)) + "&hl=" + str(settings["Language"]) + "&v=" + str(settings["Voice"]) + "&r=" + str(settings["Speed"]) + "&c=wav" + "&f=8khz_8bit_mono")

            response = connection.getresponse()
            ttsData = response.read()

            if (str(ttsData).startswith("b'ERROR:") == True):
                if (str(ttsData) == "b'ERROR: The API key is not available!'"):
                    print("ERROR: Missing or Invalid API Key, use $Key to update API Key [https://www.voicerss.org/registration.aspx] or change it in settings.json")
                else:
                    print(str(ttsData).replace("b'", "").replace("'", ""))
                continue
            
            with open(str(file), "wb") as ttsFile: # USED WB TO WRITE BINARY
                ttsFile.write(ttsData)
                ttsFile.close()
        except:
            print("ERROR: Unable to connect to VoiceRSS API [Make sure API Key is correct] or Corrupt sound file returned [Restart if problem persists]")
        else:
            playSound(file, 1.0)
            ttsCount += 1
    else:
        cmd = msg.replace("$", "").lower()

        if (cmd == "stop"):
            print("Stopped Text To Speech")
        elif (cmd == "help"):
            print("\n-----")
            print("Commands: ")
            print("$stop - Disable TTS and stop script")
            print("$settings - List current settings [manually configurable in settings.json]")
            print("$play list - List all files in the special directory")
            print("$play { filename (without .extenstion) } - Play the sound file through the mic")
            print("$speed - Change the TTS speed")
            print("$language - Change the TTS language (english: John, hindi: Kabir) [more options from VoiceRSS can be configured in settings.json]")
            print("$key - Change the VoiceRSS API Key")
            print("-----\n")
        elif(cmd == "settings"):
            print("\n-----")
            printSettings()
            print("-----\n")
        elif (cmd.startswith("play")):
            playFile = "special/" + cmd.replace("play ", "") + ".wav"

            if ("list" == cmd.replace("play ", "")):
                print("\nCurrently available special sound effects: ")
                
                if (os.path.isdir("special")):
                    for specialFile in os.listdir("special"):
                        print("- " + specialFile)
                else:
                    print("No special sound effects available")
                    os.mkdir("special")
            elif (os.path.isfile(playFile) == True):
                playSound(str(playFile), 1.0)
                print("Playing file: " + playFile)
            elif (os.path.isfile(playFile.replace("wav", "mp3")) == True):
                playSound(str(playFile.replace("wav", "mp3")), 1.0)
                print("Playing File: " + playFile.replace("wav", "mp3"))
            else:
                print("Invalid File, make sure your filename is all lowercase")
            print("\n")
        elif (cmd == "speed"):
            print("Currently: " + str(settings["Speed"]))
            getSpeed()
            print("\n")
        elif (cmd == "language"):
            print(f"Currently: {str(settings["Language"])}, {str(settings["Voice"])} [To get more options for voice and language, configure settings.json and write any language and voice from https://www.voicerss.org/api/#Voices, live test available on same website]")
            getLanguage()
            print("\n")
        elif (cmd == "key"):
            getKey()
            print("\n")
        else:
            print("Invalid Command\n")

