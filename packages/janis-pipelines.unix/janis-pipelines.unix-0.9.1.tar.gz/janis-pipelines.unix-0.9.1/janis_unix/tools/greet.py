from janis_core import String, ToolInput, ToolOutput, ToolArgument, Stdout, Boolean
from .unixtool import UnixTool


class Greet(UnixTool):
    def tool(self):
        return "greet"

    def friendly_name(self):
        return "Greet"

    def base_command(self):
        return "echo"

    def arguments(self):
        return [ToolArgument("Hello, ", position=0)]

    def inputs(self):
        return [ToolInput("name", String(), position=1)]

    def outputs(self):
        return [ToolOutput("out", Stdout())]
