from flask_nemo.plugin import PluginPrototype
from MyCapytain.resources.texts.api import Text
from MyCapytain.common.reference import URN
from flask_nemo.query.proto import QueryPrototype
from flask_nemo.query.annotation import AnnotationResource

from pkg_resources import resource_filename


class ArethusaSimpleQuery(QueryPrototype):
    """ Query Interface for hardcoded annotations.

    :param annotations: List of tuple of (CTS URN Targeted, URI of the Annotation, Type of the annotation
    :type annotations: [(str, str, str)]
    :param resolver: Resolver
    :type resolver: Resolver
    """
    
    def __init__(self, annotations, resolver=None):
        super(ArethusaSimpleQuery, self).__init__(None)
        self.__annotations__ = []
        self.__nemo__ = None
        self.__resolver__ = resolver

        for target, body, type_uri in annotations:
            self.__annotations__.append(AnnotationResource(
                body, target, type_uri, self.__resolver__
            ))

    def process(self, nemo):
        """ Register nemo and parses annotations

        :param nemo: Nemo
        """
        self.__nemo__ = nemo
        for annotation in self.__annotations__:
            annotation.target.expanded = frozenset(self.__getinnerreffs__(
                text=self.__getText__(annotation.target.urn),
                urn=annotation.target.urn
            ))

    def __getText__(self, urn):
        """ Return a metadata text object

        :param urn: URN object of the passage
        :return: Text
        """
        return self.__nemo__.get_text(
            urn.namespace,
            urn.textgroup,
            urn.work,
            urn.version
        )

    @property
    def annotations(self):
        return self.__annotations__

    def getAnnotation(self, uri):
        return [annotation for annotation in self.annotations if annotation.uri == uri][0]

    def getAnnotations(self,
            *urns,
            wildcard=".", include=None, exclude=None,
            limit=None, start=1,
            expand=False, **kwargs
        ):
        annotations = []
        for urn in urns:
            _urn = URN(urn)
            if _urn.reference.end:
                urns_in_range = self.__getinnerreffs__(
                    text=self.__getText__(_urn),
                    urn=_urn
                )
            else:
                urns_in_range = [urn]

            urns_in_range = frozenset(urns_in_range)
            annotations.extend([
                annotation
                for annotation in self.annotations
                if bool(urns_in_range.intersection(annotation.target.expanded))
            ])

        annotations = list(set(annotations))

        return len(annotations), sorted(annotations, key=lambda x: x.uri)

    def __getinnerreffs__(self, text, urn):
        """ Resolve the list of urns between in a range

        :param urn: Urn of the passage
        :type urn: URN
        :return:
        """
        text = Text(
            str(text.urn),
            self.__nemo__.retriever,
            citation=text.citation
        )
        return text.getValidReff(reference=urn.reference, level=len(text.citation))


class Arethusa(PluginPrototype):
    """ Arethusa plugin for Nemo

    """
    HAS_AUGMENT_RENDER = True
    
    def __init__(self, interface, *args, **kwargs):
        super(Arethusa, self).__init__(*args, **kwargs)
        self.__interface__ = interface

    @property
    def interface(self):
        return self.__interface__