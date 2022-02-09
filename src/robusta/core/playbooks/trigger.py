from pydantic import PrivateAttr

from .base_trigger import BaseTrigger
from ..triggers.custom_triggers import CustomTriggers
from ...integrations.prometheus.trigger import PrometheusAlertTriggers
from ...integrations.kubernetes.autogenerated.triggers import K8sTriggers
from ...integrations.scheduled.trigger import ScheduledTriggers


class Trigger(K8sTriggers, PrometheusAlertTriggers, ScheduledTriggers, CustomTriggers):
    _trigger: BaseTrigger = PrivateAttr()

    def __init__(self, *args, **data):
        super().__init__(*args, **data)
        trigger_keys = [trigger for trigger in dir(self) if not trigger.startswith("_")]
        triggers = []
        for key in trigger_keys:
            trigger_def = getattr(self, key)
            if trigger_def is not None and isinstance(trigger_def, BaseTrigger):
                triggers.append(trigger_def)
        if len(triggers) != 1:
            raise Exception("Exactly one trigger type must be defined")
        self._trigger = triggers[0]

    def get(self) -> BaseTrigger:
        return self._trigger
