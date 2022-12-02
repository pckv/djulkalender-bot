import inspect

from .command import Command, CommandCallback


class Module:
    """A module containing commands."""

    def __init__(self) -> None:
        self.commands: list[Command] = []

    def command(self):
        """Decorator for registering a command.

        Command names are automatically inferred from the function name.
        Command descriptions are automatically inferred from the function docstring.
        Arguments are all strings.
        """
        # Define a decorator function for registering the command callback
        def decorator(callback: CommandCallback):
            # Create the command object
            command = Command(
                name=callback.__name__,
                description=callback.__doc__ or "Undocumented command.",
                callback=callback,
                min_args=len(inspect.signature(callback).parameters) - 1,
            )

            # Register the command to the module
            self.commands.append(command)

            return callback

        return decorator
