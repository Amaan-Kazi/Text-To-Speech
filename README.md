# Text To Speech
This python script uses the [VoiceRSS API](https://www.voicerss.org/api/) to convert your messages into voice.\
The voice is outputted using a Virtual Cable Audio so other applications can use it as input too

> [!Note]
> Get your own free [VoiceRSS API key](https://www.voicerss.org/login.aspx)\
> Download [VB Cable](https://vb-audio.com/Cable/) to output audio\
> Enable [listen to this device](https://www.cyberacoustics.com/how-to-get-microphone-playback-windows-10) in windows settings

## Features
Highly [customizable voice](https://www.voicerss.org/api/) using settings.json\
Moderate response times\
Can output in calls using the virtual cable audio microphone so others can hear it\
Can play your own sound files using play command\
Commands (prefix - $):
- $help - shows all commands and their description
- $settings - lists current settings from settings.json
- $play list - lists all playable files
- $play {file in special directory without .extension}
- $speed - Voice speed [-10 - 10]
- $language - Change language [english or hindi, more options manually in settings.json]
- $key - change the API Key

## How to use
Make sure that you have downloaded VB cable and enabled listen to this device\
Download TextToSpeech.zip from releases\
Unzip it and run TextToSpeech.exe\
Input the VoiceRSS API Key when asked for it\
You can change the key or other settings in settings.json or inbuilt commands\
Any messages you type will now be converted to voice and played\
To output this voice to any application just select "**Cable Output (VB-Audio Virtual Cable)**" as the input device

## How to build
```
pip install pygame
```
You can run this directly using python
or you can convert it to an executable .exe file using [pyinstaller](https://pyinstaller.org/en/stable/usage.html) as follows

```
pip install pyinstaller
```
```
pyinstaller -D -i "logo.ico" TextToSpeech.py
```
the executable will be created in dist folder
