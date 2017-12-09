class Method(object):
    callback = False
    data = []

    def check(self):
        raise NotImplementedError('Method check not implemented in %s' % type(self).__name__)

    def correspondence(self, field):
        raise NotImplementedError('Method correspondence not implemented in %s' % type(self).__name__)

    class UserNotFound(Exception):
        pass

    class PasswordDoesNotMatch(Exception):
        pass