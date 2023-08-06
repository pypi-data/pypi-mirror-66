#!/usr/bin/env python3
from orger import StaticView
from orger.inorganic import node, link
from orger.common import dt_heading

from my.instapaper import get_pages


class IpView(StaticView):
    def get_items(self):
        for page in get_pages():
            yield node(
                heading=dt_heading(
                    page.dt,
                    f'{link(title="ip", url=page.bookmark.instapaper_link)}   {link(title=page.title, url=page.url)}',
                ),
                children=[node(
                    heading=dt_heading(hl.dt, link(title="ip", url=page.bookmark.instapaper_link)),
                    body=hl.text,
                    children=[] if hl.note is None else [
                        node(heading=hl.note),
                    ],
                ) for hl in page.highlights]
            )
        # TODO autostrip could be an option for formatter
        # TODO reverse order? not sure...
        # TODO spacing top level items could be option of dumper as well?
        # TODO better error handling, cooperate with org_tools

# TODO move tests to separate files, otherwise they would annoy other people
test = IpView.make_test(
    heading='Life Extension Methods',
    contains='sleep a lot',
)


if __name__ == '__main__':
    IpView.main()
