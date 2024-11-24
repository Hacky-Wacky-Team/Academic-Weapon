#Made by Jeffery, Jonathan, and Eric <3

#all the imports
import discord
import os
from discord.ext import commands
from discord.commands import Option
import asyncio
from discord.ui import Button, Select, View
import random


#this is for slash commands (application commands)
bot = commands.Bot(command_prefix="!")
client = discord.Client()
guildID = 0

@client.event
async def on_message(message):
 if message.author == client.user:
    print(f"Guild id {message.guild.id}")
    guildID = message.guild.id

reminders = {}

#this tells us when the bot comes online
@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online,activity=discord.Activity(type=discord.ActivityType.playing,name="Training"))
  print("Bot is Up and Ready!")

#reminder slash command
@bot.slash_command(guild_ids = [1165307327755341877], description = "Create your own reminders!")
async def reminder(ctx,
  days:Option(int,"How many days until I remind you?",default = 0, require = False),
  hours:Option(int,"How many hours until I remind you?", default = 0, require = False),
  minutes:Option(int,"How many minutes until I remind you?",default = 0, require = False),
  seconds:Option(int,"How many minutes until I remind you?",default = 0, require = False),
  task:Option(str,"What is the purpose of the reminder?", default  = "Untitled", require = False)
  ):
  #creates a unique reminder ID
  reminderID = len(reminders) + 1

  #stores the reminder IDs
  reminders[reminderID] = {
      'user_id': ctx.author.id,
      'task': task,
      'days': days,
      'hours': hours,
      'minutes': minutes,
      'seconds': seconds,
      'cancel_button': None
  }
  #The cancel button
  button = Button(label="Cancel the Reminder", style=discord.ButtonStyle.red, emoji="❌")
  async def button_callback(interaction):
    #retrieve the reminder from the dictionary
    reminder = reminders.get(reminderID)
    if reminder and interaction.user.id == reminder['user_id']:
        reminders.pop(reminderID)  # Remove the reminder
        await interaction.response.send_message(f"Reminder '{reminder['task']}' has been canceled. ⏰")
  button.callback = button_callback

  #view
  view = View()
  view.add_item(button)
  
  #the embed
  embedRemind = discord.Embed(title="Reminder", description=f"Your reminder to {task} has been set! \n{days} Days \n{hours} Hours \n{minutes} Minutes \n{seconds} Seconds", color=0x206694)
  await ctx.respond(embed=embedRemind, view=view)
  await asyncio.sleep((days*60*60*24) + (hours*60*60) + (minutes*60) + (seconds))
  
  #Check if the reminder still exists (not canceled)
  if reminders.get(reminderID):
      reminders.pop(reminderID)  #Remove the reminder
      await ctx.respond(f"{ctx.author.mention}: Reminder to {task}")


#Select Role
@bot.slash_command(guild_ids = [1165307327755341877], description = "Assign yourself roles!")
async def role(ctx):
    userID = ctx.author.id
    select = Select(
        min_values = 1, # Minimum number of options that must be chosen
        max_values = 1, # Maximum number of options that can be chosen
        #options for the selcect drop down
        placeholder="Choose a role!" ,options=[
            discord.SelectOption(
              label="Elementary School", 
              emoji="👶", 
              description="Gr 1-6!"
            ),
            discord.SelectOption(
              label="Middle School", 
              emoji="👦", 
              description="Gr 7-8"
            ),
            discord.SelectOption(
              label="High School", 
              emoji="🧔‍♂️", 
              description="Gr 9-12"
            ),
            discord.SelectOption(
              label="Post Secondary", 
              emoji="👴", 
              description="Uni/College"
            ),
            discord.SelectOption(
              label="Other", 
              emoji="💀", 
              description="Other"
            ),
        ],
    )

    #when the user interacts with the select menu
    async def my_callback(interaction):
        if interaction.user.id == userID:
            selected_option = interaction.data['values'][0]

            #assigns each select option to a discord role ID
            role_mapping = {
                "Elementary School": 1165406856156545055,
                "Middle School": 1165406932157333547,
                "High School": 1165406993968808081,
                "Post Secondary": 1165407043868438589,
                "Other": 1165407092832747520,
            }

            #gets the role ID to assign
            role_id = role_mapping.get(selected_option)

            #gives the role to the user
            role_to_assign = discord.utils.get(ctx.guild.roles, id=role_id)
            await interaction.user.add_roles(role_to_assign)

            await interaction.response.send_message(f"You chose: {selected_option}")

    select.callback = my_callback
    view = View()
    view.add_item(select)
    await ctx.respond("**Choose a role!**", view=view)

