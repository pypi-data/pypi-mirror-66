# ------------------------------------------------------------------------------
from appy.gen import Show, Pod, Table
from appy.shared.xml_parser import Escape
from appy.gen.wrappers import AbstractWrapper

# ------------------------------------------------------------------------------
EXPRESSION_ERROR = 'error while evaluating page expression: %s'

# ------------------------------------------------------------------------------
class PageWrapper(AbstractWrapper):

    def getSubBreadCrumb(self):
        '''Display an icon for downloading this page (and sub-pages if any) as a
           POD.'''
        if not self.isEmpty('parent'): return
        return self.getField('doc').doRender('view', self)

    def validate(self, new, errors):
        '''Inter-field validation.'''
        return self._callCustom('validate', new, errors)

    def showSubPages(self):
        '''Show the sub-pages.'''
        if self.user.hasRole('Manager'): return 'view'

    def showPortlet(self):
        '''Do not show the portlet for a page'''
        return

    def showExpression(self):
        '''Show the expression to managers only'''
        # Do not show it on "view" if empty
        if self.isEmpty('expression'): return Show.V_
        return self.user.hasRole('Manager')

    def mayView(self):
        '''In addition to the workflow, evaluating p_self.expression, if
           defined, determines p_self's visibility.'''
        expression = self.expression
        if not expression: return True
        user = self.user
        try:
            return eval(expression)
        except Exception, err:
            self.log(EXPRESSION_ERROR % str(err), type='error')
            return

    def onEdit(self, created):
        return self._callCustom('onEdit', created)

    def getMergedContent(self, level=1):
        '''Returns a chunk of XHTML code containing p_self's info (title and
           content) and, recursively, info about all its sub-pages.'''
        # Add p_self's title
        title = self.getValue('title', formatted='shown')
        r = ['<h%d>%s</h%d>' % (level, Escape.xhtml(title), level)]
        # Add p_self's content
        if not self.isEmpty('content'):
            r.append(self.getValue('content', formatted='shown'))
        # Add sub-pages
        if not self.isEmpty('pages'):
            for page in self.pages:
                r.append(page.getMergedContent(level=level+1))
        return ''.join(r)
# ------------------------------------------------------------------------------
