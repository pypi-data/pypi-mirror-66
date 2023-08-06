from contextlib import contextmanager
import ipywidgets.widgets as w
from .output import Output


class CollectionMixin:
    @contextmanager
    def _capture(self, title=None, selected=None, err_stop=True, **kw):
        out = Output(err_stop=err_stop, **kw)
        self.append(out, title, selected=selected)
        with out:
            yield out

    def select(self, i):
        self.selected_index = i

    def append(self, child, title=None, selected=None):
        self.children += (child,)
        if title:
            self.set_title(len(self.children) - 1, title)
        self.select(selected and len(self.children) - 1)


class Accordion(w.Accordion, CollectionMixin):
    pass

class Carousel(w.Box, CollectionMixin):
    layout = w.Layout(
        flex_flow='row nowrap',
        overflow_x='auto',
        max_width='100%',
    )
    output_layout = w.Layout()

    def capture(self, layout=None, **kw):
        return super().capture(
            layout=layout or self.output_layout, title=None, selected=None, **kw)

    def append(self, child, **kw):
        return super().append(child, title=None, selected=None, **kw)


class Tab(w.Tab, CollectionMixin):
    pass
