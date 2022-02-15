"""Original Code From https://github.com/kablekompany/Kable-Kogs/tree/master/decancer, All Credits to Kable"""
import asyncio
import random
import re
import unicodedata
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, SupportsInt

import discord
import stringcase  # type: ignore
import unidecode
from core.models import getLogger
from discord.ext import commands

properNouns = [
    "Donald Trump",
    "Joe Biden",
    "Ninja",
    "Proton Bomb",
    "He Who Shall Not Be Named",
    "Definitely Phen's Alt",
    "Cable Company without K",
    "Probably Sharts",
]

nouns = [
    "Dog",
    "Cat",
    "Gamer",
    "Ork",
    "Memer",
    "Robot",
    "Programmer",
    "Player",
    "Doctor",
    "Communist",
    "Apple",
    "Godfather",
    "Mafia",
    "Detective",
    "Politician",
]

adjectives = [
    "Fast",
    "Defiant",
    "Homeless",
    "Adorable",
    "Delightful",
    "Homely",
    "Quaint",
    "Adventurous",
    "Depressed",
    "Horrible",
    "Aggressive",
    "Determined",
    "Hungry",
    "Real",
    "Agreeable",
    "Different",
    "Hurt",
    "Relieved",
    "Alert",
    "Difficult",
    "Repulsive",
    "Alive",
    "Disgusted",
    "Ill",
    "Rich",
    "Amused",
    "Distinct",
    "Important",
    "Angry",
    "Disturbed",
    "Impossible",
    "Scary",
    "Annoyed",
    "Dizzy",
    "Inexpensive",
    "Selfish",
    "Annoying",
    "Doubtful",
    "Innocent",
    "Shiny",
    "Anxious",
    "Drab",
    "Inquisitive",
    "Shy",
    "Arrogant",
    "Dull",
    "Itchy",
    "Silly",
    "Ashamed",
    "Sleepy",
    "Attractive",
    "Eager",
    "Jealous",
    "Smiling",
    "Average",
    "Easy",
    "Jittery",
    "Smoggy",
    "Awful",
    "Elated",
    "Jolly",
    "Sore",
    "Elegant",
    "Joyous",
    "Sparkling",
    "Bad",
    "Embarrassed",
    "Splendid",
    "Beautiful",
    "Enchanting",
    "Kind",
    "Spotless",
    "Better",
    "Encouraging",
    "Stormy",
    "Bewildered",
    "Energetic",
    "Lazy",
    "Strange",
    "Enthusiastic",
    "Light",
    "Stupid",
    "Bloody",
    "Envious",
    "Lively",
    "Successful",
    "Blue",
    "Evil",
    "Lonely",
    "Super",
    "Blue-eyed",
    "Excited",
    "Long",
    "Blushing",
    "Expensive",
    "Lovely",
    "Talented",
    "Bored",
    "Exuberant",
    "Lucky",
    "Tame",
    "Brainy",
    "Tender",
    "Brave",
    "Fair",
    "Magnificent",
    "Tense",
    "Breakable",
    "Faithful",
    "Misty",
    "Terrible",
    "Bright",
    "Famous",
    "Modern",
    "Tasty",
    "Busy",
    "Fancy",
    "Motionless",
    "Thankful",
    "Fantastic",
    "Muddy",
    "Thoughtful",
    "Calm",
    "Fierce",
    "Mushy",
    "Thoughtless",
    "Careful",
    "Filthy",
    "Mysterious",
    "Tired",
    "Cautious",
    "Fine",
    "Tough",
    "Charming",
    "Foolish",
    "Nasty",
    "Troubled",
    "Cheerful",
    "Fragile",
    "Naughty",
    "Clean",
    "Frail",
    "Nervous",
    "Ugliest",
    "Clear",
    "Frantic",
    "Nice",
    "Ugly",
    "Clever",
    "Friendly",
    "Nutty",
    "Uninterested",
    "Cloudy",
    "Frightened",
    "Unsightly",
    "Clumsy",
    "Funny",
    "Obedient",
    "Unusual",
    "Colorful",
    "Obnoxious",
    "Upset",
    "Combative",
    "Gentle",
    "Odd",
    "Uptight",
    "Comfortable",
    "Gifted",
    "Old-fashioned",
    "Concerned",
    "Glamorous",
    "Open",
    "Vast",
    "Condemned",
    "Gleaming",
    "Outrageous",
    "Victorious",
    "Confused",
    "Glorious",
    "Outstanding",
    "Vivacious",
    "Cooperative",
    "Good",
    "Courageous",
    "Gorgeous",
    "Panicky",
    "Wandering",
    "Crazy",
    "Graceful",
    "Perfect",
    "Weary",
    "Creepy",
    "Grieving",
    "Plain",
    "Wicked",
    "Crowded",
    "Grotesque",
    "Pleasant",
    "Wide-eyed",
    "Cruel",
    "Grumpy",
    "Poised",
    "Wild",
    "Curious",
    "Poor",
    "Witty",
    "Cute",
    "Handsome",
    "Powerful",
    "Worrisome",
    "Happy",
    "Precious",
    "Worried",
    "Dangerous",
    "Healthy",
    "Prickly",
    "Wrong",
    "Dark",
    "Helpful",
    "Proud",
    "Dead",
    "Helpless",
    "Putrid",
    "Zany",
    "Defeated",
    "Hilarious",
    "Puzzled",
    "Zealous",
    "Dank",
    "Sexy",
    "Darth",
]

