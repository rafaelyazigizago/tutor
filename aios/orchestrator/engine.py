from aios.orchestrator.task_queue import TaskQueue
from aios.orchestrator.agent_registry import AgentRegistry
from aios.orchestrator.router import AgentRouter
from aios.orchestrator.task_planner import TaskPlanner
from aios.memory.execution_memory import ExecutionMemory
from aios.orchestrator.agent_loader import DynamicAgentLoader


class OrchestratorEngine:
    """
    Cérebro central do AIOS.
    CORREÇÕES APLICADAS:
      - usa agent.run() em vez de agent.execute() (preserva logs e error handling)
      - status de execução real (success / partial_failure)
      - try/except por task: uma falha não derruba toda a execução
    """

    MAX_STEPS = 10

    def __init__(self):

        self.queue = TaskQueue()
        self.registry = AgentRegistry()
        self.router = AgentRouter()
        self.planner = TaskPlanner(self.router)
        self.execution_memory = ExecutionMemory()

        self.agent_loader = DynamicAgentLoader(self.registry)

        self.current_objective = None
        self.current_plan = []

    def register_agent(self, name: str, agent):

        print(f"Registering agent: {name}")
        self.registry.register(name, agent)

    def register_route(self, intent: str, agent_name: str):

        self.router.register(intent, agent_name)

    def add_task(self, task):

        print(f"Task added: {task.name}")
        self.queue.add(task)
        self.current_plan.append(task.name)

    def run_objective(self, objective: str):

        print("\n🎯 Objetivo recebido:")
        print(objective)

        self.current_objective = objective
        self.current_plan = []

        tasks = self.planner.create_plan(objective)

        for task in tasks:
            self.add_task(task)

    def start(self):

        print("\n🔎 Detectando agentes dinâmicos...\n")
        self.agent_loader.load_agents()

        print("AIOS Orchestrator started")

        steps = 0
        failed_tasks = []

        while not self.queue.is_empty():

            if steps >= self.MAX_STEPS:
                print("\n⚠️  Max steps reached. Stopping execution.")
                break

            steps += 1

            task = self.queue.next()

            print(f"\nExecuting task: {task.name}")

            agent_name = self.router.resolve(task.payload)

            if not agent_name:
                agent_name = task.name

            agent = self.registry.get(agent_name)

            if not agent:
                print(f"❌ Agent not found: {agent_name}. Skipping task.")
                failed_tasks.append(task.name)
                continue

            # CORREÇÃO: usar run() que inclui logs e tratamento de erros
            try:
                agent.run(task.payload)

            except Exception as e:
                print(f"❌ Task '{task.name}' falhou: {e}")
                failed_tasks.append(task.name)

        # CORREÇÃO: status real baseado nas falhas
        if not failed_tasks:
            final_status = "success"
        elif len(failed_tasks) < steps:
            final_status = "partial_failure"
        else:
            final_status = "failure"

        self.execution_memory.record_execution(
            objective=self.current_objective,
            plan=self.current_plan,
            tasks_executed=steps,
            status=final_status
        )

        print(f"\n✅ Execução finalizada. Status: {final_status}")
        print(f"   Tasks executadas: {steps} | Falhas: {len(failed_tasks)}")
