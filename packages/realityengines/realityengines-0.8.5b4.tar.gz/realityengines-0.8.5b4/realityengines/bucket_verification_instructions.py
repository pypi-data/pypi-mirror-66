

class BucketVerificationInstructions():
    '''

    '''

    def __init__(self, client, location=None, contents=None, verified=None, writePermission=None, authOptions=None):
        self.client = client
        self.id = None
        self.location = location
        self.contents = contents
        self.verified = verified
        self.write_permission = writePermission
        self.auth_options = authOptions

    def __repr__(self):
        return f"BucketVerificationInstructions(location={repr(self.location)}, contents={repr(self.contents)}, verified={repr(self.verified)}, write_permission={repr(self.write_permission)}, auth_options={repr(self.auth_options)})"

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id

    def to_dict(self):
        return {'location': self.location, 'contents': self.contents, 'verified': self.verified, 'write_permission': self.write_permission, 'auth_options': self.auth_options}
