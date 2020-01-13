"""File for holding custom exceptions"""


class TekstowoUnableToLogin(Exception):
    """Self-explanatory"""


class TekstowoBadSite(Exception):
    """Self-explanatory"""


class TekstowoBadJar(Exception):
    """Self-explanatory"""


class TekstowoBadObject(Exception):
    """Self-explanatory"""


class TekstowoNotLoggedIn(Exception):
    """Self-explanatory"""


def catchAndReturn(ret):
    """Add catch around function, if it fails return ret()"""
    def decorate(func):
        def call(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:  # FIXME: too broad catch
                print(f"Got exception in: {func.__name__}")
                return ret()
        return call
    return decorate
