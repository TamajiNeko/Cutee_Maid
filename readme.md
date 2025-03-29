# Cuteee Maid Bot~♡ 

She's a Discord Chat Bot that use Generative AI to response. (˶ᵔ ᵕ ᵔ˶)

you can try it on my [Discord Server](https://discord.gg/xbkDcayn6T) ⸜(｡˃ ᵕ ˂ )⸝♡. or you can invite her to your server

`Note` : Please read Discord Documentation If you need to try her

## Installation

After clone this project you can delete **README.MD**. And Install [Discord](https://discordpy.readthedocs.io/en/stable/) and [Requests](https://pypi.org/project/requests/)

Discord (˶˃ ᵕ ˂˶) .ᐟ.ᐟ
```bash
py -m pip install discord
```

Requests
```bash
py -m pip install requests
```

You can Install any Database, but you need to edit many parts of **model.py**. ૮ ˶ᵔ ᵕ ᵔ˶ ა

## Usage (￣▽￣*)ゞ

After done all [in Installation](#Installation) you have to config Discord Token ([You can read this documentation how to get](https://discord.com/developers/docs/topics/oauth2)) and your any **LM or LLM API**. in case i use [openchat-3.6-8b-20240522](https://huggingface.co/lmstudio-community/openchat-3.6-8b-20240522-GGUF) with [LM Studio](https://lmstudio.ai) *(Local server, Only for test)* (˶˃⤙˂˶)

**model.py** line 149. Change it to your Discord Token
```python
bot.run("YOUR TOKEN")
```

**model.py** line 59. Change it to your API URL
```python
API_URL = "YOUR API"
```

### All done! (˶ᵔ ᵕ ᵔ˶)