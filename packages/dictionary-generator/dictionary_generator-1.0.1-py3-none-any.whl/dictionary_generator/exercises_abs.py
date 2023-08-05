import abc
import random


class ExerciseAbstract(abc.ABC):
    @property
    @abc.abstractmethod
    def _description(self):
        """
        list of strings
        """
        pass

    def description(self):
        return random.choice(self._description)

    @property
    @abc.abstractmethod
    def _pulse(self):
        """
        min and max
        """
        pass

    def pulse(self):
        return random.randint(self._pulse[0], self._pulse[1])

    @property
    @abc.abstractmethod
    def _state_of_health(self):
        """
        list of strings
        """
        pass

    def state_of_health(self):
        return random.choice(self._state_of_health)
