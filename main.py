import requests
import os
import discord
from keep_alive import keep_alive
import random

intent = discord.Intents.all()
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
  print("Bot is up and running")


@client.event
async def on_message(message):
  if "!dog" in message.content.lower():
    reqImg = requests.get("https://dog.ceo/api/breeds/image/random")
    resImg = reqImg.json()

    reqFact = requests.get("https://dogapi.dog/api/v2/facts?limit=1")
    resFact = reqFact.json()

    em = discord.Embed(title='Doggo!', colour=discord.Colour.random())
    em.set_image(url=resImg['message'])
    em.set_footer(text="Fun Fact: " + resFact['data'][0]['attributes']['body'])

    await message.channel.send(embed=em)

  if "!cat" in message.content.lower():
    pass
    reqImg = requests.get("https://api.thecatapi.com/v1/images/search")
    resImg = reqImg.json()

    reqFact = requests.get("https://meowfacts.herokuapp.com/")
    resFact = reqFact.json()

    em = discord.Embed(title='Kitty!', colour=discord.Colour.random())
    em.set_image(url=resImg[0]['url'])
    em.set_footer(text="Fun Fact: " + resFact['data'][0])

    await message.channel.send(embed=em)

  if "!dadjoke" in message.content.lower():
    req = requests.get("https://icanhazdadjoke.com/slack")
    res = req.json()

    await message.channel.send(":older_man:: " +
                               res['attachments'][0]['fallback'])

  if "!fortune" in message.content.lower():
    # url = "https://fortune-cookie4.p.rapidapi.com/slack"

    # headers = {
    #   "X-RapidAPI-Key": "6304e998c4msh0a5d262ea2d4512p120770jsne3dba4274335",
    #   "X-RapidAPI-Host": "fortune-cookie4.p.rapidapi.com"
    # }

    # req = requests.get(url, headers=headers)
    # res = req.json()

    # em = discord.Embed(title='Fortune Cookie',
    #                    description=res['text'],
    #                    colour=discord.Colour.yellow())

    url2 = "https://fortune-cookie2.p.rapidapi.com/fortune"

    headers2 = {
      "X-RapidAPI-Key": "6304e998c4msh0a5d262ea2d4512p120770jsne3dba4274335",
      "X-RapidAPI-Host": "fortune-cookie2.p.rapidapi.com"
    }

    req2 = requests.get(url2, headers=headers2)
    res2 = req2.json()

    em2 = discord.Embed(title='Fortune Cookie',
                        description="Theme: " + res2['category'] + "\n\n" +
                        "🥠 your fortune reads: " + "'" + res2['answer'] + "'",
                        colour=discord.Colour.yellow())

    await message.channel.send(embed=em2)

  if message.content.lower().startswith("wynny roast"):
    name = message.content[11:]
    name = name.strip()
    name = name.lower()

    if name[-1] == 's':
      req = requests.get("https://insult.mattbas.org/api/en/insult.json?who=" +
                         name + "&plural=on")
    else:
      req = requests.get("https://insult.mattbas.org/api/en/insult.json?who=" +
                         name)

    res = req.json()

    await message.channel.send(res['insult'] +
                               " :face_with_symbols_over_mouth: ")

  if "excuse" in message.content.lower() or "excuses" in message.content.lower(
  ):
    if message.author != client.user:
      categories = [
        'family', 'office', 'children', 'college', 'party', 'funny',
        'unbelievable', 'developers'
      ]

      category = random.choice(categories)

      req = requests.get("https://excuser-three.vercel.app/v1/excuse/" +
                         category)
      res = req.json()

      await message.channel.send("Need an excuse? Try this:\n" + "`" +
                                 res[0]['excuse'] + "`")

  if message.content.lower().startswith("!translate-help"):
    await message.channel.send(
      "Format: `!translate [source_lang] [target_lang] [text]`")

  if message.content.lower().startswith(
      "!translate") and message.content.lower() != "!translate-help":
    if message.author != client.user:
      if len(message.content) < 17:
        await message.channel.send(
          "Invalid usage. Format: `!translate [source_lang] [target_lang] [text]`"
        )
      else:
        source = message.content[11:13]
        target = message.content[14:16]

        text = message.content[17:]
        text = text.strip()

        url = "https://text-translator2.p.rapidapi.com/translate"

        payload = {
          "source_language": source,
          "target_language": target,
          "text": text
        }
        headers = {
          "content-type": "application/x-www-form-urlencoded",
          "X-RapidAPI-Key":
          "6304e998c4msh0a5d262ea2d4512p120770jsne3dba4274335",
          "X-RapidAPI-Host": "text-translator2.p.rapidapi.com"
        }

        req = requests.post(url, data=payload, headers=headers)
        res = req.json()

        if res['status'] == "success":
          await message.channel.send(res['data']['translatedText'])
        else:
          await message.channel.send(
            "Invalid source or target language. List of supported languages: `https://rapidapi.com/dickyagustin/api/text-translator2/details`"
          )

  if "!csjoke" in message.content.lower():
    req1 = requests.get("https://v2.jokeapi.dev/joke/Programming?type=twopart")
    res1 = req1.json()

    req2 = requests.get("https://backend-omega-seven.vercel.app/api/getjoke")
    res2 = req2.json()

    joke1 = res1['setup'] + "\n\n" + "||" + res1['delivery'] + "||"
    joke2 = res2[0]['question'] + "\n\n" + "||" + res2[0]['punchline'] + "||"

    jokes = [joke1, joke2]

    joke = random.choice(jokes)

    await message.channel.send(joke)


keep_alive()

my_secret = os.environ['DISCORD_BOT_SECRET']

client.run(my_secret)
