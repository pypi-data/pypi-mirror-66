# prcs.py - PRCS source for the Mercurial convert extension
# Copyright (C) 2015-2020 Kaz Nishimura
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
PRCS source for the Mercurial convert extension
"""

from __future__ import absolute_import, unicode_literals

import re
from hgext.convert.common import NoRepo, commit, converter_source
from mercurial.util import unlinkpath
from prcslib import PrcsVersion, PrcsProject, PrcsError

# Regular expression pattern that checks for main branches.
_MAIN_BRANCH_RE = re.compile(r"^(\d+)$")

class prcs_source(converter_source):
    """
    PRCS source class.
    """

    def __init__(self, ui, scm, path, revs=None):
        """
        initialize a PRCS source
        """
        super(prcs_source, self).__init__(ui, scm, path, revs)

        try:
            self._project = PrcsProject(path.decode())
            self._versions = self._project.versions()
        except PrcsError:
            raise NoRepo(b"%s does not look like a PRCS project" % path)

        self._cached_descriptor = {}

    def _descriptor(self, version):
        """Return a revision descriptor with caching."""
        if version in self._cached_descriptor:
            return self._cached_descriptor[version]

        descriptor = self._project.descriptor(version)
        self._cached_descriptor[version] = descriptor
        return descriptor

    def _nearest_ancestor(self, version):
        """Return an indirect parent for a deleted version."""
        if version is None:
            return None
        if isinstance(version, str):
            version = PrcsVersion(version)

        deleted = False
        while self._versions[str(version)]['deleted']:
            self.ui.note(version, " is deleted\n")
            deleted = True
            version = PrcsVersion(version.major(), version.minor() - 1)
            if version.minor() == 0:
                self.ui.note("No more ancestors on branch ", version.major())
                return None
        if deleted:
            self.ui.note("substituting ", version, "\n")
        return version

    def getheads(self):
        """
        return all the head versions of the PRCS source
        """
        last_minors = {}
        for key in self._versions:
            if not self._versions[key]["deleted"]:
                version = PrcsVersion(key)
                if last_minors.get(version.major(), 0) < version.minor():
                    last_minors[version.major()] = version.minor()
        return map(
            lambda item: str(PrcsVersion(*item)).encode(),
            last_minors.items())

    def getfile(self, name, rev):
        """
        Return the content and mode of a file as a 'tuple' value
        """
        if rev is None:
            return None, None

        rev = rev.decode()
        descriptor = self._descriptor(rev)
        files = descriptor.files()
        if not name.decode() in files:
            self.ui.debug(b"%s not found for %s" % (name, rev.encode()))
            return None, None

        attr = files[name.decode()]
        if "symlink" in attr:
            return attr["symlink"].encode(), b"l"

        self._project.checkout(rev, files=[name.decode()])

        try:
            with open(name, "rb") as stream:
                content = stream.read()
        finally:
            unlinkpath(name)

        return content, b"x" if attr["mode"] & (0x1 << 6) else b""

    def _removedfiles(self, files, parentfiles):
        """
        Return a (files, copies) tuple for removed or renamed files.
        """
        changes = []
        copies = {}
        pnamebyid = {}
        for pname, pa in parentfiles.items():
            if pname not in files:
                changes.append((pname.encode(), None))
            if "symlink" not in pa:
                pnamebyid[pa['id']] = pname
        # To process renamed files for copies.
        for name, attr in files.items():
            if not "symlink" in attr and attr['id'] in pnamebyid:
                pname = pnamebyid[attr['id']]
                if name != pname:
                    self.ui.note(b"%s was renamed to %s\n" % \
                        (pname.encode(), name.encode()))
                    copies[name.encode()] = pname.encode()
        return changes, copies

    def getchanges(self, version, full=False):
        version = version.decode()
        descriptor = self._descriptor(version)

        files = []
        copies = {}
        f = descriptor.files()
        parent = descriptor.parent()
        # Preparing for a deleted parent.
        parent = self._nearest_ancestor(parent)
        if full or parent is None:
            # This is the initial checkin so all files are affected.
            for name in f:
                files.append((name.encode(), version.encode()))
        else:
            pf = self._descriptor(parent).files()
            # Handling added or changed files.
            for name, a in f.items():
                if name in pf:
                    pa = pf[name]
                    if "symlink" in a:
                        if "symlink" not in pa:
                            # Changed from a regular file to a symlink.
                            files.append((name.encode(), version.encode()))
                    elif "symlink" in pa:
                        # Changed from a symlink to a regular file.
                        files.append((name.encode(), version.encode()))
                    elif a['id'] != pa['id'] \
                            or a['revision'] != pa['revision'] \
                            or (a['mode'] ^ pa['mode']) & (0x1 << 6):
                        files.append((name.encode(), version.encode()))
                else:
                    # Added.
                    files.append((name.encode(), version.encode()))
            # To process removed or renamed files.
            removes, copies = self._removedfiles(f, pf)
            files.extend(removes)
        return files, copies, set()

    def getcommit(self, version):
        version = version.decode()
        revision = self._versions[version]
        descriptor = self._descriptor(version)

        parents = []
        parent = descriptor.parent()
        # Preparing for a deleted parent.
        parent = self._nearest_ancestor(parent)
        if not parent is None:
            parents.append(str(parent).encode())
        for mp in descriptor.mergeparents():
            # Preparing for a deleted merge parent.
            mp = self._nearest_ancestor(mp)
            if mp is not None:
                parents.append(str(mp).encode())

        branch = PrcsVersion(version).major()
        if _MAIN_BRANCH_RE.match(branch):
            branch = None
        return commit(
            revision['author'].encode(), revision['date'].isoformat().encode(),
            descriptor.message().encode(), parents, branch)

    def numcommits(self):
        """
        Return the number of commits.
        """
        return len(self._versions)

    def gettags(self):
        """Return an empty dictionary since PRCS has no tags."""
        return {}
