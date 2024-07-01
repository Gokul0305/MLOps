from abc import ABC, abstractmethod


# Define an abstract base class for edge detection strategies
class EdgeDetectionStrategy(ABC):
    @abstractmethod
    def detect_edges(self, previous_states: list,
                     current_states: list) -> list:
        """
        Abstract method to detect edges in a sequence of states.

        Args:
            previous_states (list): List of previous states.
            current_states (list): List of current states.

        Returns:
            list: Indices of detected edges.
        """
        pass


# Implementation of a strategy for detecting rising edges
class RisingEdgeDetection(EdgeDetectionStrategy):
    def detect_edges(self, previous_states, current_states):
        """
        Detects rising edges in a sequence of states.

        Args:
            previous_states (list): List of previous states.
            current_states (list): List of current states.

        Returns:
            list: Indices of detected rising edges.
        """
        rising_edges = []
        for i in range(len(current_states)):
            previous_state = previous_states[i]
            current_state = current_states[i]
            if current_state == 1 and previous_state == 0:
                rising_edges.append(i)  # Rising edge detected
        return rising_edges


# Implementation of a strategy for detecting falling edges
class FallingEdgeDetection(EdgeDetectionStrategy):
    def detect_edges(self, previous_states, current_states):
        """
        Detects falling edges in a sequence of states.

        Args:
            previous_states (list): List of previous states.
            current_states (list): List of current states.

        Returns:
            list: Indices of detected falling edges.
        """
        falling_edges = []
        for i in range(len(current_states)):
            previous_state = previous_states[i]
            current_state = current_states[i]
            if current_state == 0 and previous_state == 1:
                falling_edges.append(i)  # Falling edge detected
        return falling_edges
