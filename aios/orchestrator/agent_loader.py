import os
import importlib
import inspect


class DynamicAgentLoader:
    """
    Detecta e registra agentes automaticamente.
    """

    IGNORE_CLASSES = {
        "BaseAgent",
        "ToolAgent",
        "LLMAgent"
    }

    def __init__(self, registry):

        self.registry = registry

        self.agents_package = "aios.agents"
        self.agents_dir = os.path.join("aios", "agents")

    def load_agents(self):

        if not os.path.exists(self.agents_dir):
            return

        for file in os.listdir(self.agents_dir):

            if not file.endswith(".py"):
                continue

            if file.startswith("__"):
                continue

            module_name = file[:-3]

            try:

                module = importlib.import_module(
                    f"{self.agents_package}.{module_name}"
                )

                self._register_from_module(module)

            except Exception as e:

                print(f"⚠️ Erro ao carregar agente {module_name}: {e}")

    def _register_from_module(self, module):

        for name, obj in inspect.getmembers(module):

            if not inspect.isclass(obj):
                continue

            if not name.endswith("Agent"):
                continue

            if name in self.IGNORE_CLASSES:
                continue

            try:

                # tenta criar agente
                agent = obj()

            except TypeError:
                # construtor incompatível
                continue

            except Exception as e:
                print(f"⚠️ Falha ao instanciar agente {name}: {e}")
                continue

            try:

                agent_name = getattr(agent, "name", None)

                if not agent_name:
                    agent_name = name.replace("Agent", "").lower()

                if not self.registry.exists(agent_name):

                    print(f"🔌 Registrando agente dinâmico: {agent_name}")

                    self.registry.register(agent_name, agent)

            except Exception as e:

                print(f"⚠️ Falha ao registrar agente {name}: {e}")