__version__ = '0.1.0'

import fire

def hello(name="World"):
    return "Hello %s!" % name

def run():
    fire.Fire(hello)