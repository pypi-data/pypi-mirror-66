"""sequencing tools for managing lists of actions"""
import copy
from typing import Union, List
from collections.abc import MutableSequence
from .action import Action, ConfiguredAction, TrackedAction
from .step import Step


def _ensure_configuredaction(action: Union[str, Action]) -> ConfiguredAction:
    """
    Converts the provided action into a configured action

    :param action: action to convert
    """
    if isinstance(action, ConfiguredAction):
        return action
    return ConfiguredAction(
        action
    )


class ActionList(MutableSequence):
    def __init__(self, *actions: Action):
        """
        A manager for a list of Actions.

        :param actions: actions to sequence
        """
        self._action_list: List[Action] = []
        for action in actions:
            self.append(action)

    @staticmethod
    def _ensure_type(action: Union[str, Action]) -> Action:
        """Ensures that the provided action is of the correct type for the list"""
        return Action.register_action(action)

    def __getitem__(self, item) -> Action:
        return self._action_list[item]

    def __setitem__(self, key, value: Action):
        value = self._ensure_type(value)
        self._action_list[key] = value

    def __delitem__(self, key):
        del self._action_list[key]

    def __len__(self):
        return len(self._action_list)

    def __copy__(self):
        # provides a copy of the class while preventing mutation of the actions in the instance itself
        return self.__class__(
            *[copy.copy(action) for action in self]
        )

    def insert(self, index: int, action: Action) -> None:
        """
        Inserts the provided action into the Action list

        :param index: index to insert at
        :param action: action object to insert
        :return:
        """
        action = self._ensure_type(action)
        self._action_list.insert(
            index,
            action,
        )

    @classmethod
    def create_from_steps(cls, first_step: Step) -> "ActionList":
        """
        Creates an ActionList instance from a provided step sequence. Only the first step need be provided.

        :param first_step: first step in the sequence
        :return: ActionList
        """
        # todo
        raise NotImplementedError

    def convert_to_steps(self) -> List[Step]:
        """
        Converts the ActionList instance to a series of Steps.

        :return: Series of steps
        """
        # todo
        raise NotImplementedError


class ConfiguredActionList(ActionList):
    def __init__(self, *actions: Union[Action, ConfiguredAction]):
        """
        A manager for a list of Actions.

        :param actions: actions to sequence
        """
        self._action_list: List[ConfiguredAction] = []
        super().__init__(*actions)

    @staticmethod
    def _ensure_type(action: Union[str, Action, ConfiguredAction]) -> ConfiguredAction:
        """Ensures that the provided action is of the correct type for the list"""
        if isinstance(action, ConfiguredAction):
            return copy.copy(action)
        else:
            return ConfiguredAction(action)


class TrackedActionList(ActionList):
    def __init__(self, *actions: Union[Action, ConfiguredAction, TrackedAction]):
        self._action_list: List[TrackedAction] = []
        super().__init__(*actions)

    @staticmethod
    def _ensure_type(action: Union[str, Action, ConfiguredAction, TrackedAction]) -> TrackedAction:
        """Ensures that the provided action is of the correct type for the list"""
        if isinstance(action, TrackedAction):
            return copy.copy(action)
        else:
            return TrackedAction(action)
