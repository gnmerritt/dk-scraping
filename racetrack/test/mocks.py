class MockPlayer(object):
    id = 1


class MockSession(object):
    def __init__(self):
        self.added = []

    def add(self, what):
        self.added.append(what)

    def commit(self):
        pass


class MockDb(object):
    def __init__(self):
        self.session = MockSession()
