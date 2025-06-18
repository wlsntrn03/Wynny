import requests
import os
import discord
from webserver import keep_alive
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
    em.add_field(name="!help", value="Show commands")
    em.add_field(name="!dog", value="Dog + fact")
    em.add_field(name="!cat", value="Cat + fact")
    em.add_field(name="!meme", value="Random meme")
    em.add_field(name="!fortune", value="Fortune message")
    em.add_field(name="!poem", value="Read a poem")
    em.add_field(name="!excuse", value="Random excuse")
    em.add_field(name="!dadjoke", value="Dad joke")
    em.add_field(name="!csjoke", value="CS joke")
    em.add_field(name="!insult [name]", value="Playful insult")
    em.add_field(name="!8ball [question]", value="Yes/no answer")

    await message.channel.send(embed=em)

  # !DOG COMMAND
  if message.content.lower().startswith("!dog"):
    reqImg = requests.get("https://dog.ceo/api/breeds/image/random")
    resImg = reqImg.json()

    reqFact = requests.get("https://dogapi.dog/api/v2/facts?limit=1")
    resFact = reqFact.json()

    em = discord.Embed(title="Doggy! 🐶", colour=discord.Colour.random())
    em.set_image(url=resImg["message"])
    em.set_footer(text="Fun Fact: " + resFact["data"][0]["attributes"]["body"])

    await message.channel.send(embed=em)

  # !CAT COMMAND
  if message.content.lower().startswith("!cat"):
    pass
    reqImg = requests.get("https://api.thecatapi.com/v1/images/search")
    resImg = reqImg.json()

    reqFact = requests.get("https://meowfacts.herokuapp.com/")
    resFact = reqFact.json()

    em = discord.Embed(title="Kitty! 🐱", colour=discord.Colour.random())
    em.set_image(url=resImg[0]["url"])
    em.set_footer(text="Fun Fact: " + resFact["data"][0])

    await message.channel.send(embed=em)

  # !DADJOKE COMMAND
  if message.content.lower().startswith("!dadjoke"):
    req = requests.get("https://icanhazdadjoke.com/slack")
    res = req.json()

    await message.channel.send("👴 " + res["attachments"][0]["fallback"])

  # 8BALL COMMAND
  if message.content.lower().startswith("!8ball"):
    if len(message.content) > 7:
      replies = [
          "As I see it, yes",
          "It is certain",
          "It is decidedly so",
          "Most likely",
          "Outlook good",
          "Signs point to yes",
          "Without a doubt",
          "Yes",
          "Yes - definitely",
          "You may rely on it",
          "Don't count on it",
          "My reply is no",
          "My sources say no",
          "Outlook not so good",
          "Very doubtful",
          "No",
          "Try asking again",
          "I don't think so",
          "Maybe someday",
      ]
      reply = random.choice(replies)
    else:
      reply = "Please ask a question"

    await message.channel.send("🎱 " + reply)

  # !FORTUNE COMMAND
  if message.content.lower().startswith("!fortune"):

    req = requests.get("https://fortunecookies-i3p5.onrender.com/fortune/")
    res = req.json()

    luckyNums = ""
    for i in range(5):
      luckyNums += str(res["cookies"]["luckyNumbers"][i]) + ", "

    luckyNums += str(res["cookies"]["luckyNumbers"][5]) + "`"

    des = "🥠 " + res["cookies"]["fortune"] + "\n`Lucky Numbers: " + luckyNums

    em = discord.Embed(title="Fortune Cookie",
                       description=des,
                       colour=discord.Colour.yellow())

    await message.channel.send(embed=em)

  # !CSJOKE COMMAND
  if message.content.lower().startswith("!csjoke"):
    req1 = requests.get(
        "https://v2.jokeapi.dev/joke/Programming?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
    )
    res1 = req1.json()

    if res1["type"] == "single":
      joke = "🤖 " + res1["joke"]
    else:
      joke = "🤖 " + res1["setup"] + " ||" + res1["delivery"] + "||"

    await message.channel.send(joke)

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

    em = discord.Embed(title="📖 " + res[arr]['title'],
                       description=des,
                       colour=discord.Colour.pink())
    em.set_footer(text="— " + res[arr]['author'])

    await message.channel.send(embed=em)

  if message.content.lower().startswith(
      "!excuse") and message.author != client.user:
    categories = [
        'family', 'office', 'children', 'college', 'funny', 'unbelievable'
    ]

    category = random.choice(categories)

    req = requests.get("https://excuser-three.vercel.app/v1/excuse/" +
                       category)
    res = req.json()

    await message.channel.send("🤥 " + res[0]['excuse'])

  # !INSULT COMMAND
  if message.content.lower().startswith("!insult"):
    if len(message.content) > 8:
      name = message.content[7:]
      name = name.strip()

      # if name[-1] == 's':
      #   req = requests.get(
      #       "https://insult.mattbas.org/api/en/insult.json?who=" + name +
      #       "&plural=on")
      # else:
      req = requests.get("https://insult.mattbas.org/api/en/insult.json?who=" +
                         name)

      res = req.json()

      await message.channel.send("😡 " + res['insult'] + ".")
    else:
      await message.channel.send("Please provide a name")

  # !MEME COMMAND
  if message.content.lower().startswith("!meme"):
    req = requests.get("https://meme-api.com/gimme")
    res = req.json()

    await message.channel.send(res["url"])

keep_alive()

my_secret = os.environ["DISCORD_BOT_SECRET"]

client.run(my_secret)
