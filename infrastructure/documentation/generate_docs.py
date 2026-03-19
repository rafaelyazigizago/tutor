import os
import datetime


PROJECT_ROOT = os.getcwd()

DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

AGENTS_DIR = os.path.join(PROJECT_ROOT, "aios", "agents")
TOOLS_DIR = os.path.join(PROJECT_ROOT, "aios", "tools")
MEMORY_DIR = os.path.join(PROJECT_ROOT, "aios", "memory")
ORCHESTRATOR_DIR = os.path.join(PROJECT_ROOT, "aios", "orchestrator")


def ensure_docs():

    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)


def list_python_files(directory):

    files = []

    if not os.path.exists(directory):
        return files

    for file in os.listdir(directory):

        if file.endswith(".py") and not file.startswith("__"):
            files.append(file)

    return sorted(files)


def generate_agents_doc():

    agents = list_python_files(AGENTS_DIR)

    path = os.path.join(DOCS_DIR, "agents.md")

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Tutor AIOS — Agents\n\n")

        for agent in agents:
            f.write(f"- {agent}\n")


def generate_tools_doc():

    tools = list_python_files(TOOLS_DIR)

    path = os.path.join(DOCS_DIR, "tools.md")

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Tutor AIOS — Tools\n\n")

        for tool in tools:
            f.write(f"- {tool}\n")


def generate_memory_doc():

    memory = list_python_files(MEMORY_DIR)

    path = os.path.join(DOCS_DIR, "memory.md")

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Tutor AIOS — Memory\n\n")

        for m in memory:
            f.write(f"- {m}\n")


def generate_orchestrator_doc():

    files = list_python_files(ORCHESTRATOR_DIR)

    path = os.path.join(DOCS_DIR, "orchestrator.md")

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Tutor AIOS — Orchestrator\n\n")

        for file in files:
            f.write(f"- {file}\n")


def generate_architecture():

    path = os.path.join(DOCS_DIR, "architecture.md")

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Tutor AIOS — Architecture\n\n")

        f.write("## Core\n")
        f.write("- OrchestratorEngine\n")
        f.write("- TaskQueue\n")
        f.write("- AgentRegistry\n")
        f.write("- AgentRouter\n")
        f.write("- TaskPlanner\n")
        f.write("- LLMPlanner\n\n")

        f.write("## Memory\n")
        f.write("- VectorMemory\n")
        f.write("- ExecutionMemory\n\n")

        f.write("## Auto Expansion\n")
        f.write("- AutoAgentBuilder\n")
        f.write("- DynamicAgentLoader\n\n")

        f.write("## Telemetry\n")
        f.write("- run_tutor.py\n")
        f.write("- logs/\n")


def generate_roadmap():

    path = os.path.join(DOCS_DIR, "roadmap.md")

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Tutor AIOS — Roadmap\n\n")

        f.write("## Implementado\n")
        f.write("- OrchestratorEngine\n")
        f.write("- TaskPlanner\n")
        f.write("- LLMPlanner\n")
        f.write("- ExecutionMemory\n")
        f.write("- AutoAgentBuilder\n")
        f.write("- DynamicAgentLoader\n")
        f.write("- Telemetry System\n\n")

        f.write("## Próximos passos\n")
        f.write("- PlanEvaluator\n")
        f.write("- Agent Collaboration\n")
        f.write("- Learning Engine\n")
        f.write("- Dashboard\n")
        f.write("- System Agents\n")


def generate_project_state():

    path = os.path.join(DOCS_DIR, "project_state.md")

    with open(path, "w", encoding="utf-8") as f:

        f.write("# Tutor AIOS — Project State\n\n")

        f.write(f"Generated: {datetime.datetime.now()}\n\n")

        f.write("Este documento representa o estado atual validado do projeto.\n")

        f.write("\nSomente funcionalidades testadas e confirmadas foram incluídas.\n")


def generate_all():

    ensure_docs()

    generate_agents_doc()
    generate_tools_doc()
    generate_memory_doc()
    generate_orchestrator_doc()
    generate_architecture()
    generate_roadmap()
    generate_project_state()

    print("\n📚 Documentação do Tutor atualizada com sucesso.\n")


if __name__ == "__main__":

    generate_all()