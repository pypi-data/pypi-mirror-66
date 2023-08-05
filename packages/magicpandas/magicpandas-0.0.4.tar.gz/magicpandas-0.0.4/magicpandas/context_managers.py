import sys
import io
from contextlib import _RedirectStream

class capture(_RedirectStream):

    def __init__(self, stream='stdout'):
        self._stream = stream
        self.f = io.StringIO()
        self._new_target = self.f
        # We use a list of old targets to make this CM re-entrant
        self._old_targets = []

    def __enter__(self):
        self._old_targets.append(getattr(sys, self._stream))
        setattr(sys, self._stream, self._new_target)
        return self  # instead of self._new_target in the parent class

    def __repr__(self):
        return self.f.getvalue()