# from: https://github.com/Cog-Creators/Red-DiscordBot/blob/9ab307c1efc391301fc6498391d2e403aeee2faa/redbot/core/utils/chat_formatting.py#L122
def box(text: str, lang: str = "") -> str:
    """Get the given text in a code block.
    Parameters
    ----------
    text : str
        The text to be marked up.
    lang : `str`, optional
        The syntax highlighting language for the codeblock.
    Returns
    -------
    str
        The marked up text.
    """
    return f"```{lang}\n{text}\n```"


# from: https://github.com/Cog-Creators/Red-DiscordBot/blob/9ab307c1efc391301fc6498391d2e403aeee2faa/redbot/core/utils/chat_formatting.py#L517
def humanize_timedelta(
    *, timedelta: Optional[timedelta] = None, seconds: Optional[SupportsInt] = None
) -> str:
    """
    Get a locale aware human timedelta representation.
    This works with either a timedelta object or a number of seconds.
    Fractional values will be omitted, and values less than 1 second
    an empty string.
    Parameters
    ----------
    timedelta: Optional[datetime.timedelta]
        A timedelta object
    seconds: Optional[SupportsInt]
        A number of seconds
    Returns
    -------
    str
        A locale aware representation of the timedelta or seconds.
    Raises
    ------
    ValueError
        The function was called with neither a number of seconds nor a timedelta object
    """

    try:
        obj = seconds if seconds is not None else timedelta.total_seconds()
    except AttributeError:
        raise ValueError("You must provide either a timedelta or a number of seconds")

    seconds = int(obj)
    periods = [
        ("year", "years", 60 * 60 * 24 * 365),
        ("month", "months", 60 * 60 * 24 * 30),
        ("day", "days", 60 * 60 * 24),
        ("hour", "hours", 60 * 60),
        ("minute", "minutes", 60),
        ("second", "seconds", 1),
    ]

    strings = []
    for period_name, plural_period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 0:
                continue
            unit = plural_period_name if period_value > 1 else period_name
            strings.append(f"{period_value} {unit}")

    return ", ".join(strings)


