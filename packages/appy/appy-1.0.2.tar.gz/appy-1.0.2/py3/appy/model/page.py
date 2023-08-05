#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Copyright (C) 2007-2020 Gaetan Delannay

# This file is part of Appy.

# Appy is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# Appy is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# Appy. If not, see <http://www.gnu.org/licenses/>.

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from appy.px import Px
from appy.model.base import Base
from appy.xml.escape import Escape
from appy.all import String, Rich, Pod, Ref, autoref, Layouts, Show

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
EXPRESSION_ERROR = 'error while evaluating page expression: %s'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Page(Base):
    '''Base class representing a web page'''
    pa = {'label': 'Page'}
    # Pages are not indexed by default
    indexable = False

    # The POD ouput
    doc = Pod(template='/model/pod/Page.odt', formats=('pdf',),
              show=False, layouts=Pod.Layouts.inline)

    # The page title
    title = String(show='edit', multiplicity=(1,1), indexed=True, **pa)

    # The POD output appears inline in the sub-breadcrumb
    def getSubBreadCrumb(self):
        '''Display an icon for downloading this page (and sub-pages if any) as a
           POD.'''
        if not self.isEmpty('parent'): return
        return self.getField('doc').doRender('view', self)

    # The page content
    content = Rich(layouts=Layouts.b)

    # A page can contain sub-pages
    def showSubPages(self):
        '''Show the field allowing to edit sub-pages'''
        if self.user.hasRole('Manager'): return 'view'

    pages = Ref(None, multiplicity=(0,None), add=True, link=False,
      composite=True, back=Ref(attribute='parent', show=False, **pa),
      show=showSubPages, navigable=True, numbered=True, **pa)

    # If this Python expression returns False, the page can't be viewed
    def showExpression(self):
        '''Show the expression to managers only'''
        # Do not show it on "view" if empty
        if self.isEmpty('expression'): return Show.V_
        return self.user.hasRole('Manager')

    expression = String(layouts=Layouts.d, show=showExpression, **pa)

    def showPortlet(self):
        '''Never show the portlet for a page'''
        return

    def mayView(self):
        '''In addition to the workflow, evaluating p_self.expression, if
           defined, determines p_self's visibility.'''
        expression = self.expression
        if not expression: return True
        user = self.user
        try:
            return eval(expression)
        except Exception as err:
            self.log(EXPRESSION_ERROR % str(err), type='error')
            return

    def getMergedContent(self, level=1):
        '''Returns a chunk of XHTML code containing p_self's info (title and
           content) and, recursively, info about all its sub-pages.'''
        # Add p_self's title
        title = self.getValue('title', type='formatted')
        r = ['<h%d>%s</h%d>' % (level, Escape.xhtml(title), level)]
        # Add p_self's content
        if not self.isEmpty('content'):
            r.append(self.getValue('content', type='formatted'))
        # Add sub-pages
        if not self.isEmpty('pages'):
            for page in self.pages:
                r.append(page.getMergedContent(level=level+1))
        return ''.join(r)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  PXs
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # This selector allows to choose one root page among tool.pages
    pxSelector = Px('''
      <select onchange="gotoURL(this)">
       <option value="">:_('goto_link')</option>
       <option for="page in tool.pages" if="guard.mayView(page)"
               value=":page.url">:page.title</option>
      </select>''',

     js='''
       function gotoURL(select) {
         var url = select.value;
         if (url) goto(url);
       }''')

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
autoref(Page, Page.pages)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
