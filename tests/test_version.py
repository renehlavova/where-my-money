from where_my_money.version import __version__

def test_version():
    assert __version__
    assert "." in __version__
    assert __version__ > "0.0.0"
