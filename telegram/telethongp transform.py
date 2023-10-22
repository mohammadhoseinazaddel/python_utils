import asyncio
from telethon.sync import TelegramClient
from telethon.tl import functions
import socks

# Replace these with your API credentials
api_id = 1231243
api_hash = 'fsdfsdfzsdfzsdf'

source_group_username = 'https://t.me/+ddasdptzk2MWQ0'
target_group_username = 'https://t.me/+asdsGrc4pPtjNzc8'

# Define your proxy information here
proxy_host = '127.0.0.1'
proxy_port = 2080  # Change to your proxy port

# Create a SOCKS5 proxy connection
proxy = (socks.SOCKS5, proxy_host, proxy_port)

async def main():
    async with TelegramClient('jj', api_id, api_hash, proxy=proxy) as client:
        # Fetch the member list from the source group
        source_group = await client.get_entity(source_group_username)
        source_members = await client.get_participants(source_group)

        # Fetch the member list from the target group
        t_group = await client.get_entity(target_group_username)
        t_members = await client.get_participants(t_group)

        # Extract the usernames or user IDs of members in both source and target groups
        source_member_ids = {member.username or member.id for member in source_members}
        target_member_ids = {member.username or member.id for member in t_members}

        # Find members in the source group that are not in the target group
        members_not_in_target = [member for member in source_members if (member.username or member.id) not in target_member_ids]

        # Print the usernames and first names of members not in the target group
        for member in members_not_in_target:
            username = member.username or "N/A"
            first_name = member.first_name or "N/A"
            print(f"Username: {username}, First Name: {first_name}")

        # Add members to the target group
        target_group = await client.get_entity(target_group_username)
        for member in source_members:
            try:
                await client(functions.channels.InviteToChannelRequest(
                    target_group, [member]
                ))
                print(f"Added {member.first_name} to {target_group_username}")
            except Exception as e:
                print(f"Failed to add {member.first_name}: {e}")

if __name__ == "__main__":
    asyncio.run(main())