@bot.slash_command(guild_ids = [1165307327755341877], description = "List of the commands")
async def help(ctx):
  #the buttons
  button1 = Button(style=discord.ButtonStyle.grey, emoji="1️⃣")
  button2 = Button(style=discord.ButtonStyle.grey, emoji="2️⃣")
  button3 = Button(style=discord.ButtonStyle.grey, emoji="3️⃣")

  #views
  view = View()
  view.add_item(button1)
  view.add_item(button2)
  view.add_item(button3)
  
  #the embed commands for the general commands tab
  embedHelp1 = discord.Embed(
    title="General Commands", 
    description=f"⏰ **/remind** - Sets a Reminder (days, hours, mins, secs) \n⭐ **/motivate** - Gives a Quote \n😎 **/role** - Assign Yourself a Role \n📚 **/resources** - online help on your subjects \n💯 **/calculate_grade** - calculates your average grade",  
    color=0x206694
  )
  embedHelp1.add_field(name="", value="")
  embedHelp1.set_footer(text="page 1/3")
  embedHelp1.set_image(url="https://cdn.discordapp.com/attachments/1165680842182496317/1165680922738303006/Add_heading_1..png?ex=6547bbf5&is=653546f5&hm=cecb1d851ac87a08c1614d46c23fc7fe4c68361b86109bef8050c037c64f6dac&")

  #the embed commands for the todo lists tab
  embedHelp2 = discord.Embed(
    title="Todo List | Commands", 
    description=f"📋 **/view_todo_list** - View your todo list \n📝 **/add_todo** - Add a task to your todo list\n🗑️ **/clear_todo_list** - Clear all tasks in your todo list\n❌ **/remove_todo** - Remove a task from your todo list\n✅ **/mark_todo_done** - Mark a task as done", 
    color=0x206694
  )
  embedHelp2.add_field(name="", value="")
  embedHelp2.set_footer(text="page 2/3")
  embedHelp2.set_image(url="https://www.salesforce.com/content/dam/blogs/ca/Infographics/how-to-get-your-to-do-list-done-faster-open-graph.jpg")

  #the embed commands for the timetable tab
  embedHelp3 = discord.Embed(
    title="Timetable | Commands", 
    description=f"📅 **/view_timetable** - View your timetable\n📝 **/add_timetable_entry** - Add a course to your timetable\n🗑️ **/clear_timetable** - Clear your timetable \n❌ **/remove_timetable_entry** - Remove a course from your timetable", 
    color=0x206694
  )
  embedHelp3.add_field(name="", value="")
  embedHelp3.set_footer(text="page 3/3")
  embedHelp3.set_image(url="https://cdn.discordapp.com/attachments/1165680842182496317/1165680949795766322/creative-timetable-made-kids-template_23-2148233202.png?ex=6547bbfb&is=653546fb&hm=f090b462be4eb0e487e770ab953854621286cbd10c8cd41584382c988ebbbd69&")

  #default view when the /help command is used
  interaction = await ctx.respond(embed=embedHelp1, view=view)

  #edits the embed messages when button is clicked
  async def button1_callback(interaction):
    interaction = await interaction.response.edit_message(embed=embedHelp1, view=view)
  button1.callback = button1_callback
  
  async def button2_callback(interaction):
    interaction = await interaction.response.edit_message(embed=embedHelp2, view=view)
  button2.callback = button2_callback

  async def button3_callback(interaction):
    interaction = await interaction.response.edit_message(embed=embedHelp3, view=view)
  button3.callback = button3_callback
  
