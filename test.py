from flask import Flask
from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from flask_nemo.query.resolve import Resolver, LocalRetriever
from nemo_arethusa_plugin import Arethusa
from flask_nemo.query.interface import SimpleQuery
from capitains_nautilus.mycapytain import NautilusRetriever

TB_URI = "http://data.perseus.org/rdfvocab/treebank"
NautilusDummy = NautilusRetriever(
    folders=[
        "./tests/test_data/latinLit"
    ]
)

app = Flask("Nemo")
app.debug = True
query = SimpleQuery(
    [
        ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:6.1", "treebanks/treebank1.xml", TB_URI),
        ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.5", "treebanks/treebank2.xml", TB_URI),
        ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:6.52", "images/N0060308_TIFF_145_145.tif", "dc:image")
    ],
    resolver=Resolver(LocalRetriever(path="./tests/test_data/"))
)
nemo = Nemo(
    app=app,
    base_url="",
    retriever=NautilusDummy,
    chunker={"default": lambda x, y: level_grouper(x, y, groupby=30)},
    plugins=[Arethusa(queryinterface=query)]
)
query.process(nemo)
app.run()
