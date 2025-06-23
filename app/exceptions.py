### Exception hierarchy ###

# This code defines a custom exception hierarchy for a 
# calculator application — a clean way to manage and categorize errors specific to that project.

# The pass statement is a no-op — it literally does nothing. 
# It acts as a placeholder when Python expects a statement but you don’t want to write any logic yet.

class CalculatorError(Exception):
    """
    Base exception class for calculator-specific errors

    all custom exceptions for the calculator application inherit from this class,
    allowing for unified error handling
    """
    pass

class ValidationError(CalculatorError):
    """
    Raised when input validation fails

    this exception is triggered when user inputs do not meet the required criteria,
    such as entering non-numeric values or exceeding maximum allowed values
    """
    pass

class OperationError(CalculatorError):
    """
    Raised when a calculation operation fails

    this exception is used to indicate failures during the execution of arithmetic
    operations, such as division by zero or invalid operations
    """
    pass

class ConfigurationError(CalculatorError):
    """
    Raised when calculator configuration is invalid

    triggered when there are issues with the calculator's configuration settings,
    such as invalid directory paths or improper configuration values
    """