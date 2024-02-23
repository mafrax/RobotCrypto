from telethon import TelegramClient, sync
import asyncio

import logging

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace these with your own details
api_id = 25428367  # Replace with your API ID
api_hash = '43184722c143dff1ab585b46ff6b3691'  # Replace with your API Hash
phone_number = '+33616394706'  # Replace with your phone number

# Initialize the client
client = TelegramClient('session_name', api_id, api_hash)


async def main():
    # Start the client and ensure the user is authorized
    try:
        client.start()
        # await client.start()
        logger.info("Client Created")
        print("Client Created")
        if client.is_user_authorized():
            print("User is authorized.")
        else:
            print("User is not authorized. Please check your phone for the verification code.")

        # Example: Fetch and print details of the current user
        me = client.get_me()
        print(me)
    finally:
        client.disconnect()

    # Function to get messages from a specific channel or group
    async def get_messages():
        # Replace 'channel_name' with the actual name of the channel or group
        channel = client.get_entity('https://t.me/trendingssol')
        # Fetch the last 10 messages
        messages = client.get_messages(channel, limit=10)
        for message in messages:
            print(message.id, message.text)

    # Call the get_messages function
    await get_messages()


# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
