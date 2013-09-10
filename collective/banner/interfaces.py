from zope.interface import Interface


class IThemeLayer(Interface):
    """Theme specific layer
    """


class IBannerProvider(Interface):
    """Marker interface for objects that can be used as banner providers.
    """
