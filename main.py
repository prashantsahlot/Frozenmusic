import os
import logging
from telethon import TelegramClient, events

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace with your own values
api_id = 24210859  # Your API ID
api_hash = '45dd2e83d7e7430b49e18b48080b81c4'  # Your API Hash
phone_number = input("Enter your phone number (e.g., +919582898743): ")

# Create the client and connect
client = TelegramClient('userbot', api_id, api_hash)

# Store approved users
approved_users = set()

# Variable to store the host ID (automatically extracted)
HOST_ID = None

@client.on(events.NewMessage(incoming=True))
async def pm_guard(event):
    # Check if the message is a direct message (DM)
    if event.is_private:
        sender_id = event.sender_id
        
        # If sender is not approved, respond with the PM guard message
        if sender_id not in approved_users:
            await event.reply("Hello, this is the Frozen userbot. Drop your message here; I will check it later.")
        else:
            # If sender is approved, just respond to their message
            await event.reply(f"Message from {sender_id}: {event.message.text}")

@client.on(events.NewMessage(pattern=r'\.approve'))
async def approve_user(event):
    # Check if the command is sent by the host ID
    if event.sender_id == HOST_ID:
        # Automatically extract the sender ID who needs approval
        user_to_approve = event.message.reply_to_msg_id
        if user_to_approve:
            original_message = await event.get_reply_message()
            if original_message:
                user_id = original_message.sender_id  # Get the sender ID of the original message
                approved_users.add(user_id)
                await event.respond(f"User {user_id} approved!")
            else:
                await event.respond("Reply to a user's message to approve them.")
        else:
            await event.respond("You need to reply to a user's message with `.approve` to approve them.")
    else:
        await event.respond("You are not authorized to use this command.")

@client.on(events.NewMessage(pattern=r'\.id'))
async def send_user_id(event):
    # Check if the message is a reply
    if event.is_reply and event.reply_to_msg_id:
        # Get the original message
        original_message = await event.get_reply_message()
        if original_message:
            sender_id = original_message.sender_id  # Get the sender ID of the original message
            await event.respond(f"The user ID of the person you replied to is: {sender_id}")
    else:
        await event.respond("Please reply to a message with `.id` to get the user's ID.")

async def main():
    global HOST_ID  # Declare HOST_ID as global to modify it
    await client.start()
    
    # Automatically extract the host user ID
    me = await client.get_me()
    HOST_ID = me.id  # Set the host ID to the bot's user ID

    print(f"Bot is running with host ID: {HOST_ID}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Run the main function
    with client:
        client.loop.run_until_complete(main())
