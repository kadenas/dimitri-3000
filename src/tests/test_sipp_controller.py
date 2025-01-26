import pytest
from core.sipp_controller import SIPPController

def test_sipp_controller_initialization():
    """Test basic initialization of SIPP controller."""
    controller = SIPPController({})
    assert controller.initialize() is True

def test_scenario_creation():
    """Test scenario creation."""
    controller = SIPPController({})
    assert controller.create_scenario("uac") is True