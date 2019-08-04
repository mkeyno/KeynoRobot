"""Module containing exceptions raised by twine."""
# Copyright 2015 Ian Stapleton Cordasco
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
print(__name__)

class KeynoException(Exception):
    """Base class for all exceptions raised by twine."""

    pass

class InputError(KeynoException):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class TransitionError(KeynoException):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message
		
		
class RedirectDetected(KeynoException):
    """A redirect was detected that the user needs to resolve.

    In some cases, requests refuses to issue a new POST request after a
    redirect. In order to prevent a confusing user experience, we raise this
    exception to allow users to know the index they're uploading to is
    redirecting them.
    """

    pass


class PackageNotFound(KeynoException):
    """A package file was provided that could not be found on the file system.

    This is only used when attempting to register a package.
    """

    pass


class UploadToDeprecatedPyPIDetected(KeynoException):
    """An upload attempt was detected to deprecated PyPI domains.

    The sites pypi.python.org and testpypi.python.org are deprecated.
    """

    @classmethod
    def from_args(cls, target_url, default_url, test_url):
        """Return an UploadToDeprecatedPyPIDetected instance."""
        return cls("You're trying to upload to the legacy PyPI site '{}'. "
                   "Uploading to those sites is deprecated. \n "
                   "The new sites are pypi.org and test.pypi.org. Try using "
                   "{} (or {}) to upload your packages instead. "
                   "These are the default URLs for Twine now. \n More at "
                   "https://packaging.python.org/guides/migrating-to-pypi-org/"
                   " .".format(target_url, default_url, test_url)
                   )
				   


class UnreachableRepositoryURLDetected(KeynoException):
    """An upload attempt was detected to a URL without a protocol prefix.

    All repository URLs must have a protocol (e.g., ``https://``).
    """

    pass


class InvalidSigningConfiguration(KeynoException):
    """Both the sign and identity parameters must be present."""

    pass


class InvalidConfiguration(KeynoException):
    """Raised when configuration is invalid."""

    pass


class InvalidDistribution(KeynoException):
    """Raised when a distribution is invalid."""

    pass
