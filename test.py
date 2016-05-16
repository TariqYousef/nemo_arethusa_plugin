from flask import Flask
from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from flask_nemo.query.resolve import Resolver, LocalRetriever
from nemo_arethusa_plugin import ArethusaSimpleQuery, Arethusa
from capitains_nautilus.mycapytain import NautilusRetriever

TB_URI = "http://data.perseus.org/rdfvocab/treebank"
NautilusDummy = NautilusRetriever(
    folders=[
        "./tests/test_data/latinLit"
    ]
)

app = Flask("Nemo")
app.debug = True
query = ArethusaSimpleQuery([
    ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.pr.1-1.pr.5", "treebanks/treebank2.xml", TB_URI),
    ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.5", "treebanks/treebank1.xml", TB_URI)
], resolver=Resolver(LocalRetriever(path="./tests/test_data/")))
nemo = Nemo(
    app=app,
    base_url="",
    retriever=NautilusDummy,
    chunker={"default": lambda x, y: level_grouper(x, y, groupby=30)},
    plugins=[Arethusa(queryinterface=query)]
)
query.process(nemo)
app.run()
