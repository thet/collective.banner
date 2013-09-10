from AccessControl import SecurityManagement
from Products.ATContentTypes.permission import ChangeTopics
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
try:
    from plone.app.collection.interfaces import ICollection
except ImportError:
    from zope.interface import Interface
    class ICollection(Interface):
        pass

_ = MessageFactory('collective.banner')


class IBannerPortlet(IPortletDataProvider):
    """A portlet displaying a banners from a Collection's results
    """

    target_collection = schema.Choice(
        title=_(u"Target collection"),
        description=_(u"Find the collection which provides the items to list"),
        required=True,
        source=SearchableTextSourceBinder(
            {'portal_type': ('Topic', 'Collection')},
            default_query='path:'))

    timer = schema.Int(
        title=_(u"Timer"),
        description=_(u"Carousel rotated time (milliseconds)"),
        required=False,
        default=10000)

    image_scale = schema.Choice(
        title=_(u'portlet_image_scale', default=u'Image Scale'),
        description=_(u'portlet_help_image_scale',
                      default=u'Select, which image scale should be used '
                              u'for the portlet, if there is any image.'),
        required=True,
        default=None,
        vocabulary="collective.banner.ImageScaleVocabulary",
        )


class Assignment(base.Assignment):
    implements(IBannerPortlet)

    target_collection = None
    timer = 10000
    image_scale = None

    def __init__(self, target_collection=None, timer=10000, image_scale=None):
        self.target_collection = target_collection
        self.timer = timer
        self.image_scale = image_scale

    @property
    def title(self):
        return u"Banner portlet"


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('portlet.pt')

    def __init__(self, *args, **kwargs):
        super(Renderer, self).__init__(*args, **kwargs)
        self.request.set('banner_image_scale', self.data.image_scale)

    @property
    def available(self):
        return len(self.results())

    @memoize
    def collection(self):
        cpath = self.data.target_collection

        if isinstance(cpath, basestring) and cpath.startswith('/'):
            cpath = cpath[1:]

        if not cpath:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                                       name=u'plone_portal_state')
        portal = portal_state.portal()
        if isinstance(cpath, unicode):
            # restrictedTraverse accepts only strings
            cpath = str(cpath)
        return portal.restrictedTraverse(cpath, default=None)

    def collection_url(self):
        collection = self.collection()
        if collection is None:
            return None
        else:
            return collection.absolute_url()

    @memoize
    def results(self):
        results = []
        collection = self.collection()
        if collection is not None:
            results = collection.queryCatalog()
        return results

    def get_tile(self, obj):
        # When adapter is uesd this means we check whether obj has any special
        # instructions about how to be handled in defined view or interface
        # for multi adapter the same is true except more object than just the
        # obj are check for instructions

        #have to use traverse to make zpt security work
        tile = obj.unrestrictedTraverse("banner-tile")
        if tile is None:
            return None
        return tile()

    def edit_collection(self):
        provider = self.collection()
        smanager = SecurityManagement.getSecurityManager()
        allowed = smanager.checkPermission(ChangeTopics, provider)
        if allowed:
            provider = self.collection()
            if provider is not None:
                if ICollection.providedBy(provider):
                    return provider.absolute_url() + '/edit'
                return provider.absolute_url() + '/criterion_edit_form'
        return None


class AddForm(base.AddForm):
    form_fields = form.Fields(IBannerPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    label = _(u"Add Banner Portlet")
    description = _(u"This portlet display a listing of items from a \
                      Collection as a banner carousel.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IBannerPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    label = _(u"Edit Banner Portlet")
    description = _(u"This portlet display a listing of items from a \
                      Collection as a banner carousel.")
