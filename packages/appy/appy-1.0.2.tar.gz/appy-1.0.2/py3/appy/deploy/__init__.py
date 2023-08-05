'''Deployment system for Appy sites and apps'''

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
import os, sys

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Target:
    '''Represents a app deployed on a site on a distant machine'''

    def __init__(self, sshHost, sshPort=22, sshLogin='root', sshKey=None):
        # The name of the distant host, for establishing a SSH connection
        self.sshHost = sshHost
        # The port for the SSH connection
        self.sshPort = sshPort
        # The login used to connect to the host in SSH
        self.sshLogin = sshLogin
        # The private key used to connect to the host in SSH
        self.sshKey = sshKey

    def __repr__(self):
        '''p_self's string representation'''
        return '<Target %s:%d>' % (self.sshHost, self.sshPort)

    def execute(self, command):
        '''Executes p_command on this target'''
        r = ['ssh', '%s@%s' % (self.sshLogin, self.sshHost), '"%s"' % command]
        # Determine port
        if self.sshPort != 22: r.insert(1, '-p%d' % self.sshPort)
        # Determine "-i" option (path to the private key)
        if self.sshKey: r.insert(1, '-i %s' % self.sshKey)
        # Build the complete command
        r = ' '.join(r)
        print('Executing: %s...' % r)
        os.system(r)

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Config:
    '''Deployment configuration'''

    def __init__(self):
        # This dict stores all the known targets for deploying this app. Keys
        # are target names, values are Target instances. The default target must
        # be defined at key "default".
        self.targets = {}

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
NO_CONFIG = 'The "deploy" config was not found in config.deploy.'
NO_TARGET = 'No target was found on config.deploy.targets.'
TARGET_KO = 'Target "%s" not found. Available target(s): %s.'

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class Deployer:
    '''App deployer'''

    # OS packages being Appy dependencies
    osDependencies = 'libreoffice subversion python3-pip apache2'

    # Python packages being Appy dependencies
    pythonDependencies = 'zodb DateTime python-ldap appy'

    def __init__(self, app, site, command, targetName='default'):
        # The path to the app
        self.app = app
        # The path to the reference, local site, containing targets definition
        self.site = site
        # The chosen target (name)
        self.targetName = targetName or 'default'
        self.target = None # Will hold a Target instance
        # The command to execute
        self.command = command
        # The app config
        self.config = None

    def list(self):
        '''Lists the available targets on the config'''
        infos = []
        for name, target in self.config.deploy.targets.items():
            info = '*** Target: %s\n%s' % (name, target)
            infos.append(info)
        infos = '\n\n'.join(infos)
        print('Available target(s) for app "%s", from reference site "%s":\n' \
              '%s' % (self.app.name, self.site.name, infos))

    def info(self):
        '''Retrieve info about the target OS'''
        self.target.execute('cat /etc/lsb-release')

    def install(self):
        '''Installs required dependencies on the target via "apt" and "pip3"'''
        target = self.target
        # Install required dependencies via Aptitude
        apt = 'DEBIAN_FRONTEND=noninteractive apt-get -yq install'
        target.execute('%s %s' % (apt, Deployer.osDependencies))
        # Install Python dependencies via "pip3"
        target.execute('pip3 install %s' % Deployer.pythonDependencies)

    def run(self):
        '''Performs p_self.command on the specified p_self.targetName'''
        # Add the relevant paths to sys.path
        for path in (self.site, self.site/'lib', self.app.parent):
            sys.path.insert(0, str(path))
        # Get the config and ensure it is complete
        self.config = __import__(self.app.name).Config
        cfg = self.config.deploy
        if not cfg:
            print(NO_CONFIG)
            sys.exit(1)
        targets = cfg.targets
        if not targets:
            print(NO_TARGET)
            sys.exit(1)
        # Get the target
        name = self.targetName
        target = self.target = targets.get(name)
        if not target:
            print(TARGET_KO % (name, ', '.join(targets)))
            sys.exit(1)
        getattr(self, self.command)()
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
