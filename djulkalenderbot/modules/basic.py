from commands import Context, Module

module = Module()


@module.command()
async def echo(ctx: Context, message: str):
    """Echoes the given message."""
    await ctx.say(message)


@module.command()
async def help(ctx: Context):
    """Shows a list of all commands."""
    await ctx.say("Available commands: " + " ".join(c.name for c in ctx.commands))


@module.command()
async def man(ctx: Context, command: str):
    """Shows the documentation for a command."""
    for c in ctx.commands:
        if c.name == command:
            await ctx.say(c.description)
            return

    await ctx.say(f"Command '{command}' not found.")
