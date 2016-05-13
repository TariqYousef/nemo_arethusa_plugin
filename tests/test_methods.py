from nemo_arethusa_plugin import Arethusa, ArethusaSimpleQuery
from flask_nemo.query.resolve import Resolver, LocalRetriever
from .resources import NautilusDummy, make_client
from unittest import TestCase


class TestQueryInterface(TestCase):
    """ Ensure that inner methods work as expected
    """

    def test_get_innerreffs(self):
        query = ArethusaSimpleQuery({
            "urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.pr.1-1.pr.5": "treebanks/treebank2.xml",
            "urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.5": "treebanks/treebank1.xml"
        }, resolver=Resolver(LocalRetriever(path="./tests/test_data/")))
        nemo = make_client(output_nemo=True)[0]
        query.process(nemo)

        self.assertEqual(
            query.annotations["urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.pr.2"], "treebanks/treebank2.xml",
            "URNs should have been expanded"
        )
