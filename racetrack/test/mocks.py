class MockPlayer(object):
    def __init__(self, id=1):
        self.id = id


class MockSession(object):
    def __init__(self):
        self.added = []

    def add(self, what):
        self.added.append(what)

    def commit(self):
        pass

    def flush(self):
        for row in self.added:
            row.id = 1


class MockDb(object):
    def __init__(self):
        self.session = MockSession()


class MockPlayerChecker(object):
    def __init__(self, player):
        pass

    def exists(self):
        return False