#Quotes List
quotes = [
"\"All our dreams can come true, if we have the courage to pursue them.\" — Walt Disney",
"\"The secret of getting ahead is getting started.\" — Mark Twain",
"\“I’ve missed more than 9,000 shots in my career. I’ve lost almost 300 games. 26 times I’ve been trusted to take the game winning shot and missed. I’ve failed over and over and over again in my life, and that is why I succeed.\” — Michael Jordan", 
"\“Only the paranoid survive.\” — Andy Grove",
"\"It’s hard to beat a person who never gives up.\” — Babe Ruth",
"\"Everything you can imagine is real.\”― Pablo Picasso",
"\"Hold the vision, trust the process.\” — Eric", 
"\"Don’t limit yourself. Many people limit themselves to what they think they can do. You can go as far as your mind lets you. What you believe, remember, you can achieve.\” — Mary Kay Ash",
"\"You're alive, motivated and ready to slay the day #MONSLAY.\" — Jonathan", 
"\"Do what you feel in your heart to be right―for you’ll be criticized anyway.\” ― Eleanor Roosevelt", 
"\"The hard days are what make you stronger.\” ― Aly Raisman", 
"\"If you believe it’ll work out, you’ll see opportunities. If you don’t believe it’ll work out, you’ll see obstacles.” ― Wayne Dyer",
"\"You can waste your lives drawing lines. Or you can live your life crossing them.\” ― Shonda Rhimes",
"\"In a gentle way, you can shake the world.\” ― Mahatma Gandhi",
"\"Work hard in silence, let your success be the noise.\” ― Frank Ocean",
"\"Hard work beats talent when talent doesn’t work hard.\” ― Tim Notke",
"\"If everything seems to be under control, you’re not going fast enough.\” ― Mario Andretti"
]

#Command to generate a quote
@bot.slash_command(guild_ids = [1165307327755341877], description = "Gives you a boost of motivation!")
async def motivate(ctx):
  quote = random.choice(quotes)
  embedQuote = discord.Embed(title=quote, color=0x206694)
  await ctx.respond(embed=embedQuote)

# Resources
studyResources = "Math: https://www.khanacademy.org \n Language: https://www.duolingo.com \n Speaches: https://ed.ted.com \n Accessible Videos: https://www.youtube.com \n Music: https://musictheory.net"

studyVideos = "https://www.youtube.com/watch?v=4RkWiNO3iq8 \n https://www.youtube.com/watch?v=TjPFZaMe2yw \n https://www.youtube.com/watch?v=lEHt8m61hSg \n https://www.youtube.com/watch?v=IDB_3S1ezsc \n https://www.youtube.com/watch?v=76yqErAib5g"

mentalHealthResources = "https://www.youtube.com/watch?v=oxx564hMBUI \n https://youtu.be/RUrpw8RLEDI?si=sLKKFh2FjRb7WMIV \n https://youtu.be/SwdbL0LAZGY?si=SDm5se6rWDQxlFwv \n https://www.youtube.com/watch?v=IwR3TljxVuA \n https://www.youtube.com/watch?v=-OAjfrhuwRk"

#Resources slash command
@bot.slash_command(guild_ids=[1165307327755341877], description="Here are some resources to help you study")
async def resources(ctx):
  #Buttons
  study_resources_button = Button(
    label="Study Resources", 
    style=discord.ButtonStyle.secondary
  )
  study_videos_button = Button(
    label="Study Videos", 
    style=discord.ButtonStyle.secondary
  )
  mental_health_resources_button = Button(
    label="Mental Health Resources", 
    style=discord.ButtonStyle.secondary
  )

  #view
  view = View()
  view.add_item(study_resources_button)
  view.add_item(study_videos_button)
  view.add_item(mental_health_resources_button)

  #embed for the Study Resources tab
  embedStudyResources = discord.Embed(
    title="Study Resources", 
    description=studyResources, 
    color=0x206694
  )
  embedStudyResources.add_field(name="", value="")
  embedStudyResources.set_image(url="https://th.bing.com/th/id/R.a54aa6cae2fe89959677adc6591c5603?rik=q0JLPSYLJy4%2fvg&pid=ImgRaw&r=0")

  #embed for the Study Videos tab
  embedStudyVideos = discord.Embed(
    title="Study Videos", 
    description=studyVideos, 
    color=0x206694
  )
  embedStudyVideos.add_field(name="", value="")
  embedStudyVideos.set_image(url="https://img.freepik.com/free-photo/back-school-education-banner-background_8087-1192.jpg?size=626&ext=jpg")

  #embed for the Mental Health Resources tab
  embedMentalHealthResources = discord.Embed(
    title="Mental Health Resources", 
    description=mentalHealthResources, 
    color=0x206694
  )
  embedMentalHealthResources.add_field(name="", value="")
  embedMentalHealthResources.set_image(url="https://cdn.discordapp.com/attachments/1165680842182496317/1165681049427247274/Mental_Health_Facebook_Cover.jpg?ex=6547bc13&is=65354713&hm=461a21a265630d059994a450047a36efcd6dc931a296fd8837d957717f0e1afe&")

  #default view when the /resources command is used
  interaction = await ctx.respond(embed=embedStudyResources, view=view)

  #button interactions 
  async def study_resources_button_callback(interaction):
    interaction = await interaction.response.edit_message(embed=embedStudyResources, view=view)
  study_resources_button.callback = study_resources_button_callback
  async def study_videos_button_callback(interaction):
    interaction = await interaction.response.edit_message(embed=embedStudyVideos, view=view)
  study_videos_button.callback = study_videos_button_callback
  async def mental_health_resources_button_callback(interaction):
    interaction = await interaction.response.edit_message(embed=embedMentalHealthResources, view=view)
  mental_health_resources_button.callback = mental_health_resources_button_callback


