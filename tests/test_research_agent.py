from aios.agents.research_agent import ResearchAgent


def main():

    agent = ResearchAgent()

    task = {
        "topic": "arquitetura multi-agente em sistemas de inteligência artificial"
    }

    result = agent.handle(task)

    print("\n===== RESULTADO DA PESQUISA =====\n")

    print(result)


if __name__ == "__main__":
    main()