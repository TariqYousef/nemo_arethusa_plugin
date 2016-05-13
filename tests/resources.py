from flask import Flask
from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from capitains_nautilus.mycapytain import NautilusRetriever


NautilusDummy = NautilusRetriever(
    folders=[
        "./tests/test_data/latinLit"
    ]
)


def make_client(*plugins, output_nemo=False):
    """ Create a test client with *plugins inserted

    :param plugins: plugins instances
    :return:
    """
    app = Flask("Nemo")
    app.debug = True
    nemo = Nemo(
        app=app,
        base_url="",
        retriever=NautilusDummy,
        chunker={"default": lambda x, y: level_grouper(x, y, groupby=30)},
        plugins=plugins
    )
    if output_nemo:
        return nemo, app.test_client()
    return app.test_client()
