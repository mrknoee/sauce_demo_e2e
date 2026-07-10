
PASSWORD = "secret_sauce"

LOCKED_OUT_ERROR = "Epic sadface: Sorry, this user has been locked out."
INVALID_CREDENTIALS_ERROR = "Epic sadface: Username and password do not match any user in this service"

STANDARD_USER = {"username": "standard_user", "password": PASSWORD, "should_login": True}
LOCKED_OUT_USER = {"username": "locked_out_user", "password": PASSWORD, "should_login": False, "expected_error": LOCKED_OUT_ERROR}
PROBLEM_USER = {"username": "problem_user", "password": PASSWORD, "should_login": True}
PERFORMANCE_GLITCH_USER = {"username": "performance_glitch_user", "password": PASSWORD, "should_login": True}
ERROR_USER = {"username": "error_user", "password": PASSWORD, "should_login": True}
VISUAL_USER = {"username": "visual_user", "password": PASSWORD, "should_login": True}

# Test user cases for parametrize
LOGIN_CASES = [
    (STANDARD_USER["username"], STANDARD_USER),
    (LOCKED_OUT_USER["username"], LOCKED_OUT_USER),
    (PROBLEM_USER["username"], PROBLEM_USER),
    (PERFORMANCE_GLITCH_USER["username"], PERFORMANCE_GLITCH_USER),
    (ERROR_USER["username"], ERROR_USER),
    (VISUAL_USER["username"], VISUAL_USER),
]