#Grade calculate slash command
@bot.slash_command(guild_ids = [1165307327755341877], description = "Calculates your average grade")
async def calculate_grade(ctx,
  marks1:Option(int,"List one of your marks", default = 0, require = False),
  marks2:Option(int,"List one of your marks", default = 0, require = False),
  marks3:Option(int,"List one of your marks", default = 0, require = False),
  marks4:Option(int,"List one of your marks", default = 0, require = False),
  marks5:Option(int,"List one of your marks", default = 0, require = False),
  marks6:Option(int,"List one of your marks", default = 0, require = False),
  marks7:Option(int,"List one of your marks", default = 0, require = False),
  marks8:Option(int,"List one of your marks", default = 0, require = False),
  marks9:Option(int,"List one of your marks", default = 0, require = False),
  marks10:Option(int,"List one of your marks", default = 0, require = False),
  ):
  
  #Calculate the number of marks provided by the user.
  number_of_marks = len([mark for mark in [marks1, marks2, marks3, marks4, marks5, marks6, marks7, marks8, marks9, marks10] if mark > 0])

  #Checks if there is at least 1 mark
  if number_of_marks == 0:
    await ctx.respond("Please provide at least one mark.")
    return
  
  #Calculate the average grade.
  average_grade = (sum([marks1, marks2, marks3, marks4, marks5, marks6, marks7, marks8, marks9, marks10]) / number_of_marks)
  average_grade = round(average_grade, 2)
  
  embedCalculateGrade = discord.Embed(
    title="Calculate Grade", 
    description=f"Your average grade is: {average_grade}", 
    color=0x206694
  )
  await ctx.respond(embed=embedCalculateGrade)

#Todo list
userTodoLists = {}

#Command to add a task to the user's todo list
@bot.slash_command(guild_ids=[1165307327755341877], description="Add a task to your todo list")
async def add_todo(ctx, task: str):
    userID = ctx.author.id

    #Check if the user has an existing todo list, and create one if not
    if userID not in userTodoLists:
      userTodoLists[userID] = []

    userTodoLists[userID].append(task)
    await ctx.respond(f"Task '{task}' added to your todo list.")

#Command to remove a task from the user's todo list
@bot.slash_command(guild_ids=[1165307327755341877], description="Remove a task from your todo list")
async def remove_todo(ctx, task_number: int):
  userID = ctx.author.id
  if userID in userTodoLists:
    userTodoList = userTodoLists[userID]
    if 1 <= task_number <= len(userTodoList):
      removed_task = userTodoList.pop(task_number - 1)
      await ctx.respond(f"Removed task #{task_number}: '{removed_task}' from your todo list.")
    else:
      await ctx.respond("Invalid task number. Please provide a valid task number.")
  else:
    await ctx.respond("You don't have any tasks in your todo list.")

#Command to clear the user's todo list
@bot.slash_command(guild_ids=[1165307327755341877], description="Clear all tasks in your todo list")
async def clear_todo_list(ctx):
  userID = ctx.author.id
  if userID in userTodoLists:
    userTodoList = userTodoLists[userID]
    if not userTodoList:
      await ctx.respond("Your todo list is already empty.")
    else:
      userTodoList.clear()
      await ctx.respond("Your todo list has been cleared.")
  else:
    await ctx.respond("You don't have a todo list")

