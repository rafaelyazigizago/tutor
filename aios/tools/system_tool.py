import subprocess
from .tool import Tool


class SystemTool(Tool):
    """
    Tool responsável por executar comandos no sistema.
    CORREÇÃO: allowlist de prefixos seguros — bloqueia comandos
    potencialmente destrutivos gerados por agentes automáticos.
    """

    # Lista de prefixos de comandos permitidos
    ALLOWED_PREFIXES = [
        "python",
        "pip",
        "git",
        "dir",
        "ls",
        "cat",
        "type",
        "echo",
        "mkdir",
        "tree",
        "cd",
        "pwd",
        "ollama",
    ]

    def __init__(self):

        super().__init__("system")

    def is_allowed(self, command: str) -> bool:

        command_lower = command.strip().lower()

        return any(command_lower.startswith(prefix) for prefix in self.ALLOWED_PREFIXES)

    def execute(self, command: str):

        if not command:
            return "SystemTool: nenhum comando recebido."

        # CORREÇÃO: bloquear comandos fora da allowlist
        if not self.is_allowed(command):
            print(f"🔒 SystemTool: comando bloqueado por segurança: '{command}'")
            return f"Comando bloqueado por política de segurança: '{command}'"

        try:

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout if result.stdout else result.stderr

            return output

        except subprocess.TimeoutExpired:
            return f"SystemTool: timeout ao executar '{command}'"

        except Exception as e:
            return f"SystemTool error: {str(e)}"
