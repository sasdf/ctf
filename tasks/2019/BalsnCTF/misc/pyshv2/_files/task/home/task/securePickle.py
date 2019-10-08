import pickle
import io


whitelist = []


# See https://docs.python.org/3.7/library/pickle.html#restricting-globals
class RestrictedUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if module not in whitelist or '.' in name:
            raise KeyError('The pickle is spoilt :(')
        module = __import__(module)
        return getattr(module, name)


def loads(s):
    """Helper function analogous to pickle.loads()."""
    return RestrictedUnpickler(io.BytesIO(s)).load()


dumps = pickle.dumps
