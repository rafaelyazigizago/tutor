import os
from .tool import Tool


class FileSystemTool(Tool):
    """
    Tool responsável por operações no sistema de arquivos.
    """

    def __init__(self):

        super().__init__("filesystem")

    def execute(self, action: str, path: str = "", content: str = ""):

        if action == "read":

            if not os.path.exists(path):
                return f"File not found: {path}"

            with open(path, "r", encoding="utf-8") as f:
                return f.read()

        if action == "write":

            directory = os.path.dirname(path)

            if directory and not os.path.exists(directory):
                os.makedirs(directory)

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            return f"File written: {path}"

        if action == "append":

            with open(path, "a", encoding="utf-8") as f:
                f.write(content)

            return f"Content appended to: {path}"

        if action == "list":

            if not os.path.exists(path):
                return f"Directory not found: {path}"

            return os.listdir(path)

        return "Invalid filesystem action"