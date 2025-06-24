import pytest
from unittest.mock import patch, MagicMock
from app.calculator_repl import calculator_repl  # or wherever your REPL function is
from decimal import Decimal
from app.calculator import Calculator
from app.exceptions import ValidationError, OperationError


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


# covers lines 85-90 in calculator_repl.py
@pytest.mark.parametrize("side_effect,expected_output", [
    (None, "History saved successfully"),
    (Exception("fail"), "Error saving history: fail"),
])
def test_save_command(monkeypatch, capsys, side_effect, expected_output):
    calc_mock = MagicMock()
    calc_mock.save_history.side_effect = side_effect

    # patch where Calculator is used
        # Calculator is used in calculator_repl, but defined in calculator
    with patch('app.calculator_repl.Calculator', return_value=calc_mock):
        inputs = iter(['save', 'exit'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        calculator_repl()
        
        out = capsys.readouterr().out
        assert expected_output in out


# covers lines 93-98 in calculator_repl.py
@pytest.mark.parametrize("side_effect, expected_output", [
    (None, "History loaded successfully"),
    (Exception("load failed"), "Error loading history: load failed"),
])
def test_load_command(monkeypatch, capsys, side_effect, expected_output):
    mock_calc = MagicMock()
    if side_effect:
        mock_calc.load_history.side_effect = side_effect

    # patch where Calculator is used
    with patch("app.calculator_repl.Calculator", return_value=mock_calc):
        inputs = iter(["load", "exit"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        calculator_repl()

        output = capsys.readouterr().out
        assert expected_output in output

# covers lines 105-106 in calculator_repl.py
def test_cancel_first_operand(monkeypatch, capsys):
    inputs = iter(['add', 'cancel', 'exit'])  # 'cancel' triggers the 'Operation cancelled' branch
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # patch where Calculator is used
    with patch('app.calculator_repl.Calculator') as mock_calc:
        calculator_repl()
        out = capsys.readouterr().out

        assert "Operation cancelled" in out

# covers lines 110-111 in calculator_repl.py
def test_cancel_second_operand(monkeypatch, capsys):
    inputs = iter(['add', '5', 'cancel', 'exit'])  # First number is valid, second is 'cancel'
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    # patch where Calculator is used
    with patch('app.calculator_repl.Calculator') as mock_calc:
        calculator_repl()
        output = capsys.readouterr().out

        assert "Operation cancelled" in output



# covers lines 125-130 in calculator_repl.py
@pytest.mark.parametrize("side_effect, expected_output", [
    (ValidationError("Invalid input"), "Error: Invalid input"),
    (OperationError("Calculation failed"), "Error: Calculation failed"),
    (Exception("Unexpected failure"), "Unexpected error: Unexpected failure"),
])
def test_exception_handling_in_repl(monkeypatch, capsys, side_effect, expected_output):
    calc_mock = MagicMock()
    # Simulate perform_operation raising different exceptions depending on test
    calc_mock.perform_operation.side_effect = side_effect

    with patch('app.calculator_repl.Calculator', return_value=calc_mock):
        inputs = iter([
            'add',         # command triggers calculation
            '1',           # first operand
            '2',           # second operand
            'exit'         # exit REPL after test
        ])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        calculator_repl()

        out = capsys.readouterr().out
        assert expected_output in out

# covers lines 134-135 of calculator_repl.py
def test_unknown_command_prints_message(monkeypatch, capsys):
    inputs = iter(['foobar', 'exit'])  # 'foobar' is unknown command, then exit to stop loop

    # Replace the built-in input() function temporarily during the test.
    # Instead of waiting for actual user input (which would hang the test), 
    # it uses a fake input function that returns the next value from the inputs iterator each time it’s called.
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    calculator_repl()
    
    # Capture everything that was printed to the console during the test.
    # capsys is a pytest built-in fixture that grabs all stdout and stderr output.
    output = capsys.readouterr().out
    assert "Unknown command: 'foobar'. Type 'help' for available commands" in output


# covers lines 136-139 of calculator_repl.py
def test_repl_handles_keyboard_interrupt(monkeypatch, capsys):
    inputs = iter(['\x03', 'exit'])  # '\x03' simulates Ctrl+C (KeyboardInterrupt)

    def fake_input(prompt):
        val = next(inputs)
        if val == '\x03':
            raise KeyboardInterrupt
        return val

    monkeypatch.setattr('builtins.input', fake_input)

    calculator_repl()

    captured = capsys.readouterr().out
    assert "Operation cancelled" in captured

# covers lines 140-143 of calculator_repl.py
def test_repl_handles_eof_error(monkeypatch, capsys):
    inputs = iter(['\x04', 'exit'])  # '\x04' simulates Ctrl+D (EOFError)

    def fake_input(prompt):
        val = next(inputs)
        if val == '\x04':
            raise EOFError
        return val

    monkeypatch.setattr('builtins.input', fake_input)

    calculator_repl()

    captured = capsys.readouterr().out
    assert "Input terminated. Exiting..." in captured


# covers lines 144-147 of calculator_repl.py


# covers 148-153 of calculator_repl.py
def test_fatal_error_during_initialization(capsys):
    with patch('app.calculator_repl.Calculator', side_effect=Exception("Initialization failed")), \
         patch('app.calculator_repl.logging') as mock_logging:
        with pytest.raises(Exception) as exc_info:
            calculator_repl()

        # Check printed output contains fatal error message
        out = capsys.readouterr().out
        assert "Fatal error: Initialization failed" in out

        # Check logging.error called with expected message
        mock_logging.error.assert_called_with("fatal error in calculator REPL: Initialization failed")

        # Check exception re-raised with correct message
        assert "Initialization failed" in str(exc_info.value)

        