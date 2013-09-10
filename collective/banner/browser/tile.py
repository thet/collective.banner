from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DefaultTile(BrowserView):
    template = ViewPageTemplateFile('templates/default_tile.pt')

    def tag(self, scale='mini', css_class='tileImage'):
        """Return a tag for the leadimage"""
        context = aq_inner(self.context)

        field = context.getField(IMAGE_FIELD_NAME)
        if field is not None:
            if field.get_size(context) != 0:
                return field.tag(context, scale=scale, css_class=css_class)

        if getattr(context, 'tag', None) is not None:
            return context.tag(scale=scale, css_class=css_class)

        return ''

    def caption(self):
        context = aq_inner(self.context)
        field = context.getField(IMAGE_CAPTION_FIELD_NAME)
        if field is None:
            return ''
        return context.widget(IMAGE_CAPTION_FIELD_NAME, mode='view')
