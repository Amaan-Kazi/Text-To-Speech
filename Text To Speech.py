import http.client
import os
from pygame import mixer
import json
import pyaudio

settings = {
    "VoiceRSS_API_Key": "MISSING",
    "Speed": 0,
    "Language": "en-us",
    "Voice": "John"
}

# Variables
msg = "Hello World"
cmd = "none"
ttsCount = 0

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
    if (input("Language: ") == "Hindi"):
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


os.system("cls")
print("Starting Text To Speech")

if (os.path.isfile("settings.json") == False):
    print("Settings file not found, Creating settings.json")
    print("Enter API Key from VoiceRSS [https://www.voicerss.org/registration.aspx], you can change it through $Settings command")

    settings["VoiceRSS_API_Key"] = input("API Key: ")
    updateSettingsJSON()

with open('settings.json', "r") as settings_json:
    print("Loaded settings from settings.json \n")
    settings = json.load(settings_json)
    printSettings()
    settings_json.close()

# Check if Virtual Cable is installed
p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
CableInstalled = False

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        #print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        if (p.get_device_info_by_host_api_device_index(0, i).get('name').startswith("CABLE") == True):
            CableInstalled = True
            break
if (CableInstalled == True):
    print("\nVirtual Cable Output Device Found \nMake sure to enable listen to this device [https://www.cyberacoustics.com/how-to-get-microphone-playback-windows-10]")
else:
    print("\nPlease install Virtual Cable Output Device [https://vb-audio.com/Cable/] \nMake sure to enable listen to this device [https://www.cyberacoustics.com/how-to-get-microphone-playback-windows-10]")


# Clear Console
input("Press enter to continue")
os.system("cls")

# Empty the previous tts
os.system("rmdir tts /S /Q") # Delete entire tts directory
os.system("md tts") # Create new empty folder tts

print("Text To Speech Enabled")
print("Outputting to virtual microphone")

# API Connection
connection = http.client.HTTPSConnection("api.voicerss.org")

print("Messages: ")

#mixer.init(devicename="Headphones (Lenovo thinkplus-LP40 Pro)")
mixer.init(devicename="CABLE Input (VB-Audio Virtual Cable)")

while (cmd.lower() != "stop"):
    cmd = "none"
    msg = input("> ")

    # If message is empty then skip and check message again
    if (msg == ""):
        continue

    if (msg.startswith("$") == False):
        cmd = "None"
        file = "tts/" + "tts" + str(ttsCount) + ".wav"

        try:
            connection.request("GET", "/?key=" + str(settings["VoiceRSS_API_Key"]) + "&src=" + str(encodeMessage(msg)) + "&hl=" + str(settings["Language"]) + "&v=" + str(settings["Voice"]) + "&r=" + str(settings["Speed"]) + "&c=wav" + "&f=8khz_8bit_mono")
            response = connection.getresponse()
            ttsData = response.read()
            
            with open(str(file), "wb") as ttsFile: # USED WB TO WRITE BINARY
                ttsFile.write(ttsData)
                ttsFile.close()
        except:
            print("Error: Unable to connect to VoiceRSS API [Make sure API Key is correct] or Corrupt sound file returned [Restart if problem persists]")
        else:
            playSound(file, 1.0)
            ttsCount += 1
    else:
        cmd = msg.replace("$", "")

        if (cmd.lower() == "stop"):
            print("Stopped TTS")
        elif (cmd.lower() == "help"):
            print("")
        elif(cmd.lower() == "settings"):
            printSettings()
        elif (cmd.lower().startswith("play")):
            playFile = "special/" + cmd.replace("Play ", "") + ".wav"

            if ("list" == cmd.replace("Play ", "")):
                print("Currently available special sound effects: ")

                for specialFile in os.listdir("special"):
                    print("- " + specialFile)
            elif (os.path.isfile(playFile) == True):
                playSound(str(playFile), 1.0)
                print("Playing file: " + playFile)
            elif (os.path.isfile(playFile.replace("wav", "mp3")) == True):
                playSound(str(playFile.replace("wav", "mp3")), 1.0)
                print("Playing File: " + playFile.replace("wav", "mp3"))
            else:
                print("Invalid File")
        elif (cmd.lower() == "speed"):
            print("Currently: " + str(settings["Speed"]))
            getSpeed()
        elif (cmd.lower() == "language"):
            getLanguage()
        elif (cmd.lower() == "key"):
            getKey()
        else:
            print("Invalid Command")
