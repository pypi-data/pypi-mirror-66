#
#     Kwola is an AI algorithm that learns how to use other programs
#     automatically so that it can find bugs in them.
#
#     Copyright (C) 2020 Kwola Software Testing Inc.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


from .BaseError import BaseError
from mongoengine import *
import hashlib


class ExceptionError(BaseError):
    """
        This class represents the most typical scenario of error - when an uncaught exception bubbles to the top.
    """

    stacktrace = StringField()

    message = StringField()

    source = StringField()

    lineNumber = IntField()

    columnNumber = IntField()

    def computeHash(self):
        hasher = hashlib.md5()
        hasher.update(bytes(self.stacktrace, "utf8"))

        return hasher.hexdigest()


    def generateErrorDescription(self):
        return self.stacktrace
