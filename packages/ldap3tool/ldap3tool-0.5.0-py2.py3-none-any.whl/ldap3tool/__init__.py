#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ldap3 import Connection, Server, SUBTREE

__version__ = "0.5.0"

DEFAULT_ATTRIBUTES = [
    "manager",
    "employeeNumber",
    "employeeID",
    "cn",
    "name",
    "extensionAttribute14",
    "displayName",
    "sAMAccountName",
    "mail",
    "title",
    "department",
    "telephoneNumber",
    "mobile",
    "directReports",
]
NAME_MAPS = dict(
    display="displayName",
    name="sAMAccountName",
    email="mail",
    mail="mail",
    phone="telephoneNumber",
    number="employeeNumber",
    mobile="mobile",
)
COMMON_FILTERS = dict(
    display="(displayName={})",
    name="(sAMAccountName={})",
    email="(mail={})",
    phone="(telephoneNumber={})",
    number="(employeeNumber={})",
    mobile="(mobile={})",
)


def get_operators(maps, op="|"):
    if isinstance(maps, dict):
        items = maps.items()
    else:
        items = maps

    ops = []
    for k, v in items:
        k = NAME_MAPS.get(k, k)
        if isinstance(v, (list, tuple)):
            ops.extend(["({}={})".format(k, v_) for v_ in v])
        else:
            ops.append("({}={})".format(k, v))

    if len(ops) > 1:
        ops.insert(0, "({}".format(op))
        ops.append(")")

    return "".join(ops)


class LDAPTool(object):
    def __init__(self, **kwargs):
        self.server = kwargs.get("server")
        self.base_dn = kwargs.get("base_dn")
        self.search_scope = kwargs.get("search_scope") or SUBTREE
        self.retrive_attrs = kwargs.get("retrive_attrs", DEFAULT_ATTRIBUTES)
        self.version = kwargs.get("version", 3)
        self.conn = None

    def open_server(self, **kwargs):
        return Server(kwargs.pop("server", self.server), **kwargs)

    def connect(self, username, password, **kwargs):
        auto_bind = kwargs.pop("auto_bind", True)
        self.conn = Connection(
            kwargs.pop("server", self.server),
            user=username,
            password=password,
            auto_bind=auto_bind,
            **kwargs
        )
        return self.conn

    def close(self):
        self.conn.unbind()

    def parse_info(self, attrs=None):
        if not attrs:
            attrs = {}

        manager = (attrs.get("manager") or "").strip().split(",", 1)[0]
        number = (attrs.get("employeeNumber") or "").strip()
        if not number:
            number = (attrs.get("employeeID") or "").strip()

        alias_name = (attrs.get("extensionAttribute14") or "").strip()
        full_name = (attrs.get("displayName") or "").strip()
        cn = (attrs.get("cn") or "").strip()
        name = (attrs.get("name") or "").strip()
        if not alias_name:
            alias_name = full_name or cn or name

        if not full_name:
            full_name = alias_name or name or cn

        reports = attrs.get("directReports") or []
        reports_to = [
            r.split(",", 1)[0].split("=")[-1].strip() for r in reports
        ]
        mobile = attrs.get("mobile") or ""
        if isinstance(mobile, list):
            mobile = ", ".join(m.strip().lower() for m in mobile)

        return dict(
            ntname=attrs["sAMAccountName"].strip().lower(),
            full_name=full_name,
            alias_name=alias_name,
            email=(attrs.get("mail") or "").strip().lower(),
            manager=manager.split("=")[-1].strip(),
            title=(attrs.get("title") or "").strip().upper(),
            department=(attrs.get("department") or "").strip().upper(),
            phone=(attrs.get("telephoneNumber") or "").strip().lower(),
            mobile=mobile,
            number=number,
            reports_to=reports_to,
        )

    def search_by(self, filter_value, **kwargs):
        limit = kwargs.pop("limit", None)
        if "paged_size" in kwargs:
            limit = kwargs.pop("paged_size")

        as_raw = kwargs.pop("as_raw", False)
        conn = kwargs.pop("conn", self.conn)
        conn.search(
            search_base=self.base_dn,
            search_filter=filter_value,
            search_scope=self.search_scope,
            attributes=self.retrive_attrs,
            paged_size=limit,
            **kwargs
        )
        results = []
        for entry in conn.response:
            if "attributes" in entry:
                if as_raw:
                    results.append(entry["attributes"])
                else:
                    results.append(self.parse_info(entry["attributes"]))

        return results

    def search_name(self, name, limit=1, **kwargs):
        return self.search_by(
            COMMON_FILTERS["name"].format(name), limit=limit, **kwargs
        )

    def search_email(self, email, limit=1, **kwargs):
        return self.search_by(
            COMMON_FILTERS["email"].format(email), limit=limit, **kwargs
        )

    def search_mail(self, email, limit=1, **kwargs):
        return self.search_email(email, limit, **kwargs)

    def search_phone(self, phone, limit=1, **kwargs):
        return self.search_by(
            COMMON_FILTERS["phone"].format(phone), limit=limit, **kwargs
        )

    def search_mobile(self, mobile, limit=1, **kwargs):
        return self.search_by(
            COMMON_FILTERS["mobile"].format(mobile), limit=limit, **kwargs
        )

    def search_number(self, number, limit=1, **kwargs):
        return self.search_by(
            COMMON_FILTERS["number"].format(number), limit=limit, **kwargs
        )

    def search_display(self, display_name, limit=1, **kwargs):
        return self.search_by(
            COMMON_FILTERS["display"].format(display_name),
            limit=limit,
            **kwargs
        )
