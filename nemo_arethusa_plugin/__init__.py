from flask_nemo.plugin import PluginPrototype
from MyCapytain.resources.texts.api import Text
from MyCapytain.common.reference import URN
from flask_nemo.query.proto import QueryPrototype
from pkg_resources import resource_filename


class ArethusaSimpleQuery(QueryPrototype):
    """ Query Interface for hardcoded annotations.

    :param annotations: Dictionary of {CTS URN : annotations with URIs to resolve as resource to get}
    :type annotations:{str : str}
    """
    
    def __init__(self, annotations, resolver=None):
        super(ArethusaSimpleQuery, self).__init__(None)
        self.__annotations__ = annotations
        self.__nemo__ = None
        self.__resolver__ = resolver

    def process(self, nemo):
        """ Register nemo and parses annotations

        :param nemo: Nemo
        """
        self.__nemo__ = nemo
        annotations = dict()
        for urn_str, annotation in self.__annotations__.items():
            urn = URN(urn_str)

            for suburn in self.__getinnerreffs__(
                text=self.__nemo__.get_text(
                    urn.namespace,
                    urn.textgroup,
                    urn.work,
                    urn.version
                ),
                urn=urn
            ):
                annotations[suburn] = annotation
        self.__annotations__ = annotations

    @property
    def annotations(self):
        return self.__annotations__

    def getAnnotations(self,
            *urns,
            wildcard=".", include=None, exclude=None,
            limit=None, start=1,
            expand=False, **kwargs
        ):
        pass

    def __partOf__(self, source, annotations):
        """ See if some annotations are part of the list found

        :return:
        """
        pass

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
