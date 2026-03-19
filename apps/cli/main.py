from aios.orchestrator.engine import OrchestratorEngine

from aios.agents.tutor_agent import TutorAgent
from aios.agents.research_agent import ResearchAgent
from aios.agents.builder_agent import BuilderAgent
from aios.agents.system_agent import SystemAgent


def main():

    engine = OrchestratorEngine()

    tutor = TutorAgent()
    research = ResearchAgent()
    builder = BuilderAgent()
    system = SystemAgent()

    engine.register_agent("tutor", tutor)
    engine.register_agent("research", research)
    engine.register_agent("builder", builder)
    engine.register_agent("system", system)

    engine.register_route("tutor", "tutor")
    engine.register_route("research", "research")
    engine.register_route("builder", "builder")
    engine.register_route("system", "system")

    engine.run_objective(
        "Como construir um sistema de agentes de IA"
    )

    engine.start()


if __name__ == "__main__":
    main()