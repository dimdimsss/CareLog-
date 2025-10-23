import pytest
import app

def test_test():
    test = "test"

    assert test == "test"

def test_load_user():


    user_object = app.utils.load_user("p001")

    assert user_object.name == "Jacob Johnson"
    assert user_object.password == "patient"
    assert user_object.role == "Patient"


