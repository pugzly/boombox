
<p align="center">
  <img src='https://raw.githubusercontent.com/pugzly/boombox/main/discord-boombox256.png' title="BoomBox">
</p>

# BoomBox
Minimal self-hosted Discord MP3 music streaming BOT for your own Discord server. 

Designed to run Linux systems. It may or may not run on Windows and Apple systems, addapting it to that is on your entirely.

Feature list:

'.play' - join 'General' voice channel and start streaming (Admin only). 

'.stop' - stop playing and disconnect from voice channel (Admin only)

'.skip' - skip to next random mp3 file (Admin only)

'.quit' - stop bot and exit progma (Creator only, if add your Discord ID to boombox.py)

## Requirements (on my Debian VPS at least):

```
sudo apt install ffmpeg
```
```
python3 -m pip install -U discord.py
```
```
python3 -m pip install -U pynacl
```

## Install & Run
1. Create Bot in Discord Developer Portal and get API TOKEN: https://discord.com/developers/applications

2. Clone repository
```
git clone https://github.com/pugzly/boombox
```
```
cd boombox
```
3. Edit file 'boombox.py' to add API TOKEN and change other preferences (feel free to change code to store token in env, encypted on blockchain, or under your mom's pillow)

5. Run
```
python3 boombox.py
```
Bonus: To keep it running even with terminal closed, start it with 'nohup'
```
nohup python3 boombox.py
```
