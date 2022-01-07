import asyncio
import discord

import discordbot.config_discordbot as cfg
from discordbot.run_discordbot import gst_bot, logger
from discordbot.stocks.due_diligence.analyst import analyst_command
from discordbot.stocks.due_diligence.pt import pt_command
from discordbot.stocks.due_diligence.est import est_command
from discordbot.stocks.due_diligence.sec import sec_command
from discordbot.stocks.due_diligence.supplier import supplier_command
from discordbot.stocks.due_diligence.customer import customer_command
from discordbot.stocks.due_diligence.arktrades import arktrades_command


class DueDiligenceCommands(discord.ext.commands.Cog):
    """Due Diligence menu."""

    def __init__(self, bot: discord.ext.commands.Bot):
        self.bot = bot

    @discord.ext.commands.command(name="stocks.dd.analyst", usage="[ticker]")
    async def analyst(self, ctx: discord.ext.commands.Context, ticker=""):
        """Displays analyst recommendations [Finviz]

        Parameters
        -----------
        ticker: str
            ticker
        """
        logger.info("stocks.dd.analyst")
        await analyst_command(ctx, ticker)

    @discord.ext.commands.command(name="stocks.dd.pt", usage="[ticker] [raw] [start]")
    async def pt(self, ctx: discord.ext.commands.Context, ticker="", raw="", start=""):
        """Displays chart with price targets [Business Insiders]

        Parameters
        -----------
        ticker: str
            ticker
        raw: boolean
             True or false
        start:
            Starting date in YYYY-MM-DD format
        """
        logger.info("stocks.dd.pt")
        await pt_command(ctx, ticker, raw, start)

    @discord.ext.commands.command(name="stocks.dd.est", usage="[ticker]")
    async def est(self, ctx: discord.ext.commands.Context, ticker=""):
        """Displays earning estimates [Business Insider]

        Parameters
        -----------
        ticker: str
            ticker
        """
        logger.info("stocks.dd.est")
        await est_command(ctx, ticker)

    @discord.ext.commands.command(name="stocks.dd.sec", usage="[ticker]")
    async def sec(self, ctx: discord.ext.commands.Context, ticker=""):
        """Displays sec filings [Market Watch]

        Parameters
        -----------
        ticker: str
            ticker
        """
        logger.info("stocks.dd.sec")
        await sec_command(ctx, ticker)

    @discord.ext.commands.command(name="stocks.dd.supplier", usage="[ticker]")
    async def supplier(self, ctx: discord.ext.commands.Context, ticker=""):
        """Displays suppliers of the company [CSIMarket]

        Parameters
        -----------
        ticker: str
            ticker
        """
        logger.info("stocks.dd.supplier")
        await supplier_command(ctx, ticker)

    @discord.ext.commands.command(name="stocks.dd.customer", usage="[ticker]")
    async def customer(self, ctx: discord.ext.commands.Context, ticker=""):
        """Displays customers of the company [CSIMarket]

        Parameters
        -----------
        ticker: str
            ticker
        """
        logger.info("stocks.dd.customer")
        await customer_command(ctx, ticker)

    @discord.ext.commands.command(name="stocks.dd.arktrades", usage="[ticker] [num]")
    async def arktrades(self, ctx: discord.ext.commands.Context, ticker="", num=""):
        """Displays trades made by ark [cathiesark.com]

        Parameters
        -----------
        ticker: str
            ticker
        num: int
            number of rows displayed
        """
        logger.info("stocks.dd.arktrades")
        await arktrades_command(ctx, ticker, num)

    @discord.ext.commands.command(name="stocks.dd")
    async def due_diligence(self, ctx: discord.ext.commands.Context, ticker=""):
        """Due Diligence Context Menu

        Run `!help DueDiligenceCommands` to see the list of available commands.

        Returns
        -------
        Sends a message to the discord user with the commands from the dd context.
        The user can then select a reaction to trigger a command.
        """
        logger.info("!stocks.dd")

        if ticker == "":
            embed = discord.Embed(
                title="ERROR Stocks: Due Diligence (DD) Menu",
                colour=cfg.COLOR,
                description="A stock ticker is required",
            )
            embed.set_author(
                name=cfg.AUTHOR_NAME,
                icon_url=cfg.AUTHOR_ICON_URL,
            )

        text = (
            f"0️⃣ !stocks.dd.analyst {ticker}\n"
            f"1️⃣ !stocks.dd.pt {ticker} <RAW> <DATE_START>\n"
            f"2️⃣ !stocks.dd.est {ticker}\n"
            f"3️⃣ !stocks.dd.sec {ticker}\n"
            f"4️⃣ !stocks.dd.supplier {ticker}\n"
            f"5️⃣ !stocks.dd.customer {ticker}\n"
            f"6️⃣ !stocks.dd.arktrades {ticker}"
        )

        title = "Stocks: Due Diligence (DD) Menu"
        embed = discord.Embed(title=title, description=text, colour=cfg.COLOR)
        embed.set_author(
            name=cfg.AUTHOR_NAME,
            icon_url=cfg.AUTHOR_ICON_URL,
        )
        msg = await ctx.send(embed=embed)

        emoji_list = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣"]

        for emoji in emoji_list:
            await msg.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in emoji_list

        try:
            reaction, _ = await gst_bot.wait_for(
                "reaction_add", timeout=cfg.MENU_TIMEOUT, check=check
            )
            if reaction.emoji == "0️⃣":
                logger.info("!stocks.dd. Reaction selected: 0")
                await analyst_command(ctx, ticker)
            elif reaction.emoji == "1️⃣":
                logger.info("!stocks.dd. Reaction selected: 1")
                await pt_command(ctx, ticker)
            elif reaction.emoji == "2️⃣":
                logger.info("!stocks.dd. Reaction selected: 2")
                await est_command(ctx, ticker)
            elif reaction.emoji == "3️⃣":
                logger.info("!stocks.dd. Reaction selected: 3")
                await sec_command(ctx, ticker)
            elif reaction.emoji == "4️⃣":
                logger.info("!stocks.dd. Reaction selected: 4")
                await supplier_command(ctx, ticker)
            elif reaction.emoji == "5️⃣":
                logger.info("!stocks.dd. Reaction selected: 5")
                await customer_command(ctx, ticker)
            elif reaction.emoji == "6️⃣":
                logger.info("!stocks.dd. Reaction selected: 6")
                await arktrades_command(ctx, ticker)

            for emoji in emoji_list:
                await msg.remove_reaction(emoji, ctx.bot.user)

        except asyncio.TimeoutError:
            for emoji in emoji_list:
                await msg.remove_reaction(emoji, ctx.bot.user)
            if cfg.DEBUG:
                embed = discord.Embed(
                    description="Error timeout - you snooze you lose! 😋",
                    colour=cfg.COLOR,
                    title="TIMEOUT Stocks: Due Diligence (DD) Menu",
                ).set_author(
                    name=cfg.AUTHOR_NAME,
                    icon_url=cfg.AUTHOR_ICON_URL,
                )
                await ctx.send(embed=embed)


def setup(bot: discord.ext.commands.Bot):
    gst_bot.add_cog(DueDiligenceCommands(bot))
