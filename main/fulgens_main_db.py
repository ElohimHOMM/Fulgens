import mysql.connector as msc
import os
from dotenv import load_dotenv

load_dotenv()

mydb = msc.connect(
    host = os.getenv("DATABASE_HOST"),
    user = os.getenv("DATABASE_USERNAME"),
    password = os.getenv("DATABASE_PASSWORD"),
    database = os.getenv("DATABASE_NAME")
)
mycursor = mydb.cursor()

# Ban Channels

def get_ban_channel_by_guild_id(guild_id):
    sql = f"SELECT * FROM BAN_CHANNEL WHERE GUILD_ID = '{guild_id}'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    res = list()
    for x in myresult:
        res.append(x[0])
    return tuple(res)

def add_ban_channel(interaction):
    channel_id = interaction.channel_id
    guild_id = interaction.guild_id
    mycursor.execute("INSERT INTO BAN_CHANNEL (channel_id, guild_id) VALUES (%s, %s)", [channel_id, guild_id])
    mydb.commit()
    print(f"Inserted into BAN_CHANNEL -> {channel_id}, {guild_id}")

# Log Channels

def get_log_channel_by_guild_id(guild_id):
    sql = f"SELECT * FROM LOG_CHANNEL WHERE GUILD_ID = '{guild_id}'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    print(myresult)
    if len(myresult) == 0:
        return None
    return myresult[0][0]

def set_log_channel(interaction):
    channel_id = interaction.channel_id
    guild_id = interaction.guild_id
    db_channel = get_log_channel_by_guild_id(guild_id)
    args = [channel_id, guild_id]
    if db_channel == None:
        mycursor.execute("INSERT INTO LOG_CHANNEL (channel_id, guild_id) VALUES (%s, %s)", args)
        mydb.commit()
        print(f"Inserted into LOG_CHANNEL -> {channel_id}, {guild_id}")
    else:
        mycursor.execute("UPDATE LOG_CHANNEL SET channel_id = '%s' WHERE guild_id = '%s'", args)
        mydb.commit()
        print(f"Updated LOG_CHANNEL -> {channel_id}, {guild_id}")