#Command to mark a task as done
@bot.slash_command(guild_ids=[1165307327755341877], description="Mark a task as done")
async def mark_todo_done(ctx, task_number: int):
  userID = ctx.author.id
  if userID in userTodoLists:
    userTodoList = userTodoLists[userID]
    if 1 <= task_number <= len(userTodoList):
      userTodoList[task_number - 1] = userTodoList[task_number - 1] + " ✅"
      await ctx.respond(f"Task #{task_number} has been marked as done.")
    else:
      await ctx.respond("Invalid task number. Please provide a valid task number.")
  else:
    await ctx.respond("You don't have any tasks in your todo list.")
    
#Command to view the user's todo list
@bot.slash_command(guild_ids=[1165307327755341877], description="View your todo list")
async def view_todo_list(ctx):
  userID = ctx.author.id
  userTodoList = userTodoLists.get(userID, [])

  #Create the todo list embed
  embedTodo = discord.Embed(
    title="Your Todo List", 
    description="", 
    color=0x206694
  )
  embedTodo.set_image(url="https://cdn.discordapp.com/attachments/1165680842182496317/1165681063088107530/6-things-to-do-list.png?ex=6547bc16&is=65354716&hm=b85719acd740fa95f9a4bb5caed51399dabe79aad88e9c8a81f4c92ee62fd1fd&")

  if not userTodoList:
    embedTodo.description = "Your todo list is empty."
  else:
    for i, task in enumerate(userTodoList, start=1):
      formattedTask = f"{i}. {task}\n"
      embedTodo.description += formattedTask
  await ctx.respond(embed=embedTodo)

#Timetable 
timeTable = {}

#Command to add a timetable entry
@bot.slash_command(guild_ids=[1165307327755341877], description="Add a course to your timetable")
async def add_timetable_entry(ctx, course_name: str, course_time: str, course_room: str):
  userID = ctx.author.id
  
  #Check if the user has an existing timetable, and create one if not
  if userID not in timeTable:
    timeTable[userID] = []
  #Check if the course already exists in the timetable
  for entry in timeTable[userID]:
    if entry[0] == course_name:
      await ctx.respond("This course already exists in your timetable.")
  #Add the course to the timetable
  timeTable[userID].append([course_name, course_time, course_room])
  await ctx.respond(f"Course '{course_name}' has been added to your timetable.")

#Command to view timetable
@bot.slash_command(guild_ids=[1165307327755341877], description="View your timetable")
async def view_timetable(ctx):
  userID = ctx.author.id
  userTimeTable = timeTable.get(userID, [])
  #Create the timetable embed
  embedTimeTable = discord.Embed(
    title="Your Timetable", 
    description="", 
    color=0x206694)
  if not userTimeTable:
    embedTimeTable.description = "Your timetable is empty."
  else:
    #Add the timetable entries to the embed
    for i, entry in enumerate(userTimeTable, start=1):
      formattedEntry = f"{i}. {entry[0]}: {entry[1]} in room {entry[2]}\n"
      embedTimeTable.description += formattedEntry
  await ctx.respond(embed=embedTimeTable)

#Command to remove a timetable entry
@bot.slash_command(guild_ids=[1165307327755341877], description="Remove a course from your timetable")
async def remove_timetable_entry(ctx, course_name: str):
  userID = ctx.author.id
  removed = False
  if userID in timeTable:
    userTimeTable = timeTable[userID]
    for entry in userTimeTable:
      if course_name in entry:
        userTimeTable.remove(entry)
        removed = True
        break
    if removed:
      await ctx.respond(f"Course '{course_name}' has been removed from you timetable.")
    else:
      await ctx.respond("This course does not exist in your timetable.")
  else:
    await ctx.respond("You don't have a timetable.")

#Command to clear timetable
@bot.slash_command(guild_ids=[1165307327755341877], description="Clear your timetable")
async def clear_timetable(ctx):
  userID = ctx.author.id
  if userID in timeTable:
    timeTable[userID] = []
    await ctx.respond("Your timetable has been cleared.")
  else:
    await ctx.respond("You don't have a timetable.")
    
my_secret = os.environ['SECRET_KEY']
bot.run(my_secret)