import datetime
from unittest.mock import MagicMock
from app.calculator_memento import CalculatorMemento
from app.calculation import Calculation

# covers line 60 of calculator_memento.py
# Steps:
    # 1: create a sample dictionary as input data.
    # 2: mock Calculation.from_dict so it returns dummy objects.
    # 3: test that CalculatorMemento.from_dict uses that data and returns a properly constructed memento object.
def test_calculator_memento_from_dict(monkeypatch):
    sample_data = {
        'history': [
            {
                'operation': 'Addition',
                'operand1': '1',
                'operand2': '2',
                'result': '3',
                'timestamp': '2023-01-01T12:00:00'
            }
        ],
        'timestamp': '2023-01-01T12:00:00'
    }

    fake_calc = MagicMock(name="CalculationInstance")
    monkeypatch.setattr(Calculation, "from_dict", lambda d: fake_calc)

    memento = CalculatorMemento.from_dict(sample_data)

    assert isinstance(memento, CalculatorMemento)
    assert memento.timestamp == datetime.datetime.fromisoformat(sample_data['timestamp'])
    assert memento.history == [fake_calc]
    

# covers line 40 of calculator_memento.py
# Steps:
    # 1: Create Calculation objects without result in the constructor, then assign result afterward.
    # 2: Create a CalculatorMemento with those calculations and a timestamp.
    # 3: Call to_dict() on the memento and assert the output dictionary contains 
        # expected keys and correctly formatted data.
def test_calculator_memento_to_dict():
    calc1 = Calculation(
        operation='Addition',
        operand1=1,
        operand2=2,
        timestamp=datetime.datetime(2023, 1, 1, 12, 0, 0)
    )
    calc1.result = 3  # assign result attribute after init

    calc2 = Calculation(
        operation='Multiplication',
        operand1=3,
        operand2=4,
        timestamp=datetime.datetime(2023, 1, 2, 13, 30, 0)
    )
    calc2.result = 12

    memento = CalculatorMemento(history=[calc1, calc2], timestamp=datetime.datetime(2023, 1, 3, 10, 0, 0))

    d = memento.to_dict()

    assert 'history' in d
    assert 'timestamp' in d
    assert isinstance(d['history'], list)
    assert all(isinstance(item, dict) for item in d['history'])
    assert d['timestamp'] == '2023-01-03T10:00:00'

    expected_keys = {'operation', 'operand1', 'operand2', 'result', 'timestamp'}
    for calc_dict in d['history']:
        assert expected_keys.issubset(calc_dict.keys())




