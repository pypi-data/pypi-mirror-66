'''Portlet management'''

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

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Portlet:
    '''The portlet, in the standard layout, is a zone from the UI shown as a
       column situated at the left of the screen for left-to-right languages,
       and at the right for right-to-left languages.'''

    @classmethod
    def show(class_, tool, px, ctx):
        '''When must the portlet be shown ?'''
        # Do not show the portlet on 'edit' pages, if we are in the popup or if
        # there is no root class.
        if ctx.popup or (ctx.layout == 'edit') or (px.name == 'home') or \
           (ctx.config.model.rootClasses is None):
            return
        # If we are here, portlet visibility depends on the app, via method
        # "tool::showPortletAt", when defined.
        return tool.showPortletAt(ctx.handler.path) \
               if hasattr(tool, 'showPortletAt') else True

    px = Px('''
     <x var="toolUrl=tool.url;
             queryUrl='%s/Search/results' % toolUrl;
             currentSearch=req.search;
             currentClass=req.className;
             currentPage=handler.parts[-1];
             rootClasses=handler.server.model.getRootClasses()">

      <!-- One section for every searchable root class -->
      <x for="class_ in rootClasses" if="class_.maySearch(tool, layout)"
         var2="className=class_.name">

       <!-- A separator if required -->
       <div class="portletSep" if="not loop.class_.first"></div>

       <!-- Section title (link triggers the default search) -->
       <div class="portletContent"
            var="searches=class_.getGroupedSearches(tool, _ctx_)">
        <div class="portletTitle">
         <a var="queryParam=searches.default.name if searches.default else ''"
            href=":'%s?className=%s&amp;search=%s' % \
                   (queryUrl, className, queryParam)"
            onclick="clickOn(this)"
            class=":(not currentSearch and (currentClass==className) and \
                    (currentPage == 'pxResults')) and \
                    'current' or ''">::_(className + '_plural')</a>

         <!-- Create instances of this class -->
         <x if="guard.mayInstantiate(class_)"
            var2="asButton=False; nav='no'">:class_.pxAdd</x>
        </div>

        <!-- Searches -->
        <x if="class_.maySearchAdvanced(tool)">

         <!-- Live search -->
         <x>:tool.Search.live</x>

         <!-- Advanced search -->
         <div var="highlighted=(currentClass == className) and \
                               (currentPage == 'search')"
              class=":highlighted and 'portletSearch current' or \
                     'portletSearch'"
              align=":dright" style="margin-bottom: 4px">
          <a var="text=_('search_title')" style="font-size: 88%"
             href=":'%s/Search/advanced?className=%s' % (toolUrl, className)"
             title=":text"><x>:text</x>...</a>
         </div>
        </x>

        <!-- Predefined searches -->
        <x for="search in searches.all" var2="field=search">
         <x>:search.px if search.type == 'group' else search.view</x>
        </x>

        <!-- Portlet bottom, potentially customized by the app -->
        <x var="pxBottom=class_.getPortletBottom(tool)"
           if="pxBottom">:pxBottom</x>
       </div>
      </x>
     </x>''',

     css='''
       .portlet { width: 170px; border: none; color: white;
                  background-color: #8399b7; padding-top: 30px;
                  vertical-align: top; margin-bottom: 30px; position: relative }
       .portlet a, .portlet a:visited { color: white; padding: 0px 5px 0 0 }
       .portlet a:hover { background-color: white; color: #305e9d }
       .portletContent { padding: 0 0 0 20px; background: none; width: 180px }
       .portletContent input[type=text] { background-color: white }
       .portletTitle { font-size: 110%; padding: 5px 0; margin: 0;
                       text-transform: uppercase }
       .portletSep { border-top: 10px solid transparent }
       .portletGroup { text-transform: uppercase; padding: 5px 0 0 0;
                       margin: 0.1em 0 0.3em }
       .portletSearch { font-size: 110%; text-align: left }
       .portletCurrent { font-weight: bold }
       .portlet form { margin-left: -3px }
     ''')
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
