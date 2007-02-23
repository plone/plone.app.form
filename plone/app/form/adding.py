from Products.Five.browser.adding import ContentAdding

class CMFAdding(ContentAdding):
    """An adding view with a less silly next-url
    """
    
    def nextURL(self):
        return "%s/%s/view" % (self.context.absolute_url(), self.contentName)

# class TitleBasedNameChooser(object):
#     """A name chooser for a Zope object manager.
#     """
#     
#     implements(INameChooser)
#     
#     def __init__(self, context):
#         self.context = context
# 
#     def checkName(self, name, object):
#         try:
#             name = name.encode('ascii')
#         except UnicodeDecodeError:
#             raise UserError, "Id must contain only ASCII characters."
# 
#         context = aq_inner(self.context)
#         try:
#             check_id = getattr(object.__of__(context), 'check_id', None)
#         except AttributeError:
#             check_id = None
#         if check_id is not None:
#             invalid = check_id(name, required=1)
#             if invalid:
#                 raise UserError, invalid
#         else:
#             try:
#                 self.context._checkId(name, allow_dup=False)
#             except BadRequest, e:
#                 msg = ' '.join(e.args) or "Id is in use or invalid"
#                 raise UserError, msg
# 
#     def chooseName(self, name, object):
#         if not name:
#             title = getattr(object, 'title', '')
#             name = self.getIdFromTitle(title)
#             if not name:
#                 name = object.__class__.__name__
#         try:
#             name = name.encode('ascii')
#         except UnicodeDecodeError:
#             raise UserError, "Id must contain only ASCII characters."
# 
#         dot = name.rfind('.')
#         if dot >= 0:
#             suffix = name[dot:]
#             name = name[:dot]
#         else:
#             suffix = ''
# 
#         n = name + suffix
#         i = 0
#         while True:
#             i += 1
#             try:
#                 self.context._getOb(n)
#             except AttributeError:
#                 break
#             n = name + '-' + str(i) + suffix
# 
#         # Make sure the name is valid.  We may have started with
#         # something bad.
#         self.checkName(n, object)
# 
#         return n
# 
#     def getIdFromTitle(self, title):
#         context = self.context
#         plone_tool = getToolByName(context, 'plone_utils', None)
#         if plone_tool is not None:
#             return plone_tool.normalizeString(title)
#         return None