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
  activity = discord.Game(name="!help for commands")
  await client.change_presence(status=discord.Status.online, activity=activity)


@client.event
async def on_message(message):
  # !HELP COMMAND
  if message.content.lower().startswith("!help"):
    em = discord.Embed(title="Commands")
    em.set_author(name="Wynny", icon_url=client.user.avatar.url)
    em.add_field(name="!help", value="Gets list of commands")
    em.add_field(name="!dog", value="Gets img of dog & fun fact")
    em.add_field(name="!cat", value="Gets img of cat & fun fact")
    em.add_field(name="!dadjoke", value="Tells a dad joke")
    em.add_field(name="!csjoke", value="Tells a CS joke")
    em.add_field(name="!fortune", value="Reads a fortune cookie")
    em.add_field(name="!poem", value="Reads a poems")
    em.add_field(name="!define [word]", value="Gets definitions of a word")
    em.add_field(name="!thesaurus [word]",
                 value="Gets synonyms & antonyms of a word")
    em.add_field(name="!translate [src_lang] [targ_lang] [txt]",
                 value="Translates text")
    em.add_field(name="excuse",
                 value="Gives an excuse when the word is mentioned")
    em.add_field(name="magic conch [question]",
                 value="Gives a yes/no response")
    em.add_field(name="wynny roast [name]", value="Roasts a given person")
    em.add_field(name="wynny what is this [img_link OR embedded_img]",
                 value="Guesses object in an image")

    await message.channel.send(embed=em)

  # !DOG COMMAND
  if message.content.lower().startswith("!dog"):
    reqImg = requests.get("https://dog.ceo/api/breeds/image/random")
    resImg = reqImg.json()

    reqFact = requests.get("https://dogapi.dog/api/v2/facts?limit=1")
    resFact = reqFact.json()

    em = discord.Embed(title='Doggo!', colour=discord.Colour.random())
    em.set_image(url=resImg['message'])
    em.set_footer(text="Fun Fact: " + resFact['data'][0]['attributes']['body'])

    await message.channel.send(embed=em)

  # !CAT COMMAND
  if message.content.lower().startswith("!cat"):
    pass
    reqImg = requests.get("https://api.thecatapi.com/v1/images/search")
    resImg = reqImg.json()

    reqFact = requests.get("https://meowfacts.herokuapp.com/")
    resFact = reqFact.json()

    em = discord.Embed(title='Kitty!', colour=discord.Colour.random())
    em.set_image(url=resImg[0]['url'])
    em.set_footer(text="Fun Fact: " + resFact['data'][0])

    await message.channel.send(embed=em)

  # !DADJOKE COMMAND
  if message.content.lower().startswith("!dadjoke"):
    req = requests.get("https://icanhazdadjoke.com/slack")
    res = req.json()

    await message.channel.send(":older_man: " +
                               res['attachments'][0]['fallback'])

  # !POEM COMMAND
  if message.content.lower().startswith("!poem"):
    lines = ['3', '4', '5', '6', '7']

    line = random.choice(lines)

    req = requests.get("https://poetrydb.org/linecount/" + line)
    res = req.json()

    resArr = []

    for i in range(0, len(res)):
      resArr.append(i)

    arr = random.choice(resArr)

    des = ""
    for string in res[arr]['lines']:
      des += string + "\n"

    em = discord.Embed(title=res[arr]['title'],
                       description=des,
                       colour=discord.Colour.pink())
    em.set_footer(text="By: " + res[arr]['author'])

    await message.channel.send(embed=em)

  # !DEFINE COMMAND
  if message.content.lower().startswith("!define"):
    if len(message.content) >= 8:
      word = message.content[8:]
      word = word.strip()

      req = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" +
                         word)
      res = req.json()

      des = ""
      try:
        for i in range(len(res[0]['meanings'])):
          des += "**" + str(i + 1) + ".** " + "`" + res[0]['meanings'][i][
            'partOfSpeech'] + "`: " + res[0]['meanings'][i]['definitions'][0][
              'definition'] + "\n"

        try:
          des += "\nPronunciation: " + res[0]['phonetics'][0]['audio']
          audio = ""
          for i in range(len(res[0]['phonetics'])):
            if res[0]['phonetics'][i]['audio'] != "":
              audio = res[0]['phonetics'][i]['audio']
          if audio == "":
            des += "`N/A`"
          else:
            des += audio
        except:
          pass

        em = discord.Embed(title=word.capitalize(),
                           description=des,
                           colour=discord.Colour.blue())

        await message.channel.send(embed=em)

      except:
        await message.channel.send(res['title'])

    else:
      await message.channel.send("No word provided.")

  # !THESAURUS COMMAND
  if message.content.lower().startswith("!thesaurus"):
    if len(message.content) >= 11:
      word = message.content[11:]
      word = word.strip()

      header = {"X-Api-Key": "m5zFoyKbvUw3cLwbVT3ilw==2roK5cJKsRxzCINB"}

      req = requests.get("https://api.api-ninjas.com/v1/thesaurus?word=" +
                         word,
                         headers=header)

      res = req.json()

      des = ""
      des += "**Synonyms**: "

      if len(res['synonyms']) == 0:
        des += "`None`\n\n"
      else:
        count_syn = 0
        for i in range(len(res['synonyms']) - 1):
          if res['synonyms'][i] != "":
            count_syn += 1
            des += "`" + res['synonyms'][i] + "`, "

        if res['synonyms'][-1] != "":
          count_syn += 1
          des += "`" + res['synonyms'][-1] + "`" + "\n\n"

        if count_syn == 0:
          des += "`None`\n\n"

      des += "**Antonyms**: "

      if len(res['antonyms']) == 0:
        des += "`None`"
      else:
        count_ant = 0
        for i in range(len(res['antonyms']) - 1):
          if res['antonyms'][i] != "":
            count_ant += 1
            des += "`" + res['antonyms'][i] + "`, "

        if res['antonyms'][-1] != "":
          count_ant += 1
          des += "`" + res['antonyms'][-1] + "`"

        if count_ant == 0:
          des += "`None`"

      em = discord.Embed(title=word.capitalize(),
                         description=des,
                         colour=discord.Colour.orange())

      await message.channel.send(embed=em)

    else:
      await message.channel.send("No word provided.")

  # MAGIC CONCH COMMAND
  if message.content.lower().startswith("magic conch"):
    replies = [
      "As I see it, yes", "It is certain", "It is decidedly so", "Most likely",
      "Outlook good", "Signs point to yes", "Without a doubt", "Yes",
      "Yes - definitely", "You may rely on it", "Don't count on it",
      "My reply is no", "My sources say no", "Outlook not so good",
      "Very doubtful", "No", "Try asking again", "I don't think so",
      "Maybe someday"
    ]

    reply = random.choice(replies)

    await message.channel.send(":shell: " + reply)

  # !FORTUNE COMMAND
  if message.content.lower().startswith("!fortune"):
    # OLD FORTUNE API CODE
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

  # WYNNY ROAST COMMAND
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

  # EXCUSE/EXCUSES COMMAND
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

  # !TRANSLATE-HELP COMMAND
  if message.content.lower().startswith("!translate-help"):
    await message.channel.send(
      "Format: `!translate [source_lang] [target_lang] [text]`")

  # !TRANSLATE COMMAND
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

  # !CSJOKE COMMAND
  if message.content.lower().startswith("!csjoke"):
    req1 = requests.get("https://v2.jokeapi.dev/joke/Programming?type=twopart")
    res1 = req1.json()

    req2 = requests.get("https://backend-omega-seven.vercel.app/api/getjoke")
    res2 = req2.json()

    joke1 = res1['setup'] + "\n\n" + "||" + res1['delivery'] + "||"
    joke2 = res2[0]['question'] + "\n\n" + "||" + res2[0]['punchline'] + "||"

    jokes = [joke1, joke2]

    joke = random.choice(jokes)

    await message.channel.send(joke)

  # WYNNY WHAT IS THIS COMMAND
  if message.content.lower().startswith("wynny what is this"):
    try:
      if len(message.attachments) != 0:
        url = message.attachments[0]
        res = requests.get(url)

        index = str(url).rindex('/')

        filename = str(url)[index + 1:]

        if "png" in filename.lower() or "jpg" in filename.lower(
        ) or "jpeg" in filename.lower():
          with open(filename, "wb") as f:
            f.write(res.content)

          header = {"X-Api-Key": "m5zFoyKbvUw3cLwbVT3ilw==2roK5cJKsRxzCINB"}

          image_file_descriptor = open(filename, 'rb')
          files = {'image': image_file_descriptor}

          req = requests.post("https://api.api-ninjas.com/v1/objectdetection",
                              headers=header,
                              files=files)
          res = req.json()

          if len(res) == 0:
            await message.channel.send("I have no idea what this is.")
          else:
            confidence = float(res[0]['confidence']) * 100
            await message.channel.send("I am " + str(round(confidence)) +
                                       "% sure this is a " + "**" +
                                       res[0]['label'] + "**.")
        else:
          await message.channel.send(
            "No valid image or image link found. I only accept `png`, `jpg`, or `jpeg`."
          )

      elif "http" in message.content.lower():
        index = message.content.index("http")
        url = message.content[index:]
        url = url.strip()
        res = requests.get(url)

        index2 = url.rindex('/')

        filename = url[index2 + 1:]

        if "png" in filename.lower() or "jpg" in filename.lower(
        ) or "jpeg" in filename.lower():
          with open(filename, "wb") as f:
            f.write(res.content)

          header = {"X-Api-Key": "m5zFoyKbvUw3cLwbVT3ilw==2roK5cJKsRxzCINB"}

          api_url = 'https://api.api-ninjas.com/v1/objectdetection'
          image_file_descriptor = open(filename, 'rb')
          files = {'image': image_file_descriptor}

          req = requests.post(api_url, headers=header, files=files)
          res = req.json()

          if len(res) == 0:
            await message.channel.send("I have no idea what this is.")
          else:
            if 'error' in str(res.keys()):
              await message.channel.send(res['error'])
            else:
              confidence = float(res[0]['confidence']) * 100
              await message.channel.send("I am " + str(round(confidence)) +
                                         "% sure this is a " + "**" +
                                         res[0]['label'] + "**.")
        else:
          await message.channel.send(
            "No valid image or image link found. I only accept `png`, `jpg`, or `jpeg`."
          )

      else:
        await message.channel.send(
          "No valid image or image link found. I only accept `png`, `jpg`, or `jpeg`."
        )

    except:
      await message.channel.send(
        "No valid image or image link found. I only accept `png`, `jpg`, or `jpeg`."
      )


keep_alive()

my_secret = os.environ['DISCORD_BOT_SECRET']

client.run(my_secret)
