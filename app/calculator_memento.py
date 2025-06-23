### calculator memento

from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List

from app.calculation import Calculation

# to_dict() is an instance method because it needs access 
    # to self — it works on an existing object.

# from_dict() is a class method because it creates a new object from a dictionary, 
    # and doesn’t require an existing instance.

# to_dict() → Take a machine and draw blueprints from it
# from_dict() → Take blueprints and build a machine from them

@dataclass
class CalculatorMemento:
    """
    Stores calculator state for undo/redo functionality

    The memento pattern allows the calculator to save its current state (history)
    so that it can be restored later. This enables features like undo and redo
    """

    history: List[Calculation] # list of Calculation instances representing the calculator's history
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now) # time when the memento was created

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert memento to dictionary.

        This method serializes the memento's state into a dictionary format,
        making it easy to store or transmit.

        Returns:
            Dict[str, Any]: A dictionary containing the serialized state of the memento.
        """
        return {
            # For every calc in self.history, call calc.to_dict() and store the result in a list.
            'history': [calc.to_dict() for calc in self.history],
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CalculatorMemento':
        """
        Create memento from dictionary.

        This class method deserializes a dictionary to recreate a CalculatorMemento
        instance, restoring the calculator's history and timestamp.

        Args:
            data (Dict[str, Any]): Dictionary containing serialized memento data.

        Returns:
            CalculatorMemento: A new instance of CalculatorMemento with restored state.
        """
        return cls(
            history=[Calculation.from_dict(calc) for calc in data['history']],
            timestamp=datetime.datetime.fromisoformat(data['timestamp'])
        )
