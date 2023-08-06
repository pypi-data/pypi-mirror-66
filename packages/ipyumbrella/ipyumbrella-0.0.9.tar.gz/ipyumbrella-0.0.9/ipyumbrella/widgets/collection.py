from contextlib import contextmanager
from IPython.display import display
import ipywidgets.widgets as w
from .output import Output


class _CollectionMixin:
    output_layout = w.Layout()
    title_layout = w.Layout(font_size='1.2em')
    def item(self, title=None, layout=None, err_stop=True, **kw):
        return self.append(Output(
            err_stop=err_stop, layout=layout or self.output_layout, **kw), title=title)

    def append(self, child, title=None):
        if title:
            wrap = w.HBox([w.Label(value=title, layout=self.title_layout), child])
            self.children += (wrap,)
        else:
            self.children += (child,)
        return child

    def __len__(self):
        return len(self.children)

class _SelectableCollectionMixin(_CollectionMixin):
    def item(self, title=None, selected=True, err_stop=True, **kw):
        return self.append(Output(err_stop=err_stop, **kw), title, selected=selected)

    def select(self, i):
        self.selected_index = i

    def append(self, child, title=None, selected=True):
        self.children += (child,)
        title and self.set_title(len(self) - 1, title)
        self.select(selected and len(self) - 1)
        return child


class Carousel(w.Box, _CollectionMixin):
    layout = w.Layout(
        flex_flow='row nowrap',
        overflow_x='auto',
        max_width='100%',
    )

class Accordion(w.Accordion, _SelectableCollectionMixin):
    pass

class Tab(w.Tab, _SelectableCollectionMixin):
    pass
