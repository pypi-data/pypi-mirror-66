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
import hashlib, copy
from appy.px import Px
from appy.model.fields import Field
from appy.model.utils import Object as O

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''If you plan, in your app, to perform on-line payments via the Ogone (r)
       system, create an instance of this class in your app and place it in the
       'ogone' attr of your appy.gen.Config class.'''
    def __init__(self):
        # self.env refers to the Ogone environment and can be "test" or "prod".
        self.env = 'test'
        # You merchant Ogone ID
        self.PSPID = None
        # Default currency for transactions
        self.currency = 'EUR'
        # Default language
        self.language = 'en_US'
        # SHA-IN key (digest will be generated with the SHA-1 algorithm)
        self.shaInKey = ''
        # SHA-OUT key (digest will be generated with the SHA-1 algorithm)
        self.shaOutKey = ''

    def __repr__(self): return str(self.__dict__)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Ogone(Field):
    '''This field allows to perform payments with the Ogone (r) system'''

    # Some elements will be traversable
    traverse = Field.traverse.copy()

    urlTypes = ('accept', 'decline', 'exception', 'cancel')

    view = cell = Px('''<x>
     <!-- var "value" is misused and contains the contact params for Ogone -->
     <!-- The form for sending the payment request to Ogone -->
     <form method="post" id="form1" name="form1" var="env=value['env']"
           action=":'https://secure.ogone.com/ncol/%s/orderstandard.asp'% env">
       <input type="hidden" for="item in value.items()" if="item[0] != 'env'"
              id=":item[0]" name=":item[0]" value=":item[1]"/>
       <!-- Submit image -->
       <input type="image" id="submit2" name="submit2" src=":url('ogone.gif')"
              title=":_('custom_pay')"/>
     </form>
    </x>''')

    edit = search = ''

    def __init__(self, orderMethod, responseMethod, show='view', page='main',
      group=None, layouts=None, move=0, readPermission='read',
      writePermission='write', width=None, height=None, colspan=1, master=None,
      masterValue=None, focus=False, mapping=None, generateLabel=None,
      label=None, view=None, cell=None, edit=None, xml=None, translations=None):
        Field.__init__(self, None, (0,1), None, None, show, page, group,
          layouts, move, False, True, None, None, False, None, readPermission,
          writePermission, width, height, None, colspan, master, masterValue,
          focus, False, mapping, generateLabel, label, None, None, None, None,
          False, False, view, cell, edit, xml, translations)
        # orderMethod must contain a method returning a dict containing info
        # about the order. Following keys are mandatory:
        #   * orderID   An identifier for the order. Don't use the object ID
        #               for this, use a random number, because if the payment
        #               is canceled, Ogone will not allow you to reuse the same
        #               orderID for the next tentative.
        #   * amount    An integer representing the price for this order,
        #               multiplied by 100 (no floating point value, no commas
        #               are tolerated. Dont't forget to multiply the amount by
        #               100!
        self.orderMethod = orderMethod
        # responseMethod must contain a method accepting one param, let's call
        # it "response". The response method will be called when we will get
        # Ogone's response about the status of the payment. Param "response" is
        # an object whose attributes correspond to all parameters that you have
        # chosen to receive in your Ogone merchant account. After the payment,
        # the user will be redirected to the object's view page, excepted if
        # your method returns an alternatve URL.
        self.responseMethod = responseMethod

    noShaInKeys = ('env',)
    noShaOutKeys = ('name', 'SHASIGN')

    def createShaDigest(self, values, passphrase, keysToIgnore=()):
        '''Creates an Ogone-compliant SHA-1 digest based on key-value pairs in
           dict p_values and on some p_passphrase.'''
        # Create a new dict by removing p_keysToIgnore from p_values, and by
        # upperizing all keys.
        shaRes = {}
        for k, v in values.items():
            if k in keysToIgnore: continue
            # Ogone: we must not include empty values.
            if (v is None) or (v == ''): continue
            shaRes[k.upper()] = v
        # Create a sorted list of keys
        keys = list(shaRes.keys())
        keys.sort()
        shaList = []
        for k in keys:
            shaList.append('%s=%s' % (k, shaRes[k]))
        shaObject = hashlib.sha1(passphrase.join(shaList) + passphrase)
        return shaObject.hexdigest()

    def getValue(self, o, name=None, layout=None):
        '''The "value" of the Ogone field is a dict that collects all the
           necessary info for making the payment.'''
        tool = o.tool
        # Basic Ogone parameters were generated in the app config module.
        r = copy.deepcopy(o.config.ogone)
        shaKey = r.shaInKey
        # Remove elements from the Ogone config that we must not send in the
        # payment request.
        r.shaInKey = r.shaOutKey = None
        for name, value in self.callMethod(o, self.orderMethod).items():
            setattr(r, name, value)
        # Add user-related information
        user = o.user
        r.CN = user.getTitle(normalized=True)
        r.EMAIL = user.email or user.login
        # Add standard back URLs
        siteUrl = o.siteUrl
        r.catalogurl = r.homeurl = siteUrl
        # Add redirect URLs
        for t in self.urlTypes:
            setattr(r, '%surl' % t, '%s/%s/process' % (o.url, self.name))
        # Add additional parameter that we want Ogone to give use back in all
        # of its responses: the name of this Appy Ogone field. This way, Appy
        # will be able to call method m_process below, that will process
        # Ogone's response.
        r.paramplus = 'name=%s' % self.name
        # Ensure every value is a str
        for k, v in r.__dict__.items():
            if not isinstance(v, str):
                setattr(r, v, str(v))
        # Compute a SHA-1 key as required by Ogone and add it to the result
        r.SHASign = self.createShaDigest(r, shaKey,
                                         keysToIgnore=self.noShaInKeys)
        return r.__dict__

    def ogoneResponseOk(self, o):
        '''Returns True if the SHA-1 signature from Ogone matches retrieved
           params.'''
        resp = o.resp
        shaKey = o.config.ogone.shaOutKey
        digest = self.createShaDigest(resp, shaKey,
                                      keysToIgnore=self.noShaOutKeys)
        return digest.lower() == resp.SHASIGN.lower()

    traverse['process'] = 'perm:view'
    def process(self, o):
        '''Processes a response from Ogone'''
        # Call the response method defined in this Ogone field.
        if not self.ogoneResponseOk(o):
            o.log('Ogone response SHA failed. REQUEST: %s' % str(o.req.d()))
            raise Exception('Failure, possible fraud detection, an ' \
                            'administrator has been contacted.')
        # Create a nice object from the form
        response = O()
        for k, v in o.req.items():
            setattr(response, k, v)
        # Call the field method that handles the response received from Ogone.
        # Redirect the user to the correct page. If the field method returns
        # some URL, use it. Else, use the view page of p_o.
        url = self.responseMethod(o, response) or o.url
        o.goto(url)
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
