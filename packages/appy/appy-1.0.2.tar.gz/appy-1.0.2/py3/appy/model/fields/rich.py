# -*- coding: utf-8 -*-

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
import sys

from appy.px import Px
from appy.ui.layout import Layouts
from appy.model.fields import Field
from appy.xml.cleaner import Cleaner
from appy.utils.diff import HtmlDiff
from appy.model.fields.text import Text
from appy.ui.layout import Layouts, Layout
from appy.model.fields.multilingual import Multilingual

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NOT_IMPLEMENTED = 'This feature is not implemented yet'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Rich(Multilingual, Field):
    '''Field allowing to encode a "rich" text, based on XHTML and external
       editor "ckeditor".'''

    # Required Javascript files
    cdnUrl = 'https://cdn.ckeditor.com/%s/%s/ckeditor.js'

    # Use this constant to say that there is no maximum size for a string field
    NO_MAX = sys.maxsize

    class Layouts(Layouts):
        '''Rich-specific layouts'''
        b = Layouts(edit='lrv-d-f', view='l-f')
        c = Layouts(edit='lrv-d-f', view='lc-f') # Idem but with history
        g = Layouts(edit=Layout('d2-f;rv=', width='99%'),
                    view=Layout('fl', width='99%'))
        gc = Layouts(edit=Layout('drv-f', width='99%'),
                     view=Layout('cl-f', width='99%')) # Idem but with history

        @classmethod
        def getDefault(class_, field):
            '''Default layouts for this Rich p_field'''
            # Is this field in a grid-style group ?
            inGrid = field.inGrid()
            if field.historized:
                # self.historized can be a method or a boolean. If it is a
                # method, it means that under some condition, historization will
                # be enabled. So we come here also in this case.
                r = 'gc' if inGrid else 'c'
            else:
                r = 'g' if inGrid else 'b'
            return getattr(class_, r)

    # Default ways to render multilingual fields
    defaultLanguagesLayouts = {
      'edit': 'horizontal', 'view': 'horizontal', 'cell': 'vertical'}

    # Override this dict, defined at the Multilingual level
    lgTop = {'view': 1, 'edit': 1}

    # Default styles to use
    defaultStyles = ('p', 'h1', 'h2', 'h3', 'h4')

    # Default custom style, allowing to produce, in POD results, a page break
    # just after the paragraph having this style.
    customStyles = [{'id': 'div', 'element': 'div',
                     'attributes': {'style': 'page-break-after:always'}}]

    # The name of the index class storing values of this field in the catalog
    indexType = 'RichIndex'

    # Unilingual view and cell
    viewUni = cellUni = Px('''
     <x var="inlineEdit=field.getAttribute(o, 'inlineEdit');
             mayAjaxEdit=inlineEdit and (layout != 'cell') and not \
                       showChanges and guard.mayEdit(o, field.writePermission)">
      <div if="not mayAjaxEdit" class="xhtml">::value or '-'</div>
      <x if="mayAjaxEdit" var2="name=lg and ('%s_%s' % (name, lg)) or name">
       <div class="xhtml" contenteditable="true"
            id=":'%d_%s_ck' % (o.iid, name)">::value or '-'</div>
       <script if="mayAjaxEdit">::field.getJsInlineInit(o, name, lg)</script>
      </x>
     </x>''')

    # Unilingual edit
    editUni = Px('''
     <textarea var="inputId=not lg and name or '%s_%s' % (name, lg)"
       id=":inputId" name=":inputId" cols=":field.getTextareaCols()"
       style=":field.getTextareaStyle()"
       rows=":field.height">:field.getInputValue(inRequest, requestValue, value)
     </textarea>
     <script>::field.getJsInit(o, lg)</script>''')

    search = Px('''
     <input type="text" maxlength=":field.maxChars" size=":field.swidth"
            value=":field.sdefault" name=":widgetName"/>''')

    def __init__(self, validator=None, multiplicity=(0,1), default=None,
      defaultOnEdit=None, show=True, page='main', group=None, layouts=None,
      move=0, indexed=False, mustIndex=True, indexValue=None, searchable=False,
      filterField=None, readPermission='read', writePermission='write',
      width=None, height=None, maxChars=None, colspan=1, master=None,
      masterValue=None, focus=False, historized=False, mapping=None,
      generateLabel=None, label=None, sdefault='', scolspan=1, swidth=None,
      sheight=None, persist=True, styles=defaultStyles, customStyles=None,
      allowImageUpload=False, spellcheck=False, languages=('en',),
      languagesLayouts=None, inlineEdit=False, toolbar='Standard', view=None,
      cell=None, edit=None, xml=None, translations=None):
        # The list of styles that the user will be able to select in the styles
        # dropdown (within CKEditor) is defined hereafter.
        self.styles = styles
        # If you want to add custom, non-standard styles in the above-mentioned
        # dropdown, do not touch attribute "styles", but specify such entries in
        # the following attribute "customStyles". It must be a list or dict of
        # entries; every entry represents a custom style and must be a dict
        # having the following keys and values. Every key and value must be a
        # string.
        # ----------------------------------------------------------------------
        #    "id"    | An identifier for your style, that must be different from
        #            | any standard CKEditor style like h1, h2, p, div, etc;
        # ----------------------------------------------------------------------
        #   "name"   | A translated name for your style, that will appear in the
        #            | dropdown. Do not use any special (ie, accentuated) char
        #            | in the value: prefer the use of an HTML entity for
        #            | defining such char.
        # ----------------------------------------------------------------------
        #  "element" | The HTML tag that will surround the text onto which the
        #            | style will be applied. Do not use "blockquote", it does
        #            | not work. Non-standard tag "address" works well, or any
        #            | standard tag like h1, h2, etc. Note that if you use a
        #            | standard tag, it will work, but if you have also
        #            | activated it in attribute "style" hereabove, you won't be
        #            | able to make the difference in the result between both
        #            | styles because they will produce a similar result.
        # ----------------------------------------------------------------------
        self.customStyles = customStyles or Rich.customStyles
        # Do we allow the user to upload images in it ?
        self.allowImageUpload = allowImageUpload
        if allowImageUpload: raise Exception(NOT_IMPLEMENTED)
        # Do we run the CK spellchecker ?
        self.spellcheck = spellcheck
        # What toolbar is used ? Possible values are "Standard" or "Simple"
        self.toolbar = toolbar
        # Call the base constructors
        Multilingual.__init__(self, languages, languagesLayouts)
        Field.__init__(self, validator, multiplicity, default, defaultOnEdit,
          show, page, group, layouts, move, indexed, mustIndex, indexValue,
          None, searchable, filterField, readPermission, writePermission, width,
          height, maxChars, colspan, master, masterValue, focus, historized,
          mapping, generateLabel, label, sdefault, scolspan, swidth, sheight,
          persist, inlineEdit, view, cell, edit, xml, translations)
        # No max chars by default
        if maxChars is None:
            self.maxChars = Rich.NO_MAX

    def getDiffValue(self, o, value, i=None, language=None):
        '''If p_i is None, p_value is p_self's currently stored value on p_o (or
           its p_language part if p_language is specified) and the method will
           return a version of p_value that includes the cumulative diffs
           between successive versions, from the very first stored version in
           p_o's history to the currently stored p_value.

           If p_i is given, p_value is p_self's value as stored in the entry
           whose index is p_i-1 in p_o's history, and the method will return a
           diff between it and p_value's subsequent version, either to be found
           in a more recent entry in p_o's history or, failing that, the
           currently stored value on p_o.'''
        r = last = None
        for event in o.history.iter(eventType='Change',chronological=True,i=i):
            # Ignore irrelevant events
            if not event.hasField(self.name, language=language): continue
            # We have a matching event
            if i is not None:
                # Return the diff between p_value and the newer version stored
                # in this event.
                newer = event.getValue(self.name, language)
                iMsg, dMsg = o.history[i+1].getDiffTexts(o)
                return HtmlDiff(value, newer, iMsg, dMsg).get()
            # If we are here, we must produce a cumulative diff
            if r is None:
                # This is the first encountered version
                r = event.getValue(self.name, language)
            else:
                # We need to produce the difference between current result
                # and this version.
                newer = event.getValue(self.name, language)
                iMsg, dMsg = last.getDiffTexts(o)
                r = HtmlDiff(r, newer, iMsg, dMsg).get()
            # Remember the last walked event
            last = event
        if not last:
            # There is no diff to show
            return value
        # Now we need to compare the result with the current version
        iMsg, dMsg = last.getDiffTexts(o)
        return HtmlDiff(r, value or '', iMsg, dMsg).get()

    def getUniFormattedValue(self, o, value, layout='view', showChanges=False,
                             language=None, contentLanguage=None):
        '''Returns the formatted variant of p_value. If p_contentLanguage is
           specified, p_value is the p_contentLanguage part of a multilingual
           value.'''
        if Field.isEmptyValue(self, o, value) and not showChanges: return ''
        r = value
        if showChanges:
            # Compute the successive changes that occurred on p_value
            r = self.getDiffValue(o, r, language=contentLanguage)
        return r

    def getSearchValue(self, req, value=None):
        '''The input widget for a Rich field is of type "text". So behave like a
           Text field in that case.'''
        return Text.computeSearchValue(self, req, value=value)

    def getHistoryValue(self, o, value, i, language=None, empty='-'):
        '''For a Rich field, instead of showing the previous p_value in p_o's
           history, we show a XHTML diff between p_value and the new value, as
           currently stored on p_o or as stored in a more recent entry in p_o's
           history.'''
        r = Field.getHistoryValue(self, o, value, i, language, empty=None)
        return empty if not r else self.getDiffValue(o, value, i=i-1,
                                                     language=language)

    def getUniStorableValue(self, o, value):
        '''Gets the p_value as can be stored in the database within p_obj'''
        if not value: return value
        # Clean the value. When image upload is allowed, ckeditor inserts some
        # "style" attrs (ie for image size when images are resized). So in this
        # case we can't remove style-related information.
        try:
            value = Cleaner().clean(value)
        except Cleaner.Error:
            # Errors while parsing p_value can't prevent the user from storing
            # it.
            pass
        # Manage maxChars
        max = self.maxChars
        if max and (len(value) > max): value = value[:max]
        return value

    def getTextareaStyle(self):
        '''On "edit", get the content of textarea's "style" attribute'''
        # If the width is expressed as a string, the field width must be
        # expressed in attribute "style" (so returned by this method) and not
        # via attribute "cols" (returned by m_getTextareaCols below).
        return isinstance(self.width, str) and ('width:%s' % self.width) or ''

    def getTextareaCols(self):
        '''When this widget must be rendered as an HTML field of type
           "textarea", get the content of its "cols" attribute.'''
        # Use this attribute only if width is expressed as an integer value
        return isinstance(self.width, int) and self.width or ''

    ckLanguages = {'en': 'en_US', 'pt': 'pt_BR', 'da': 'da_DK', 'nl': 'nl_NL',
                   'fi': 'fi_FI', 'fr': 'fr_FR', 'de': 'de_DE', 'el': 'el_GR',
                   'it': 'it_IT', 'nb': 'nb_NO', 'pt': 'pt_PT', 'es': 'es_ES',
                   'sv': 'sv_SE'}

    def getCkLanguage(self, o, language):
        '''Gets the language for CK editor SCAYT. p_language is one of
           self.languages if the field is multilingual, None else. If p_language
           is not supported by CK, we use english.'''
        if not language:
            language = self.getAttribute(o, 'languages')[0]
        if language in self.ckLanguages: return self.ckLanguages[language]
        return 'en_US'

    def getCkParams(self, o, language):
        '''Gets the base params to set on a rich text field'''
        base = '%s/ckeditor' % o.buildUrl()
        ckAttrs = {'customConfig': '%s/config.js' % base,
                   'contentsCss': '%s/contents.css' % base,
                   'stylesSet': '%s/styles.js' % base,
                   'toolbar': self.toolbar, 'format_tags':';'.join(self.styles),
                   'scayt_sLang': self.getCkLanguage(o, language)}
        if self.width: ckAttrs['width'] = self.width
        if self.height: ckAttrs['height'] = self.height
        if self.spellcheck: ckAttrs['scayt_autoStartup'] = True
        # Add custom styles
        if self.customStyles:
            for style in self.customStyles:
                id = style['id']
                ckAttrs['format_%s' % id] = style
                ckAttrs['format_tags'] += ';%s' % id
        if self.allowImageUpload:
            ckAttrs['filebrowserUploadUrl'] = '%s/upload' % o.url
        if not o.user.hasRole('Manager'):
            ckAttrs['removeButtons'] = 'Source'
        ck = []
        for k, v in ckAttrs.items():
            if isinstance(v, int): sv = str(v)
            elif isinstance(v, bool): sv = str(v).lower()
            elif isinstance(v, dict): sv = str(v)
            else: sv = '"%s"' % v
            ck.append('%s: %s' % (k, sv))
        return ', '.join(ck)

    def getJs(self, layout, r, config):
        '''A rich field depend on CKeditor'''
        if layout not in ('edit', 'view'): return
        # Compute the URL to ckeditor CDN
        ckUrl = Rich.cdnUrl % (config.ui.ckVersion, config.ui.ckDistribution)
        if ckUrl not in r: r.append(ckUrl)

    def getJsInit(self, o, language):
        '''Gets the Javascript init code for displaying a rich editor for this
           field (rich field only). If the field is multilingual, we must init
           the rich text editor for a given p_language (among self.languages).
           Else, p_languages is None.'''
        name = self.name if not language else '%s_%s' % (self.name, language)
        return 'CKEDITOR.replace("%s", {%s})' % \
               (name, self.getCkParams(o, language))

    def getJsInlineInit(self, o, name, language):
        '''Gets the Javascript init code for enabling inline edition of this
           field (rich text only). If the field is multilingual, the current
           p_language is given and p_name includes it. Else, p_language is
           None.'''
        id = o.iid
        fieldName = language and name.rsplit('_',1)[0] or name
        lg = language or ''
        return "CKEDITOR.disableAutoInline = true;\n" \
               "CKEDITOR.inline('%d_%s_ck', {%s, on: {blur: " \
               "function( event ) { var content = event.editor.getData(); " \
               "doInlineSave('%d','%s','%s','view',true,content,'%s')}}})" % \
               (id, name, self.getCkParams(o,language), id, fieldName, o.url,lg)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
