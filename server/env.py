from uuid import uuid4
from typing import List

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from .models import SpecGamingAction, SpecGamingObservation
from .tasks import TASKS


class SpecGamingEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._reset_count = 0

        self.tasks = TASKS
        self.current_task = None

    # -------------------------
    # RESET
    # -------------------------
    def reset(self) -> SpecGamingObservation:
        import random

        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.current_task = random.choice(self.tasks)

        return SpecGamingObservation(
            task=self.current_task["name"],
            input_data=self.current_task["input"],
            instruction=self.current_task["instruction"],
            reward=0.5,   # ✅ MUST NOT be 0
            done=False,
            metadata={}
        )

    # -------------------------
    # STEP (FINAL VERSION)
    # -------------------------
    def step(self, action: SpecGamingAction) -> SpecGamingObservation:  # type: ignore[override]

        self._state.step_count += 1

        steps: List[str] = [s.lower() for s in action.steps]
        output: str = action.output.lower()

        # 🔥 ONLY USE GRADER (CRITICAL FIX)
        try:
            reward = self.current_task["grader"](action)
            reason = "graded via task grader"
        except Exception as e:
            reward = 0.1  # fallback (safe range)
            reason = f"grader error: {str(e)}"

        return SpecGamingObservation(
            task=self.current_task["name"],
            input_data=self.current_task["input"],
            instruction=self.current_task["instruction"],
            reward=float(reward),
            done=True,
            metadata={
                "reason": reason,
                "steps": steps,
                "output": output,
                "step_count": self._state.step_count
            }
        )

    # -------------------------
    # STATE
    # -------------------------
    @property
    def state(self) -> State:
        return self._state