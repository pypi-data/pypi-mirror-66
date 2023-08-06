# ipyumbrella
Improved ipywidgets using contextmanager.

## Install

```bash
pip install ipyumbrella
```

## Usage

```python
import ipyumbrella as uw
import matplotlib.pyplot as plt
```

```python
carousel = uw.Carousel()
for i in range(5):
    with carousel.item():
        plt.plot(range(10 + i))
carousel
```

```python
acc = uw.Accordion()
for i in range(5):
    with acc.item('Item {}'.format(i)):
        plt.plot(range(10 + i))
acc
```

```python
tabs = uw.Tabs()
for i in range(5):
    with tabs.item('Item {}'.format(i)):
        plt.plot(range(10 + i))
tabs
```

```python
# manually add an output as a tab above
with uw.Output() as out:
    tabs.append(out)
    plt.plot(range(10 + i))
```
