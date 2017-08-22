class Method:
    callback = False

    def check(self):
        raise NotImplementedError('Method check not implemented in %s' % type(self).__name__)