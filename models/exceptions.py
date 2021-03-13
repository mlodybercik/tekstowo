"""File for holding custom exceptions"""


class TekstowoUnableToLogin(BaseException):
    """Self-explanatory"""


class TekstowoBadSite(BaseException):
    """Self-explanatory"""


class TekstowoBadJar(BaseException):
    """Self-explanatory"""


class TekstowoBadObject(BaseException):
    """Self-explanatory"""


class TekstowoNotLoggedIn(BaseException):
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
