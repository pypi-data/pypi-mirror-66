from contextlib import contextmanager
import ipywidgets.widgets as w
from .output import Output


class _CollectionMixin:
    output_layout = None
    @contextmanager
    def capture(self, err_stop=True, layout=None, **kw):
        with Output(err_stop=err_stop, layout=layout or self.output_layout, **kw) as out:
            self.append(out)
            yield out

    def append(self, child):
        self.children += (child,)

    def __len__(self):
        return len(self.children)

class _SelectableCollectionMixin(_CollectionMixin):
    @contextmanager
    def capture(self, title=None, selected=None, err_stop=True, **kw):
        with Output(err_stop=err_stop, **kw) as out:
            self.append(out, title, selected=selected)
            yield out

    def select(self, i):
        self.selected_index = i

    def append(self, child, title=None, selected=None):
        self.children += (child,)
        title and self.set_title(len(self) - 1, title)
        self.select(selected and len(self) - 1)


class Accordion(w.Accordion, _SelectableCollectionMixin):
    pass

class Carousel(w.Box, _CollectionMixin):
    layout = w.Layout(
        flex_flow='row nowrap',
        overflow_x='auto',
        max_width='100%',
    )
    output_layout = w.Layout()

class Tab(w.Tab, _SelectableCollectionMixin):
    pass
