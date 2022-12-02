import asyncio

from commands import Context, Module

module = Module()


TRACKMAKER = [
    "mai hausu is danbooru",
    "NEW hausu erekutoro hausu",
    "Torakku doraibaa tsuukin rasshu",
    "Appu na roodo wa tenshon MAX",
    "Hausu dasuto non fikkushon",
    "Kafunshou ni wa masuku meron",
    "Kaasoru matte yo kurakushon",
    "Hora kurikku ririkku torakku meikaa",
    "",
    "oshare no kyokuchi da fasshon sentaa",
    "Ryoute wo kakagete kurappyohenza",
    "Jaaji ni waishatsu zettai hen da",
    "M.I.D.I torakku meikaa",
    "Oshare no seichi da fasshon sentaa",
    "Ryoute wo kakagete kurappyohenza",
    "Nouki wa ashita da zettai tetsuya",
    "Ebidei ebinai torakku meikaa",
    "",
    "torakku meikaa kurappyohenza",
    "Torakku meikaa kurappyohenza",
]


@module.command()
async def kurappyohenza(ctx: Context):
    """Echoes the given message."""
    for line in TRACKMAKER:
        await ctx.say(line)
        await asyncio.sleep(2)
