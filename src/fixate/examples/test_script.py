"""
This is a test script that shows basic use case for the fixate library
"""
from fixate.core.common import TestClass
from fixate.core.checks import *
from fixate.core.ui import *


class RedButton(TestClass):
    """
    Asks the user to push the red button
    """

    test_desc = "Red Button"

    def test(self):
        user_ok("Please Push the Red Button\n")
        chk_passes("Red Button Pushed")


class ReturnTrue(TestClass):
    """
    Just passes and returns True
    """

    test_desc = "Return True"

    def test(self):
        chk_equal(True, True)


class ReturnFalse(TestClass):
    """
    Just fails and returns False
    """

    test_desc = "Fail False"

    def test(self):
        chk_equal(False, True)


class RaiseValueError(TestClass):
    """
    Raises a value error before making a comparison
    """

    test_desc = "Raise Value Error"

    def test(self):
        raise ValueError("Things be broken")


class RaiseValueErrorInComparison(TestClass):
    """
    Comparison Value Error <- If test_desc not present than this is the test_desc
    Raises a value error during a comparison <- If test_desc not present than this is the test_desc_long
    """

    def test(self):
        chk_in_range("HI", 5, 10)


class GetUserInput(TestClass):
    """
    Raises a value error
    """

    test_desc = "Get Input from User"

    def enter(self):
        self.retry_type = self.RT_PROMPT

    def test(self):
        get_input = user_input("What is 1 + 1?\n")
        chk_equal(int(get_input), 2)


class MultiplePassedTestResults(TestClass):
    """
    This class has multiple test results
    """

    test_desc = "Multiple passed results"

    def test(self):
        chk_log_value("Result 1")
        chk_log_value("Result 2")

    def tear_down(self):
        user_info("Tearing down this function")


class ParameterisedTest(TestClass):
    """
    This class uses the init function to build a set of parameters used in the test function
    """

    test_desc = "Parameterised Test Function"
    class_param = "Class Param"
    class_param_override = "Override Me"

    def __init__(self, frequency, time, **kwargs):
        super().__init__(**kwargs)
        self.frequency = frequency
        self.time = time
        self.class_param_override = "Overridden"

    def test(self):
        chk_equal(
            self.class_param_override,
            "Overridden",
            description="Checking that parameter is overridden",
        )
        chk_equal(self.class_param, "Class Param")
        chk_log_value(
            f"Frequency {self.frequency}",
            description="Just outputting the frequency",
        )
        chk_log_value(f"Time {self.time}")
        user_info("This won't be in the report")
        chk_passes("This will be in the report")


SHOULD_I_PASS = False


class PassEverySecondAttempt(TestClass):
    """
    Only passes if the global is True
    """

    attempts = 5

    def test(self):
        chk_equal(SHOULD_I_PASS, True, description="Checking state of SHOULD_I_PASS")

    def tear_down(self):
        global SHOULD_I_PASS
        SHOULD_I_PASS = not SHOULD_I_PASS


class PassEverySecondAttemptThrowOthers(PassEverySecondAttempt):
    """
    Only passes if the global is True
    Throws Exceptions other times
    """

    def test(self):
        chk_equal(SHOULD_I_PASS, True, description="Checking state of SHOULD_I_PASS")
        if not SHOULD_I_PASS:
            raise Exception("This should throw exception if SHOULD_I_PASS is False")


class MultipleLineInstruction(TestClass):
    """
    Multiple line instruction
    """

    def test(self):
        user_info("Line 1")
        user_info("Line 2")
        user_info("Line 3")
        user_info("Line 4")
        user_ok("Line 5")


class PostSequenceInfo(TestClass):
    def test(self):
        user_post_sequence_info("Post sequence info is here and should always be here")
        user_post_sequence_info_pass(
            "Post sequence info that should only show if sequence passes"
        )
        user_post_sequence_info_fail(
            "Post sequence info that should only show if sequence fails"
        )


class CheckPostSequenceInfo(TestClass):
    def test(self):
        user_info(
            "When the sequence finishes, check the following in the active and history window:"
        )
        user_info("Post sequence info is here and should always be here")
        user_ok(
            "Post sequence info that should only show if sequence x where x is passes or fails"
        )


PASSES = [
    PostSequenceInfo(),
    CheckPostSequenceInfo(),
    ReturnTrue(),
    RedButton(),
    GetUserInput(),
    MultiplePassedTestResults(),
    ReturnTrue(),
    ParameterisedTest(50, 500),
    ReturnTrue(),
    ParameterisedTest(10, 5),
    PassEverySecondAttempt(),
    PassEverySecondAttemptThrowOthers(),
    MultipleLineInstruction(),
    CheckPostSequenceInfo(),
]
FAILS = [
    PostSequenceInfo(),
    CheckPostSequenceInfo(),
    ReturnFalse(),
    ParameterisedTest(50, 500),
    ParameterisedTest(10, 5),
    MultipleLineInstruction(),
    CheckPostSequenceInfo(),
]
ERRORS = [
    PostSequenceInfo(),
    CheckPostSequenceInfo(),
    RaiseValueError(),
    RaiseValueErrorInComparison(),
    ParameterisedTest(10, 5),
    MultipleLineInstruction(),
    CheckPostSequenceInfo(),
]

TEST_SEQUENCE = PASSES

test_data = {"default": PASSES, "passes": PASSES, "fails": FAILS, "errors": ERRORS}
