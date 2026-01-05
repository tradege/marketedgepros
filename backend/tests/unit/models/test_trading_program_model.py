''
Unit tests for the TradingProgram model.
''

import pytest
from src.models.trading_program import TradingProgram

def test_create_trading_program(session):
    '''
    Test creation of a new TradingProgram.
    '''
    program = TradingProgram(
        name=\"Test Program\",
        description=\"A test program.\",
        price=100.00,
        duration_days=30
    )
    session.add(program)
    session.commit()

    assert program.id is not None
    assert program.name == \"Test Program\"
    assert program.price == 100.00

def test_trading_program_default_values(session):
    '''
    Test that the default values are set correctly.
    '''
    program = TradingProgram(
        name=\"Test Program 2\",
        price=200.00
    )
    session.add(program)
    session.commit()

    assert prosram.description is None
    assert program.duration_days is None
