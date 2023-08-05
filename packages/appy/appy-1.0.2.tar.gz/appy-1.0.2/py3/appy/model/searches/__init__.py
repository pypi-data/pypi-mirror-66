'''Searches represent predefined sets of critera allowing to perform database
   searches. A searched is always attached to a given class from the model.'''

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
from DateTime import DateTime

from appy.px import Px
from appy.model.batch import Batch
from appy.ui.criteria import Criteria
from appy.ui.template import Template
from appy.utils import string as sutils
from appy.model.fields.group import Group
from appy.model.searches.modes import Mode
from appy.model.searches import initiators

# Error messages - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
WRONG_FIELD = 'Field "%s" does not exist on %s.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class UiSearch:
    '''Instances of this class are generated on-the-fly for manipulating a
       Search instance from the User Interface.'''
    Mode = Mode

    # Rendering a search
    view = Px('''
     <div class="portletSearch">
      <a href=":'%s?className=%s&amp;search=%s' % \
                 (queryUrl, className, search.name)"
         class=":'current' if search.name == currentSearch else ''"
         onclick="clickOn(this)"
         title=":search.translatedDescr">:search.translated</a>
     </div>''')

    # Render search results
    pxResult = Px('''
     <x var="layout='view';
             batch=mode.batch;
             empty=mode.empty;
             showNewSearch=showNewSearch|True;
             showHeaders=showHeaders|True;
             specific=uiSearch.getResultsTop(mode, ajax)">

     <!-- Application, class-specific code before displaying results -->
     <x if="specific">::specific</x>

     <!-- Search results -->
     <div id=":mode.hook">
      <script>::mode.getAjaxData()</script>

      <!-- Pod templates -->
      <x if="not empty and not popup">
       <table var="fields=class_.getListPods()"
              if="fields and mode.objects" align=":dright">
        <tr>
         <td var="o=mode.objects[0]"
             for="field in fields" var2="fieldName=field.name"
             class=":not loop.field.last and 'pod' or ''">:field.pxRender</td>
        </tr>
       </table>
      </x>

      <!-- Title -->
      <h3 if="not popup"><x>::uiSearch.translated</x>
       <x if="mode.batch and not empty">(
        <span class="discreet">:mode.batch.total</span>)
       </x>
       <x if="uiSearch.search.add and guard.mayInstantiate(class_)"
          var2="asButton=True;
                nav=mode.getNavInfo(batch.total)">:class_.pxAdd</x>
       <x if="showNewSearch and mode.newSearchUrl">&nbsp;&mdash;&nbsp;<i> 
        <a href=":mode.newSearchUrl">:_('search_new')</a></i></x>
       <x if="mode.fromRef">&nbsp;&mdash;&nbsp;<i> 
        <a href=":mode.getRefUrl()">:_('goto_source')</a></i></x>
      </h3>
      <table width="100%">
       <tr valign="top">
        <!-- Search description -->
        <td if="uiSearch.translatedDescr">
         <span class="discreet">:uiSearch.translatedDescr</span><br/>
        </td>
        <!-- (Top) navigation -->
        <td if="mode.batch" align=":dright">:mode.batch.pxNavigate</td>
       </tr>
      </table>

      <!-- Results -->
      <x if="not empty" var2="currentNumber=0">:mode.px</x>

      <!-- (Bottom) navigation -->
      <x if="mode.batch">:mode.batch.pxNavigate</x>

      <!-- No result -->
      <x if="empty">
       <x>::_('query_no_result')</x>
       <x if="showNewSearch and mode.newSearchUrl"><br/><i class="discreet">
         <a href=":mode.newSearchUrl">:_('search_new')</a></i></x>
      </x>
    </div></x>''')

    def __init__(self, search, tool, ctx, initiator=None, name=None):
        self.search = search
        self.container = search.container
        self.tool = tool
        self.req = tool.req
        self.dir = ctx.dir
        self.popup = ctx.popup
        # "name" can be more than the p_search name, ie, if the search is
        # defined in a field.
        self.name = name or search.name
        self.type = 'search'
        self.colspan = search.colspan
        self.showActions = search.showActions
        self.actionsDisplay = search.actionsDisplay
        className = self.container.name
        if search.translated:
            self.translated = search.translated
            self.translatedDescr = search.translatedDescr or ''
        else:
            # The label may be specific in some special cases
            labelDescr = ''
            if search.name == 'allSearch': label = '%s_plural' % className
            elif search.name == 'customSearch': label = 'search_results'
            elif not search.name: label = None
            else:
                label = '%s_%s' % (className, search.name)
                labelDescr = label + '_descr'
            _ = tool.translate
            self.translated = label and _(label) or ''
            self.translatedDescr = labelDescr and _(labelDescr) or ''
        # Strip the description (a single space may be present)
        self.translatedDescr = self.translatedDescr.strip()
        # An initiator instance if the search is in a popup
        self.initiator = initiator
        # When search results are shown in a popup, checkboxes must be present
        # even when not shown. Indeed, we want them in the DOM because object
        # ids are stored on it.
        if initiator:
            self.checkboxes = True
            self.checkboxesDefault = False
        else:
            cb = search.checkboxes
            cb = cb(tool) if callable(cb) else cb
            self.checkboxes = cb
            self.checkboxesDefault = search.checkboxesDefault

    def getRootHook(self):
        '''If there is an initiator, return the hook as defined by it. Else,
           return the name of the search.'''
        init = self.initiator
        return init.popupHook if init else (self.search.name or 'search')

    def showCheckboxes(self):
        '''When must checkboxes be shown ?'''
        init = self.initiator
        return init.showCheckboxes() if init else self.checkboxes

    def getCbJsInit(self, hook):
        '''Returns the code that creates JS data structures for storing the
           status of checkboxes for every result of this search.'''
        default = self.checkboxesDefault and 'unchecked' or 'checked'
        return '''var node=findNode(this, '%s');
                  node['_appy_objs_cbs'] = {};
                  node['_appy_objs_sem'] = '%s';''' % (hook, default)

    def getModes(self):
        '''Gets all the modes applicable when displaying search results (being
           instances of p_class_) via this search (p_self). r_ is a list of
           names and not a list of Mode instances.'''
        r = self.search.resultModes or self.container.getResultModes() or \
            Mode.default
        return r if not callable(r) else r(self.tool)

    def getMode(self):
        '''Gets the current mode'''
        return Mode.get(self)

    def getTitleMode(self, popup):
        '''How titles to search results, being instances of p_class_, must be
           rendered ? r_ is:
           * "link" : as links allowing to go to instances' view pages;
           * "select": as objects that can be selected from a popup;
           * "text": as simple, unclickable text.
        '''
        if popup: return 'select'
        # Check if the title mode is specified on the container class
        mode = self.container.getTitleMode()
        if not mode: return 'link'
        return mode if not callable(mode) else mode(self.tool)

    def getResultsTop(self, mode, ajax):
        '''If p_class_ defines something to display on the results page just
           before displaying search results, returns it.'''
        # Get this only on the main page, not when ajax-refreshing search
        # results.
        if ajax: return
        return self.container.getResultsTop(self.tool, self.search, mode)

    def highlight(self, text):
        '''Highlight search results within p_text'''
        return Critera.highlight(self.tool.H(), text)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Search:
    '''Used for specifying a search for a given class'''

    traverse = {}
    # Special initiator in use when an object is being created from a Search. It
    # has nothing to do with popup-oriented initiator as defined hereafter.
    initiator = initiators.SearchInitiator

    def __init__(self, name=None, group=None, sortBy='title', sortOrder='asc',
                 maxPerPage=30, default=False, colspan=1, translated=None,
                 show=True, showActions='all', actionsDisplay='block',
                 translatedDescr=None, checkboxes=False, checkboxesDefault=True,
                 container=None, add=False, resultModes=None, shownInfo=None,
                 actions=None, **fields):
        # "name" is mandatory, excepted in some special cases (ie, when used as
        # "select" param for a Ref field).
        self.name = name
        # Searches may be visually grouped in the portlet
        self.group = Group.get(group)
        self.sortBy = sortBy
        self.sortOrder = sortOrder
        self.maxPerPage = maxPerPage
        # If this search is the default one, it will be triggered by clicking
        # on main link.
        self.default = default
        self.colspan = colspan
        # If a translated name or description is already given here, we will
        # use it instead of trying to translate from labels.
        self.translated = translated
        self.translatedDescr = translatedDescr
        # Condition for showing or not this search
        self.show = show
        # Attributes "showActions" and "actionsDisplay" are similar to their
        # homonyms on the Ref class.
        self.showActions = showActions
        self.actionsDisplay = actionsDisplay
        # In dict "fiels", keys are names of indexed fields and values are
        # simple search values or terms built with database operators.
        self.fields = fields
        # Must checkboxes be shown for every object of the search result ?
        self.checkboxes = checkboxes
        # Default value for checkboxes
        self.checkboxesDefault = checkboxesDefault
        # Most of the time, we know what is the class whose instances must be
        # searched. When it is not the case, the p_container can be explicitly
        # specified.
        if container and (container.__class__.__name__ != 'Class'):
            container = container.meta
        self.container = container
        # Is it possible to create new "container" instances from this search ?
        self.add = add
        # There can be various ways to display query results
        self.resultModes = resultModes
        # Similar to the homonym Ref attribute, "shownInfo" defines the columns
        # that must be shown on lists of result objects (mode "List" only). If
        # not specified, class's "listColumns" attributes is used.
        self.shownInfo = shownInfo
        # Specify here Action fields that must be shown as custom actions that
        # will be triggered on search results.
        self.actions = actions

    def init(self, class_):
        '''Lazy search initialisation'''
        self.container = class_

    def ui(self, o, ctx):
        '''Gets a UiSearch instance corresponding to this search'''
        return UiSearch(self, o, ctx)

    def isShowable(self, tool):
        '''Is this Search instance showable ?'''
        class_ = self.container
        r = self.show
        return r if not callable(r) else \
               tool.H().methods.call(tool, self.show, class_=class_)

    def getSessionKey(self):
        '''Returns the name of the key storing siblings of a given object in the
           context of this search.'''
        return '%s_%s' % (self.container.name, self.name)

    mergeAttributes = ('sortBy', 'sortOrder', 'showActions', 'actionsDisplay',
                       'actions', 'maxPerPage', 'resultModes', 'shownInfo',
                       'checkboxes', 'checkboxesDefault')

    def merge(self, other):
        '''Merge parameters from another search in p_other'''
        self.fields.update(other.fields)
        for name in self.mergeAttributes:
            setattr(self, name, getattr(other, name))

    def getActions(self, tool):
        '''Get the actions triggerable on p_self's results'''
        actions = self.actions
        if not actions: return
        r = []
        for action in actions:
            show = action.show
            show = show(tool) if callable(show) else show
            if show:
                r.append(action)
        return r

    def getField(self, name, handler):
        '''Gets the field whose name is p_name'''
        className = self.container.name
        return handler.server.model.classes.get(className).fields.get(name)

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  The "run" method
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def run(self, handler, batch=True, start=0, ids=False, secure=True,
            sortBy=None, sortOrder='asc', filters=None, refObject=None,
            refField=None, other=None):
        '''Based on p_self's parameters, and this method's attributes, perform a
           search in the corresponding catalog ans return the results.'''
        # If p_batch is True, the result is a appy.model.batch.Batch instance
        # returning only a subset of the results starting at p_start and
        # containing at most p_self.maxPerPage results. Else, it is a list of
        # objects (or object ids if p_ids is True) representing the complete
        # result set. If p_ids is True, p_batch is ignored and implicitly
        # considered being False.
        # ~~~
        # p_secure is transmitted and documented in called method
        # appy.database.catalog.Catalog.search (called via method
        # appy.database.Database.search).
        # ~~~
        # The result is sorted according to the potential sort key and order
        # ('asc'ending or 'desc'ending) as defined in p_self.sortBy and
        # p_self.sortOrder. If p_sortBy is not None, p_sortBy and p_sortOrder
        # override p_self's homonym attributes.
        # ~~~
        # p_filters alter search parameters according to selected filters in the
        # ui.
        # ~~~
        # If p_refObject and p_refField are given, the search is limited to the
        # objects being referenced from p_refObject through p_refField.
        # ~~~
        # If p_other is not None, it is another Search instance whose parameters
        # will be merged with p_self's parameters.
        # ~~~
        # Prepare search parameters
        className = self.container.name
        params = self.fields.copy()
        # Use the search's default sort key and order if not passed as args
        if not sortBy:
            sortBy = self.sortBy
            sortOrder = self.sortOrder
        # Take p_filters into account
        if filters:
            for name, value in filters.items():
                if not value: continue
                field = self.getField(name, handler)
                value = field.getSearchValue(None, value=value)
                if value: params[name] = value
        # Manage a potential Ref field
        if refObject:
            back = refField.back
            if back: params['cid'] = '%d_%s' % (refObject.iid, back.name)
        # Perform the search in the corresponding catalog, getting IIDs of
        # matched objects.
        database = handler.server.database
        r = database.search(handler, className, ids=True, secure=secure,
                            sortBy=sortBy, sortOrder=sortOrder, **params)
        # Return object IIDs if requested
        if ids: return r
        # Return the complete set of matched objects if p_batch is False
        if not batch: return database.getObjects(handler, r, className)
        # Create a Batch and populate it with the appropriate subset of objects
        batch = Batch(total=len(r), size=self.maxPerPage, start=start)
        batch.setObjects(database.getObjects(handler, r, className,
                                            start=batch.start, size=batch.size))
        return batch

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  Class methods
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    @classmethod
    def get(class_, name, tool, modelClass, ctx, ui=True):
        '''Gets the Search instance (or a UiSearch instance if p_ui is True)
           corresponding to the search named p_name, on class p_modelClass.'''
        initiator = None
        req = tool.req
        if name == 'customSearch':
            # It is a custom search
            if req.source == 'searchForm':
                # Search criteria are in the request, sent from the search form
                co = Criteria(tool)
                co.getFromRequest(modelClass)
                criteria = co.criteria
                # Set them on the request object: it will be used to store them
                # in the browser's session storage (see modes.py).
                req.criteria = co.asString()
            else:
                # Search criteria are carried in the request as a marshalled
                # string in key "criteria".
                criteria = Criteria.readFromRequest(tool.H()) or {}
            # Create the Search instance, ommitting the "_ref" attribute, that
            # does not correspond to any field.
            if '_ref' in criteria: del(criteria['_ref'])
            r = Search('customSearch', container=modelClass, **criteria)
            # Avoid name clash
            if 'group' in criteria: r.fields['group'] = criteria['group']
            # Take into account default params for the advanced search
            advanced = modelClass.getSearchAdvanced(tool)
            if advanced: r.merge(advanced)
        elif (name == 'allSearch') or not name:
            # It is the search for every instance of p_modelClass
            r = Search('allSearch', container=modelClass)
            name = r.name
            # Take into account default params for the advanced search
            advanced = modelClass.getSearchAdvanced(tool)
            if advanced: r.merge(advanced)
        elif name == 'fromSearch':
            # It is the search for selecting a template for creating an object
            fromClass = req.fromClass
            sourceField = req.sourceField
            if sourceField:
                # We are creating an object from a Ref field
                id, fieldName = sourceField.split(':')
                o = tool.getObject(id)
                r = o.getField(fieldName).getAttribute(o, 'createVia')
            else:
                # We are creating a root object
                tool.model.classes.get(fromClass).getCreateVia(tool)
            initiator = initiators.TemplateInitiator(fromClass, req.formName,
                                                     req.insert, sourceField)
        elif ',' in name:
            # The search is defined in a field
            id, fieldName, mode = name.split(',')
            # Get the object with this "id". In the case of a Ref field with
            # link=popup, the initiator object can be a temp object.
            o = tool.getObject(id)
            field = o.getField(fieldName)
            if field.type == 'Ref':
                initiator = initiators.RefInitiator(o, field, fieldName, mode)
                r = field.getSelect(o)
            elif field.type == 'Computed':
                r = field.getSearch(o)
        else:
            # Search among static searches
            r = modelClass.searches.get(name)
            if not r:
                # Search among dynamic searches
                dyn = modelClass.getDynamicSearches(tool)
                if dyn:
                    for search in dyn:
                        if search.name == name:
                            r = search
                            break
        # The search may not exist
        if not r: tool.raiseUnauthorized(tool.translate('search_broken'))
        # Return a UiSearch if required
        return r if not ui else UiSearch(r, tool, ctx, initiator, name)

    @classmethod
    def getRefInfo(class_, tool, info=None, nameOnly=True):
        '''When a search is restricted to objects referenced through a Ref
           field, this method returns information about this reference: the
           source object and the Ref field.'''
        if not info:
            criteria = Criteria.readFromRequest(tool.H())
            if criteria and ('_ref' in criteria): info = criteria['_ref']
        if not info: return None, None
        id, field = info.split(':')
        o = tool.getObject(id)
        field = field if nameOnly else o.getField(field)
        return o, field

    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    #  PXs
    #  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Display results of a search whose name is in the request
    results = Px('''
     <div var="hook=uiSearch.getRootHook()" id=":hook">
      <script>:uiSearch.getCbJsInit(hook)</script>
      <x>::ui.Globals.getForms(tool)</x>
      <div align=":dright" if="len(resultModes) &gt; 1">
       <select name="px"
               onchange=":'switchResultMode(this, %s)' % q('searchResults')">
        <option for="mode in resultModes"
                value=":mode">:uiSearch.Mode.getText(mode, _)</option>
       </select>
      </div>
      <x>:uiSearch.pxResult</x>
     </div>''',

     js='''
       function switchResultMode(select, hook) {
         var mode = select.options[select.selectedIndex].value;
         askAjax(hook, null, {'resultMode': mode});
       }''',

     template=Template.px, hook='content')

    traverse['jresults'] = True
    @classmethod
    def jresults(class_, tool):
        '''Returns, as a JSON dict, in the context of a search whose name is in
           the request, the indexes of the siblings object of the one whose
           index is in the request.'''
        req = tool.req
        # The index of the current object
        index = int(req.index)
        # Get the search
        modelClass = tool.model.classes.get(req.className)
        search = class_.get(req.search, tool, modelClass, None, ui=False)
        # Determine the start of the batch search surrounding the object being
        # at "index".
        size = search.maxPerPage
        start = index - int(size / 2)
        if start < 0: start = 0
        # Perform the search
        ids = search.run(tool.H(), ids=True)
        r = {}
        i = start
        end = start + size
        while i < end:
            try:
                r[i] = ids[i]
            except IndexError:
                break
            i += 1
        tool.resp.setContentType('json')
        return sutils.getStringFrom(r, c='"')

    # Display results of a live search
    liveResults = Px('''
     <div var="objects=uiSearch.search.run(handler).objects"
          id=":'%s_LSResults' % className">
      <p if="not objects" class="lsNoResult">::_('query_no_result')</p>
      <div for="o in objects" style="padding: 3px 5px">
       <a href=":o.url" var="content=Px.truncateValue(o.title, width=80)"
          title=":o.title">:content</a>
      </div>
      <!-- Go to the page showing all results -->
      <div if="objects" align=":dright" style="padding: 3px">
       <a class="clickable" style="font-size: 80%; font-style: italic"
          onclick=":'document.forms[%s].submit()' % \
            q('%s_LSForm' % className)">:_('search_results_all') + '...'</a>
      </div>
     </div>''')

    # The advanced search form
    advanced = Px('''
     <x var="refInfo=req.ref;
             fields,css,js,gridder=class_.getSearchFields(tool, refInfo);
             layout='search'">

      <!-- Include type-specific CSS and JS -->
      <x>::ui.Includer.getSpecific(tool, css, js)</x>
      <script>var errors = null;</script>

      <!-- Search title -->
      <h1><x>:_('%s_plural' % className)</x> &ndash;
          <x>:_('search_title')</x></h1>

      <!-- Form for searching objects of the requested class -->
      <form name="search" action=":'%s/Search/results' % tool.url"
            method="post">
       <input type="hidden" name="className" value=":className"/>
       <input type="hidden" name="source" value="searchForm"/>
       <input type="hidden" name="search" value="customSearch"/>
       <input if="refInfo" type="hidden" name="ref" value=":refInfo"/>

       <!-- The search fields -->
       <div style=":gridder.getContainerStyle() + ';margin-bottom: 1em'">
         <div for="field in fields"
            style=":'grid-column:span %d' %field.scolspan">:field.pxRender</div>
       </div>

       <!-- Submit button -->
       <input var="label=_('search_button');
                   css=ui.Button.getCss(label, small=False)"
              type="submit" class=":css" value=":label"
              style=":url('search', bg=True)"/>
      </form>
     </x>''', template=Template.px, hook='content')

    # The live search form
    live = Px('''
     <form var="formId='%s_LSForm' % className"
           id=":formId" name=":formId" action=":'%s/Search/results' % toolUrl">
      <input type="hidden" name="className" value=":className"/>
      <input type="hidden" name="search" value="customSearch"/>
      <input type="hidden" name="source" value="searchForm"/>
      <table var="searchLabel=_('search_button')">
       <tr valign="bottom">
        <td style="position: relative">
         <input type="text" size="14" name="w_searchable" autocomplete="off"
                id=":'%s_LSinput' % className" class="inputSearch"
                title=":searchLabel"
                var="jsCall='onLiveSearchEvent(event, %s, %s, %s)' % \
                             (q(className), q('auto'), q(toolUrl))"
                onkeyup=":jsCall" onfocus=":jsCall"
                onblur=":'onLiveSearchEvent(event, %s, %s)' % \
                         (q(className), q('hide'))"/>
         <!-- Dropdown containing live search results -->
         <div id=":'%s_LSDropdown' % className" class="dropdown liveSearch">
          <div id=":'%s_LSResults' % className"></div>
         </div>
        </td>
        <td><input type="image" src=":url('search')" title=":searchLabel"/></td>
       </tr>
      </table>
     </form>''',

     css='''
       .liveSearch a, .liveSearch a:visited { color: #1f549a }
       .lsSelected { background-color: #d9d7d9 }
       .lsNoResult { color: #1f549a }''',

     # Live-search-related functions (LS)
     js='''
       function detectEventType(event) {
         /* After p_event occurred on a live search input field, must we trigger
            a search (a new char has been added), move up/down within the search
            results (key up/down has been pressed) or hide the dropdown
            (escape)? */
         if (event.type == 'focus') return 'search'
         switch (event.keyCode) {
           case 38: return 'up';
           case 40: return 'down';
           case 27: return 'hide'; // escape
           case 13: return 'go'; // cr
           case 37: break; // left
           case 39: break; // right
           default: return 'search';
         }
       }

       /* Function that selects the search result within the dropdown, after the
          user has pressed the 'up' od 'down' key (p_direction). */
       function selectLSResult(dropdown, direction){
         var results = dropdown.children[0].getElementsByTagName('div');
         if (results.length == 0) return;
         var j; // The index of the new element to select
         for (var i=0, len=results.length; i<len; i++) {
           if (results[i].className == 'lsSelected') {
             if (direction == 'up') {
               if (i > 0) j = i-1;
               else j = len-1;
             }
             else {
               if (i < (len-1)) j = i+1;
               else j = 0;
             }
             results[i].className = '';
             results[j].className = 'lsSelected';
             break;
           }
         }
         if (isNaN(j)) results[0].className = 'lsSelected';
       }

       // Function that allows to go to a selected search result
       function gotoLSLink(dropdown) {
         var a, results = dropdown.children[0].getElementsByTagName('div');
         for (var i=0, len=results.length; i<len; i++) {
           if (results[i].className == 'lsSelected') {
             a = results[i].children[0];
             if (a.href) window.location = a.href;
             else eval(a.onclick);
           }
         }
       }
    
       function hideLSDropdown(dropdown, timeout) {
         if (dropdown.style.display == 'none') return;
         if (!timeout) { dropdown.style.display = 'none'; return; }
         lsTimeout = setTimeout(function(){
           dropdown.style.display = 'none';}, 400);
       }

       // Function managing an p_event triggered from the LS input field
       function onLiveSearchEvent(event, class_, action, toolUrl) {
         var dropdown = document.getElementById(class_ + '_LSDropdown');
         if (lsTimeout) clearTimeout(lsTimeout);
         // Hide the dropdown if action is forced to 'hide'
         if (action == 'hide') { hideLSDropdown(dropdown, true); return; }
         // Detect if the dropdown must be shown or hidden
         var input = document.getElementById(class_ + '_LSinput');
         if (input.value.length > 2) {
           var eventType = detectEventType(event);
           if (!eventType) return;
           if (eventType == 'hide') { hideLSDropdown(dropdown, false); return;}
           if (eventType == 'go') { gotoLSLink(dropdown); return; }
           if (eventType == 'search') {
             // Trigger an Ajax search and refresh the dropdown content
             var f = document.getElementById(class_ + '_LSForm'),
                 formElems = f.elements,
                 params = {}, param;
             for (var i=0, len=formElems.length; i<len; i++) {
               param = formElems.item(i);
               params[param.name] = param.value;
             }
             lsTimeout = setTimeout(function() {
               askAjaxChunk(toolUrl + '/Search/liveResults', 'GET', params,
                            class_+ '_LSResults');
               dropdown.style.display = 'block';}, 400);
             }
           else { // Move up or down within results
             selectLSResult(dropdown, eventType);
           }
         }
         else { hideLSDropdown(dropdown, true); }
       }''')

    # An alias to batch results
    batchResults = UiSearch.pxResult
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
