import asyncio
import os
import re

from commands import Command, Context, Module
from dotenv import load_dotenv  # type: ignore
from modules import basic

# Create an event loop
loop = asyncio.new_event_loop()

# Pattern for when we receive a message from the server that is a command
COMMAND_PATTERN = re.compile(r"^(\w+)\s*said\s*(.*)$")

# List of all registered commands
commands: list[Command] = []


def register_module(module: Module):
    """Registers all commands from a module."""
    commands.extend(module.commands)


async def main():
    """Main function."""
    # Register modules
    # TODO: should be dynamic based on a modules folder, and should support
    # hot-reloading
    register_module(basic.module)

    # Load environment variables from .env files
    load_dotenv()

    # Set configuration variables based on environment variables
    host = os.getenv("DJUL_HOST", "localhost")
    port = os.getenv("DJUL_PORT", 1337)
    password = os.getenv("DJUL_PASSWORD", None)
    username = os.getenv("DJUL_USERNAME", "TheHolySpirit")
    startup_commands = os.getenv(
        "DJUL_STARTUP_COMMANDS", "go north").split(";")

    # Password is required
    if password is None:
        raise ValueError("Password must be set.")

    startup_commands = [
        password,
        username,
        *startup_commands,
    ]

    # Connect to the server
    reader, writer = await asyncio.open_connection(host, port)

    async def send(message: str):
        """Sends a message to the server."""
        print(message)
        writer.write(f"{message}\n".encode())
        await writer.drain()

    async def say(message: str):
        """Speak in the chat."""
        await send(f"say {message}")

    print("Connected to server.")

    # Send startup commands
    for command in startup_commands:
        await send(command)

    # Main loop
    while True:
        # Read a line from the server and decode it
        data = await reader.read(1024)
        if not data:
            break

        text = data.decode()
        print(text)

        # Attempt to match the line to a command
        match = COMMAND_PATTERN.match(text)
        if not match:
            continue

        # Get the command author, and the raw command arguments
        author, args = match.groups()
        args = args.split(maxsplit=1)

        # Attempt to find a command
        for command in commands:
            if command.name == args[0] and len(args) - 1 >= command.min_args:
                # Create a context for the command
                context = Context(author, say, send, reader, writer, commands)

                # Split the arguments into a list of the required number of arguments
                # -1 because 1 argument would equal 0 splits
                command_args = args[1].split(
                    maxsplit=command.min_args - 1) if command.min_args > 0 else []

                # Get the coroutine of the command and run it in the background
                callback = command.callback(context, *command_args)
                loop.create_task(callback)

    # Close the connection
    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
