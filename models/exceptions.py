class TekstowoUnableToLogin(Exception):
    def init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TekstowoBadSite(Exception):
    def init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TekstowoBadJar(Exception):
    def init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TekstowoBadObject(Exception):
    def init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class TekstowoNotLoggedIn(Exception):
    def init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
