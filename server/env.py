from uuid import uuid4
from typing import List, Any, Dict
import random

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from .models import SpecGamingAction, SpecGamingObservation
# Note: We import TASKS from .tasks to keep a single source of truth
from .tasks import (
    TASKS, 
    grade_data_cleaning, 
    grade_financial, 
    grade_instruction,
    normalize_score
)

# =========================
# 🌍 ENVIRONMENT
# =========================
class SpecGamingEnvironment(Environment):
    """
    OpenEnv compliant environment for SpecGuard tasks.
    """
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    tasks = TASKS

    def __init__(self):
        super().__init__()
        self.tasks = TASKS 
        
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.current_task = None
        self.task_index = 0
        
        # Internal mapping for string-based grader lookups if needed
        self._grader_map = {
            "grade_data_cleaning": grade_data_cleaning,
            "grade_financial": grade_financial,
            "grade_instruction": grade_instruction
        }

    # -------------------------
    # RESET
    # -------------------------
    def reset(self) -> SpecGamingObservation:
        """
        Resets the environment and cycles to the next task.
        """
        self._state = State(episode_id=str(uuid4()), step_count=0)

        # 🔥 Cycle through tasks to ensure all 3 are validated by the agent
        self.current_task = self.tasks[self.task_index % len(self.tasks)]
        self.task_index += 1

        return SpecGamingObservation(
            task=self.current_task["name"],
            input_data=self.current_task["input"],
            instruction=self.current_task["instruction"],
            # Initial reward must be > 0.0 and < 1.0 for Phase 2 compliance
            reward=0.10,
            done=False,
            metadata={
                "task_id": self.current_task["id"],
                "required_steps": self.current_task.get("required_steps", [])
            }
        )

    # -------------------------
    # STEP
    # -------------------------
    def step(self, action: SpecGamingAction) -> SpecGamingObservation:
        self._state.step_count += 1
        
        try:
            grader = self.current_task.get("grader")
            
            # Use the map only as a fallback for strings, otherwise call directly
            if isinstance(grader, str):
                reward = self._grader_map.get(grader, lambda x: 0.10)(action)
            elif callable(grader):
                reward = grader(action)
            else:
                reward = 0.10
                
            reason = "graded via task grader"
        except Exception as e:
            reward = 0.10
            reason = f"grader error: {str(e)}"

        return SpecGamingObservation(
            task=self.current_task["name"],
            input_data=self.current_task["input"],
            instruction=self.current_task["instruction"],
            reward=float(reward),
            done=True,
            metadata={
                "reason": reason,
                "steps": action.steps,
                "output": action.output,
                "step_count": self._state.step_count
            }
        )

    # -------------------------
    # STATE
    # -------------------------
    @property
    def state(self) -> State:
        return self._state


# =========================
# 🔥 EXPORTS (CRITICAL)
# =========================
__all__ = [
    "SpecGamingEnvironment",
    "TASKS"
]