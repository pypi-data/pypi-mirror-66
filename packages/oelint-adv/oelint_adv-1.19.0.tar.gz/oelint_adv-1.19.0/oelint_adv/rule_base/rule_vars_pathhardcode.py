from oelint_adv.cls_rule import Rule
from oelint_adv.cls_item import Variable, Comment

from collections import OrderedDict


class VarsPathHardcode(Rule):
    def __init__(self):
        super().__init__(id="oelint.vars.pathhardcode",
                         severity="warning",
                         message="<FOO>")

    def check(self, _file, stash):
        res = []
        items = stash.GetItemsFor(filename=_file)
        _map = OrderedDict({
            "/usr/lib/systemd/user": "${systemd_user_unitdir}",
            "/lib/systemd/system": "${systemd_system_unitdir}",
            "/usr/share/doc": "${docdir}",
            "/usr/share/info": "${infodir}",
            "/usr/share/man": "${mandir}",
            "/usr/libexec": "${libexecdir}",
            "/lib/systemd": "${systemd_unitdir}",
            "/usr/lib": "${libdir}",
            "/usr/bin": "${bindir}",
            "/usr/share": "${datadir}",
            "/usr/include": "${includedir}",
            "/var": "${localstatedir}",
            "/lib": "${nonarch_base_libdir}",
            "/usr/sbin": "${sbindir}",
            "/srv": "${servicedir}",
            "/com": "${sharedstatedir}",
            "/etc": "${sysconfdir}",
        })
        for i in items:
            if isinstance(i, Variable) and \
               i.VarName in ["SUMMARY", "DESCRIPTION", "HOMEPAGE", "AUTHOR", "BUGTRACKER", "FILES", "FILES_${PN}"]:
                continue
            if isinstance(i, Comment):
                continue
            _matches = []
            for k, v in _map.items():
                for pre in ["'", "\"", " ", "${D}", "="]:
                    for ext in [" ", "/", "\"", "*"]:
                        for line in i.get_items():
                            if line.strip().startswith("#"):
                                continue
                            if pre + k + ext in line and k not in _matches:
                                _cleanapp = v.strip("$").strip("{").strip("}")
                                res += self.finding(i.Origin, i.InFileLine,
                                                    "'{}' should be used instead of '{}'".format(v, k), appendix=_cleanapp)
                                _parts = [x for x in k.split("/") if x]
                                for x in range(0, len(_parts)):
                                    _matches.append("/" + "/".join(_parts[0:x]))
        return res
