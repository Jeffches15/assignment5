import pytest
from unittest.mock import patch
from app.calculator_repl import calculator_repl  # or wherever your REPL function is

# covers lines 50-51 of calculator_repl.py
def test_repl_warning_on_save_history_exception(monkeypatch, capsys):
    # Create an iterator of inputs to simulate user typing "exit"
    inputs = iter(["exit"])

    # Patch input() to return next item from inputs iterator
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Patch Calculator.save_history to raise an Exception
    with patch("app.calculator.Calculator.save_history", side_effect=Exception("Simulated failure")):
        # Run REPL (should hit exit and raise the exception inside except block)
        calculator_repl()

    # Capture printed output
    captured = capsys.readouterr()

    # Assert warning message was printed
    assert "Warning: Could not save history: Simulated failure" in captured.out

# covers lines 56-63 of calculator_repl.py
@pytest.mark.parametrize("history_return, expected_output", [
    ([], "No calculations in history"),
    (["Addition(1, 2) = 3", "Multiply(3, 4) = 12"], "Calculation History:")
])
def test_history_command_output(capsys, history_return, expected_output):
    with patch('app.calculator.Calculator.show_history', return_value=history_return), \
         patch('builtins.input', side_effect=['history', 'exit']):
        calculator_repl()
        captured = capsys.readouterr()
        assert expected_output in captured.out

# covers lines 66-68 of calculator_repl.py
def test_clear_command_prints_history_cleared(capsys):
    with patch('builtins.input', side_effect=['clear', 'exit']), \
         patch('app.calculator.Calculator.clear_history') as mock_clear_history:
        
        calculator_repl()
        
        # Check that clear_history was called once
        mock_clear_history.assert_called_once()
        
        captured = capsys.readouterr()
        assert "History cleared" in captured.out

# covers lines 70-75 of calculator_repl.py
def test_undo_command_operation_undone_and_nothing_to_undo(capsys):
    # First test: undo() returns True → prints "Operation undone"
    with patch('builtins.input', side_effect=['undo', 'exit']), \
         patch('app.calculator.Calculator.undo', return_value=True) as mock_undo:
        
        calculator_repl()
        
        mock_undo.assert_called_once()
        captured = capsys.readouterr()
        assert "Operation undone" in captured.out

    # Second test: undo() returns False → prints "Nothing to undo"
    with patch('builtins.input', side_effect=['undo', 'exit']), \
         patch('app.calculator.Calculator.undo', return_value=False) as mock_undo:
        
        calculator_repl()
        
        mock_undo.assert_called_once()
        captured = capsys.readouterr()
        assert "Nothing to undo" in captured.out


# covers lines 78-82 of calculator_reply.py
# "Run this test function multiple times, each time passing in a different set of 
    # arguments as defined in the decorator"
# this function runs twice:
    # redo_return=True and expected_output="Operation redone"
    # redo_return=False and expected_output="Nothing to redo"
@pytest.mark.parametrize("redo_return, expected_output", [
    (True, "Operation redone"),
    (False, "Nothing to redo"),
])
def test_redo_command(redo_return, expected_output, capsys):
    with patch('builtins.input', side_effect=['redo', 'exit']), \
         patch('app.calculator.Calculator.redo', return_value=redo_return):
        calculator_repl()
        captured = capsys.readouterr()
        assert expected_output in captured.out



