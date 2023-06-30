

# [+] Создать комнату
@bot.event
async def on_voice_state_update(member: discord.Member,
                                before: discord.VoiceState,
                                after: discord.VoiceState):
    # create room if user connect to 'create room' room
    if str(after.channel) == '[+] Создать комнату':
        if str(after) != str(before):
            await after.channel.clone(name=f'{member} room')
            channel = discord.utils.get(member.guild.voice_channels,
                                        name=f'{member} room')
            if channel is not None:
                await member.move_to(channel)
                await channel.set_permissions(member, mute_members=True,
                                              manage_CHANNELS=True)
                await asyncio.sleep(3)
                if not channel.members:
                    await channel.delete()

    # delete channel after 1 second if user leaved
    try:
        if before.channel.category_id == CATEGORIES[
            'private-voice'] and before.channel.id != CHANNELS[
            'create-voice-channel']:
            channel = bot.get_channel(before.channel.id)
            await asyncio.sleep(1)
            if not channel.members:
                await channel.delete()
    except:
        pass