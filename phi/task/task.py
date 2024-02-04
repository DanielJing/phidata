from uuid import uuid4
from typing import List, Any, Optional, Dict, Union, Type, Iterator

from pydantic import BaseModel, ConfigDict, field_validator

from phi.memory.assistant import AssistantMemory
from phi.utils.log import logger, set_log_level_to_debug


class Task(BaseModel):
    # -*- Task settings
    # Task UUID (autogenerated if not set)
    task_id: Optional[str] = None
    # Task name
    task_name: Optional[str] = None

    # -*- Assistant state
    assistant_name: Optional[str] = None
    assistant_memory: Optional[AssistantMemory] = None

    # -*- Run state
    run_id: Optional[str] = None
    run_message: Optional[Union[List, Dict, str]] = None
    run_task_data: Optional[List[Dict[str, Any]]] = None

    # -*- Task Output Settings
    # Provide an output model for the responses
    output_model: Optional[Union[str, List, Type[BaseModel]]] = None
    # If True, the output is converted into the output_model (pydantic model or json dict)
    parse_output: bool = True
    # -*- Final output of this Task
    output: Optional[Any] = None
    # If True, shows the output of the task in the assistant.run()
    show_output: bool = True

    # If True, enable debug logs
    debug_mode: bool = False

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("debug_mode", mode="before")
    def set_log_level(cls, v: bool) -> bool:
        if v:
            set_log_level_to_debug()
            logger.debug("Debug logs enabled")
        return v

    @property
    def streamable(self) -> bool:
        return False

    def set_task_id(self) -> None:
        if self.task_id is None:
            self.task_id = str(uuid4())

    def prepare_task(self) -> None:
        self.set_task_id()

    def run(
        self,
        message: Optional[Union[List, Dict, str]] = None,
        stream: bool = True,
        **kwargs: Dict[str, Any],
    ) -> Union[Iterator[str], str, BaseModel]:
        raise NotImplementedError

    def to_dict(self) -> Dict[str, Any]:
        _dict = {
            "task_id": self.task_id,
            "task_name": self.task_name,
            "output": self.output,
        }
        return _dict
