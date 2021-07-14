class ADError(ValueError):
    pass


class ADResultError(ADError):
    def __init__(self, result, message):
        if not message:
            self.message = result['message']
        else:
            self.message = message

        self.dn = result['dn']
        super().__init__(self.message)


class NoSuchObject(ADResultError):
    def __init__(self, result):
        super().__init__(result, 'No such object: %s' % result['dn'])
