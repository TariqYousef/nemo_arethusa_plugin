from nemo_arethusa_plugin import Arethusa, ArethusaSimpleQuery
from flask_nemo.query.resolve import Resolver, LocalRetriever
from .resources import NautilusDummy, make_client
from unittest import TestCase


TB_URI = "http://data.perseus.org/rdfvocab/treebank"


class TestQueryInterface(TestCase):
    """ Ensure that inner methods work as expected
    """

    def test_get_innerreffs(self):
        query = ArethusaSimpleQuery([
            ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.pr.1-1.pr.5", "treebanks/treebank2.xml", TB_URI),
            ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.5", "treebanks/treebank1.xml", TB_URI)
        ], resolver=Resolver(LocalRetriever(path="./tests/test_data/")))
        arethusa = Arethusa(query)
        nemo = make_client(arethusa, output_nemo=True)[0]
        query.process(nemo)

        self.assertEqual(
            str(query.getResource("treebanks/treebank2.xml").target.urn),
            "urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.pr.1-1.pr.5",
            "URNs should have been expanded"
        )

        self.assertEqual(
            str(query.getResource("treebanks/treebank1.xml").target.urn),
            "urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.5",
            "URNs should have been expanded"
        )

    def test_query(self):
        query = ArethusaSimpleQuery([
            ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.pr.1-1.pr.5", "treebanks/treebank2.xml", TB_URI),
            ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.5", "treebanks/treebank1.xml", TB_URI)
        ], resolver=Resolver(LocalRetriever(path="./tests/test_data/")))
        arethusa = Arethusa(query)
        nemo = make_client(arethusa, output_nemo=True)[0]
        query.process(nemo)

        self.assertEqual(
            query.getAnnotations("urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.pr.2"),  # Query
            (1, [query.getResource("treebanks/treebank2.xml")]),  # Result
            "Resource should be found"
        )
        self.assertEqual(
            query.getAnnotations("urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.pr.1-1.5.1"),  # Query
            (2, [
                query.getResource("treebanks/treebank1.xml"),
                # Annotations are registered by their lower level
                query.getResource("treebanks/treebank2.xml")
                # 1.pr.1 to 1.pr.2 share the same object, so we can check on equality like this
            ]),  # Result
            "Resource should be found"
        )
