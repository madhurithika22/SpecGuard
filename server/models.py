from openenv.core.env_server.types import Action, Observation
from pydantic import Field
from typing import List, Dict, Any


class SpecGamingAction(Action):
    """
    Action sent by the agent.

    Includes:
    - steps: reasoning steps taken
    - output: final answer
    """

    steps: List[str] = Field(
        ...,
        description="Reasoning steps followed by the agent"
    )

    output: str = Field(
        ...,
        description="Final output of the agent"
    )


class SpecGamingObservation(Observation):
    """
    Observation returned by the environment.
    """

    task: str = Field(
        ...,
        description="Current task name"
    )

    input_data: Dict[str, Any] = Field(
        ...,
        description="Input data for the task"
    )

    instruction: str = Field(
        ...,
        description="Task instruction"
    )

    reward: float = Field(
        default=0.0,
        description="Reward assigned after action"
    )

    done: bool = Field(
        default=False,
        description="Whether episode is complete"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional debugging and evaluation info"
    )