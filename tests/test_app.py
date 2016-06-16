from unittest import TestCase
from .resources import NautilusDummy
from flask import Flask
from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from flask_nemo.query.interface import SimpleQuery
from flask_nemo.query.resolve import LocalRetriever, Resolver
from nemo_arethusa_plugin import Arethusa
import json


class TestPlugin(TestCase):
    def setUp(self):
        TB_URI = "http://data.perseus.org/rdfvocab/treebank"

        app = Flask("Nemo")
        app.debug = True
        self.interface = SimpleQuery(
            [
                ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:6.1", "treebanks/treebank1.xml", TB_URI),
                ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:1.5", "treebanks/treebank2.xml", TB_URI),
                ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:6.1", "images/N0060308_TIFF_145_145.tif", "dc:image"),
                ("urn:cts:latinLit:phi1294.phi002.perseus-lat2:6.2", "images/N0060308_TIFF_145_145.tif", "dc:image")
            ],
            resolver=Resolver(LocalRetriever(path="./tests/test_data/"))
        )
        self.arethusa = Arethusa(queryinterface=self.interface)
        app.debug = True
        nemo = Nemo(
            app=app,
            base_url="",
            retriever=NautilusDummy,
            chunker={"default": lambda x, y: level_grouper(x, y, groupby=30)},
            plugins=[self.arethusa]
        )
        self.interface.process(nemo)
        self.client = app.test_client()

    def test_text_with_treebank(self):
        """Ensure treebank are visible"""
        data = self.client.get("/read/latinLit/phi1294/phi002/perseus-lat2/6.1").data.decode("utf-8")
        self.assertIn(
            ">Treebank</a>", data,
            "Treebank tab should be visible when there is a treebank"
        )
        self.assertIn(
            self.interface.annotations[0].sha, data,
            "Treebank sha should be visible in scripts"
        )

    def test_text_without_treebank(self):
        """Ensure treebank are not loaded"""
        data = self.client.get("/read/latinLit/phi1294/phi002/perseus-lat2/6.2").data.decode("utf-8")
        self.assertNotIn(
            ">Treebank</a>", data,
            "Treebank tab should not be visible when there is no treebank"
        )
        data = self.client.get("/read/latinLit/phi1294/phi002/perseus-lat2/6.3").data.decode("utf-8")
        self.assertNotIn(
            ">Treebank</a>", data,
            "Treebank tab should not be visible when there is no treebank"
        )

    def test_asset_route(self):
        """ Ensure assets are accessible """
        response = self.client.get("/arethusa-assets/js/arethusa.min.js")
        self.assertEqual(response.status_code, 200, "Assets should be accessible")

    def test_dependencies_config(self):
        """ Ensure dependencies json are working """
        data = json.loads(self.client.get("/arethusa.deps.json").data.decode("utf-8"))
        self.assertCountEqual(list(data.keys()), ["js", "css"], "Dict should have two dict : js and css")
        self.assertCountEqual(list(data["js"].keys()), ["arethusa", "packages"], "Js should have required pkgs")
        self.assertCountEqual(list(data["css"].keys()), ["arethusa", "colorpicker", "foundation", "font_awesome"],
                              "Js should have required pkgs")
        counter = 6

        for url in list(data["js"].values()) + list(data["css"].values()):
            self.assertEqual(self.client.get(url).status_code, 200, "Assets should be accessible")
            counter -= 1
        self.assertEqual(counter, 0)

    def test_arethusa_config(self):
        """ Ensure the config for Arethusa contains the right URI """
        data = json.loads(self.client.get("/arethusa.config.json").data.decode("utf-8"))
        self.assertEqual(
            data["resources"]["arethusaServerTreebank"]["route"], "/api/annotations/:doc/body",
            "Route to annotation API body should be available"
        )