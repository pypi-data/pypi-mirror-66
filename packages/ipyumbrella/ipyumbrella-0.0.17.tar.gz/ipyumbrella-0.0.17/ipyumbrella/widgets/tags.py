from IPython.display import display, HTML


def h1(content):
    return header(content, 1)

def h2(content):
    return header(content, 1)

def h3(content):
    return header(content, 1)

def h4(content):
    return header(content, 1)

def h5(content):
    return header(content, 1)

def h6(content):
    return header(content, 1)

def header(content, level=1):
    return tag(content, 'h{}'.format(level))

def div(content):
    return HTML(content)

def tag(content, elem='div'):
    return HTML('<{elem}>{content}</{elem}>'.format(content=content, elem=elem))