# originally from https://github.com/PumPum7/PumCogs repo which has a en masse version of this
class Decancer(commands.Cog):
    """
    Decancer users names removing special and accented chars.

    `[p]decancerset` to get started if you're already using redbot core modlog
    """

    _id = "config"
    default_config = {
        "modlogchannel": str(int()),
        "auto": False,
        "new_custom_nick": "simp name",
    }

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.api.get_plugin_partition(self)
        self._config_cache: Dict[str, Any] = {}
        self.enabled_guilds = set()
        self.logger = getLogger("modmail.decancer")
        self.bot.loop.create_task(self.initialize())

    __author__ = ["KableKompany#0001", "PhenoM4n4n"]
    __version__ = "1.8.2"

    async def initialize(self):
        await self.populate_config_cache()
        await self.populate_enabled_guilds()

    async def populate_config_cache(self):
        """
        Populates the config cache with data from database.
        """
        db_config = await self.db.find_one({"_id": self._id})
        if db_config is None:
            db_config = {}  # empty dict, so we can use `.get` method without error

        to_update = False
        for guild in self.bot.guilds:
            config = db_config.get(str(guild.id))
            if config is None:
                config = {k: v for k, v in self.default_config.items()}
                to_update = True
            self._config_cache[str(guild.id)] = config

        if to_update:
            await self.config_update()

    def guild_config(self, guild_id: str):
        config = self._config_cache.get(guild_id)
        if config is None:
            config = {k: v for k, v in self.default_config.items()}
            self._config_cache[guild_id] = config

        return config

    async def config_update(self):
        """
        Updates the database with the data from config cache.
        This will update the database from the cache globally (not guild specific).
        """
        await self.db.find_one_and_update(
            {"_id": self._id},
            {"$set": self._config_cache},
            upsert=True,
        )

    async def populate_enabled_guilds(self):
        await self.bot.wait_until_ready()

        for guild in self.bot.guilds:
            config = self.guild_config(str(guild.id))
            if config["auto"] == False:
                continue
            self.logger.info(f"Enabling decancer for {guild.name}")
            self.enabled_guilds.add(guild.id)

    @staticmethod
    def is_cancerous(text: str) -> bool:
        for segment in text.split():
            for char in segment:
                if not (char.isascii() and char.isalnum()):
                    return True
        return False

    # the magic
    @staticmethod
    def strip_accs(text):
        try:
            text = unicodedata.normalize("NFKC", text)
            text = unicodedata.normalize("NFD", text)
            text = unidecode.unidecode(text)
            text = text.encode("ascii", "ignore")
            text = text.decode("utf-8")
        except Exception as e:
            print(e)
        return str(text)

    # the magician
    async def nick_maker(self, guild: discord.Guild, old_shit_nick):
        old_shit_nick = self.strip_accs(old_shit_nick)
        new_cool_nick = re.sub("[^a-zA-Z0-9 \n.]", "", old_shit_nick)
        new_cool_nick = " ".join(new_cool_nick.split())
        new_cool_nick = stringcase.lowercase(new_cool_nick)
        new_cool_nick = stringcase.titlecase(new_cool_nick)
        default_name = self.guild_config(str(guild.id)).get("new_custom_nick")
        if len(new_cool_nick.replace(" ", "")) <= 1 or len(new_cool_nick) > 32:
            if default_name == "random":
                new_cool_nick = await self.get_random_nick(2)
            elif default_name:
                new_cool_nick = default_name
            else:
                new_cool_nick = "simp name"
        return new_cool_nick

    async def decancer_log(
        self,
        guild: discord.Guild,
        member: discord.Member,
        moderator: discord.Member,
        old_nick: str,
        new_nick: str,
        dc_type: str,
    ):
        channel = guild.get_channel(int(self.guild_config(str(guild.id)).get("modlogchannel")))
        if not channel or not (
            channel.permissions_for(guild.me).send_messages
            and channel.permissions_for(guild.me).embed_links
        ):
            return
        color = 0x2FFFFF
        description = [
            f"**Offender:** {member} {member.mention}",
            f"**Reason:** Remove cancerous characters from previous name",
            f"**New Nickname:** {new_nick}",
            f"**Responsible Moderator:** {moderator} {moderator.mention}",
        ]
        embed = discord.Embed(
            color=discord.Color(color),
            title=dc_type,
            description="\n".join(description),
            timestamp=datetime.utcnow(),
        )
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

    async def get_random_nick(self, nickType: int):
        if nickType == 1:
            new_nick = random.choice(properNouns)
        elif nickType == 2:
            adjective = random.choice(adjectives)
            noun = random.choice(nouns)
            new_nick = adjective + noun
        elif nickType == 3:
            adjective = random.choice(adjectives)
            new_nick = adjective.lower()
        if nickType == 4:
            nounNicks = nouns, properNouns
            new_nick = random.choice(random.choices(nounNicks, weights=map(len, nounNicks))[0])
        return new_nick

    @commands.group()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def decancerset(self, ctx):
        """
        Set up the modlog channel for decancer'd users,
        and set your default name if decancer is unsuccessful.
        """

        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @decancerset.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def showsettings(self, ctx):
        """
        Shows the current settings for the server.
        """
        data = self.guild_config(str(ctx.guild.id))
        channel = data["modlogchannel"]
        name = data["new_custom_nick"]
        auto = data["auto"]
        if channel == str(0):
            channel = "**NOT SET**"
        else:
            channel = self.bot.get_channel(int(channel)).mention
        values = [f"**Modlog Destination:** {channel}", f"**Default Name:** `{name}`"]
        if auto:
            values.append(f"**Auto-Decancer:** `{auto}`")
        e = discord.Embed(colour=self.bot.main_color)
        e.add_field(
            name=f"{ctx.guild.name} Settings",
            value="\n".join(values),
        )
        e.set_footer(text="To change these, pass [p]decancerset modlog|defaultname")
        e.set_image(url=ctx.guild.icon_url)
        try:
            await ctx.send(embed=e)
        except Exception:
            pass
    
    @decancerset.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def toggle(self, ctx):
        """
        Toggles the auto-decancer on and off.
        """
        config= self.guild_config(str(ctx.guild.id))
        auto = config["auto"]
        if auto:
            new_config = dict(auto=False)
            self.enabled_guilds.remove(ctx.guild.id)
            await ctx.send("Auto-decancer has been disabled.")
        else:
            new_config = dict(auto=True)
            self.enabled_guilds.add(ctx.guild.id)
            await ctx.send("Auto-decancer has been enabled.")
        config.update(new_config)
        await self.config_update()

    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    @decancerset.command(aliases=["ml"])
    async def modlog(self, ctx, channel: discord.TextChannel, override: str = None):
        """
        Set a decancer entry to a channel.
        """
        config = self.guild_config(str(ctx.guild.id))
        new_config = dict(modlogchannel=str(channel.id))
        config.update(new_config)
        await self.config_update()

        embed = discord.Embed(
            description=f"Modlog channel is now set to {channel.mention}",
            color=self.bot.main_color,
        )
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    @decancerset.command(aliases=["name"])
    async def defaultname(self, ctx, *, name):
        """
        If you don't want a server of simps, change this
        to whatever you'd like, simp.


            Example: `[p]decancerset name kable is coolaf`
        Changing the default to "random" might do something cool..
        """
        if len(name) > 32 or len(name) < 3:
            await ctx.send("Let's keep that nickname within reasonable range, scrub")
            return

        config = self.guild_config(str(ctx.guild.id))
        new_config = dict(new_custom_nick=str(name))
        config.update(new_config)
        await self.config_update()
        await ctx.send(
            f"Your fallback name, should the cancer be too gd high for me to fix, is `{name}`"
        )

    @commands.command(name="decancer")
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.guild_only()
    async def nick_checker(self, ctx: commands.Context, user: discord.Member):
        """
        Remove special/cancerous characters from user nicknames

        Change username glyphs (i.e 乇乂, 黑, etc)
        special font chars (zalgo, latin letters, accents, etc)
        to their unicode counterpart. If the former, expect the "english"
        equivalent to other language based glyphs.
        """
        config = self.guild_config(str(ctx.guild.id))
        if config["modlogchannel"] == str(0):
            return await ctx.send(
                f"Set up a modlog for this server using `{ctx.prefix}decancerset modlog #channel`"
            )

        if user.top_role >= ctx.me.top_role:
            return await ctx.send(
                f"I can't decancer that user since they are higher than me in heirarchy."
            )
        m_nick = user.display_name
        new_cool_nick = await self.nick_maker(ctx.guild, m_nick)
        if m_nick != new_cool_nick:
            try:
                await user.edit(
                    reason=f"Old name ({m_nick}): contained special characters",
                    nick=new_cool_nick,
                )
            except Exception as e:
                await ctx.send(
                    f"Double check my order in heirarchy buddy, got an error\n```diff\n- {e}\n```"
                )
                return
            await ctx.send(f"({m_nick}) was changed to {new_cool_nick}")

            guild = ctx.guild
            await self.decancer_log(guild, user, ctx.author, m_nick, new_cool_nick, "decancer")
            try:
                await ctx.tick()
            except discord.NotFound:
                pass

        else:
            await ctx.send(f"{user.display_name} was already decancer'd")
            try:
                await ctx.message.add_reaction("\N{CROSS MARK}")
            except Exception:
                return

    @commands.max_concurrency(1, commands.BucketType.guild)
    @commands.cooldown(1, 36000, commands.BucketType.guild)
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    @commands.guild_only()
    @commands.command(cooldown_after_parsing=True)
    async def dehoist(self, ctx: commands.Context, *, role: discord.Role = None):
        """Decancer all members of the targeted role.

        Role defaults to all members of the server."""
        config = self.guild_config(str(ctx.guild.id))
        if config["modlogchannel"] == str(0):
            await ctx.send(
                f"Set up a modlog for this server using `{ctx.prefix}decancerset modlog #channel`"
            )
            ctx.command.reset_cooldown(ctx)
            return

        role = role or ctx.guild.default_role
        guild = ctx.guild
        cancerous_list = [
            member
            for member in role.members
            if not member.bot
            and self.is_cancerous(member.display_name)
            and ctx.me.top_role > member.top_role
        ]
        if not cancerous_list:
            await ctx.send(f"There's no one I can decancer in **`{role}`**.")
            ctx.command.reset_cooldown(ctx)
            return
        if len(cancerous_list) > 5000:
            await ctx.send(
                "There are too many members to decancer in the targeted role. "
                "Please select a role with less than 5000 members."
            )
            ctx.command.reset_cooldown(ctx)
            return
        member_preview = "\n".join(
            f"{member} - {member.id}"
            for index, member in enumerate(cancerous_list, 1)
            if index <= 10
        ) + (
            f"\nand {len(cancerous_list) - 10} other members.." if len(cancerous_list) > 10 else ""
        )

        case = "" if len(cancerous_list) == 1 else "s"
        await ctx.send(
            f"Are you sure you want me to decancer the following {len(cancerous_list)} member{case}? yes or no\n"
            + box(member_preview, "py")
        )
        try:
            m = await self.bot.wait_for(
                "message",
                check=lambda p: p.author.id == ctx.author.id and p.channel.id == ctx.channel.id,
                timeout=60,
            )
        except asyncio.TimeoutError:
            await ctx.send("Action cancelled.")
            ctx.command.reset_cooldown(ctx)
            return

        if m.content.lower() == "yes":
            await ctx.send(
                f"Ok. This will take around **{humanize_timedelta(timedelta=timedelta(seconds=len(cancerous_list) * 1.5))}**."
            )
            async with ctx.typing():
                for member in cancerous_list:
                    await asyncio.sleep(1)
                    old_nick = member.display_name
                    new_cool_nick = await self.nick_maker(guild, member.display_name)
                    if old_nick.lower() != new_cool_nick.lower():
                        try:
                            await member.edit(
                                reason=f"Dehoist | Old name ({old_nick}): contained special characters",
                                nick=new_cool_nick,
                            )
                        except discord.Forbidden:
                            await ctx.send("Dehoist failed due to invalid permissions.")
                            return
                        except discord.NotFound:
                            continue
                    else:
                        await self.decancer_log(
                            guild, member, guild.me, old_nick, new_cool_nick, "dehoist"
                        )
            try:
                await ctx.send("Dehoist completed.")
            except (discord.NotFound, discord.Forbidden):
                pass
        else:
            await ctx.send("Action cancelled.")
            ctx.command.reset_cooldown(ctx)
            return

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        member = after
        if member.bot:
            return

        guild: discord.Guild = member.guild
        if guild.id not in self.enabled_guilds:
            return

        data = self.guild_config(str(member.guild.id))
        if data["auto"] == False:
            self.logger.info(f"not auto enabled in {guild}")
            return
        if data["modlogchannel"] == str(0):
            self.logger.info(f"modlog not set in {guild}")
            return

        old_nick = member.display_name
        if not self.is_cancerous(old_nick):
            return

        await asyncio.sleep(
            5
        )  # waiting for auto mod actions to take place to prevent discord from fucking up the nickname edit
        member = guild.get_member(member.id)
        if not member:
            return
        if member.top_role >= guild.me.top_role:
            return
        new_cool_nick = await self.nick_maker(guild, old_nick)
        if old_nick.lower() != new_cool_nick.lower():
            try:
                await member.edit(
                    reason=f"Auto Decancer | Old name ({old_nick}): contained special characters",
                    nick=new_cool_nick,
                )
            except discord.NotFound:
                pass
            else:
                await self.decancer_log(
                    guild, member, guild.me, old_nick, new_cool_nick, "auto-decancer"
                )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.bot:
            return

        guild: discord.Guild = member.guild
        if guild.id not in self.enabled_guilds:
            return

        data = self.guild_config(str(member.guild.id))
        if data["auto"] == False:
            self.logger.info(f"not auto enabled in {guild}")
            return
        if data["modlogchannel"] == str(0):
            self.logger.info(f"modlog not set in {guild}")
            return

        old_nick = member.display_name
        if not self.is_cancerous(old_nick):
            return

        await asyncio.sleep(
            5
        )  # waiting for auto mod actions to take place to prevent discord from fucking up the nickname edit
        member = guild.get_member(member.id)
        if not member:
            return
        if member.top_role >= guild.me.top_role:
            return
        new_cool_nick = await self.nick_maker(guild, old_nick)
        if old_nick.lower() != new_cool_nick.lower():
            try:
                await member.edit(
                    reason=f"Auto Decancer | Old name ({old_nick}): contained special characters",
                    nick=new_cool_nick,
                )
            except discord.NotFound:
                pass
            else:
                await self.decancer_log(
                    guild, member, guild.me, old_nick, new_cool_nick, "auto-decancer"
                )


def setup(bot):
    bot.add_cog(Decancer(bot))
