from flask_nemo.plugins.annotations_api import AnnotationsApiPlugin
from flask import url_for, jsonify, send_from_directory
from pkg_resources import resource_filename


class Arethusa(AnnotationsApiPlugin):
    """ Arethusa plugin for Nemo

    .. note:: This class inherits some routes from the base `AnnotationsApiPluigin <http://flask-capitains-nemo.readthedocs.io/en/1.0.0b-dev/Nemo.api.html#flask.ext.nemo.plugins.annotations_api.AnnotationsApiPlugin>`_

    :param queryinterface: QueryInterface to use to retrieve annotations
    :type queryinterface: flask_nemo.query.proto.
    """
    HAS_AUGMENT_RENDER = True
    CSS_FILENAMES = ["arethusa.min.css", "foundation-icon.css", "font-awesome.min.css", "colorpicker.css"]
    JS_FILENAMES = ["arethusa.widget.loader.js", "arethusa.min.js", "arethusa.packages.min.js"]
    CSS = ["http://127.0.0.1:5000/arethusa-assets/css/arethusa.min.css"]
    REQUIRED_ASSETS = ["arethusa.widget.loader.js"]
    TEMPLATES = {
        "arethusa": resource_filename("nemo_arethusa_plugin", "data/templates")
    }
    FILTERS = [
        "f_annotation_filter"
    ]

    ROUTES = AnnotationsApiPlugin.ROUTES + [
        ("/arethusa.deps.json", "r_arethusa_dependencies", ["GET"]),
        ("/arethusa-assets/<path:filename>", "r_arethusa_assets", ["GET"]),
        ("/arethusa.config.json", "r_arethusa_config", ["GET"])
    ]
    
    def __init__(self, queryinterface, *args, **kwargs):
        super(Arethusa, self).__init__(queryinterface=queryinterface, *args, **kwargs)
        self.__interface__ = queryinterface

    @property
    def interface(self):
        return self.__interface__

    def render(self, **kwargs):
        update = kwargs
        if "template" in kwargs and kwargs["template"] == "main::text.html":
            total, update["annotations"] = self.interface.getAnnotations(kwargs["urn"])

            if total > 0:
                update["template"] = "arethusa::text.html"
            else:
                del update["annotations"]

        return update

    def r_arethusa_assets(self, filename):
        """

        :param filename:
        :return:
        """
        return send_from_directory(resource_filename("nemo_arethusa_plugin", "data/assets"), filename)

    def r_arethusa_dependencies(self):
        """ Return the json config of dependencies

        :return:
        """
        return jsonify({
            "css": {
                "arethusa": url_for(".r_arethusa_assets", filename="css/arethusa.min.css"),
                "foundation": url_for(".r_arethusa_assets", filename="css/foundation-icons.css"),
                "font_awesome": url_for(".r_arethusa_assets", filename="css/font-awesome.min.css"),
                "colorpicker": url_for(".r_arethusa_assets", filename="css/colorpicker.css",)
            },
            "js": {
                "arethusa": url_for(".r_arethusa_assets", filename="js/arethusa.min.js"),
                "packages": url_for(".r_arethusa_assets", filename="js/arethusa.packages.min.js")
            }
        })

    def r_arethusa_config(self):
        return {
            "template": "arethusa::widget.tree.json"
        }

    @staticmethod
    def f_annotation_filter(annotations, type_uri, number):
        """ Annotation filtering filter

        :param annotations: List of annotations
        :type annotations: [AnnotationResource]
        :param type_uri: URI Type on which to filter
        :type type_uri: str
        :param number: Number of the annotation to return
        :type number: int
        :return: Annotation(s) matching the request
        :rtype: [AnnotationResourcee] or AnnotationResource
        """
        filtered = [
            annotation
            for annotation in annotations
            if annotation.type_uri == type_uri
        ]
        number = min([len(filtered), number])
        if number == 0:
            return None
        else:
            return filtered[number-1]
