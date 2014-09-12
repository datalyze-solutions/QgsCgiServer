# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgisCgiServer
                                 A QGIS plugin
 Provides a simple cgi server integrated into qgis, so you can call internal functions from web.
                              -------------------
        begin                : 2014-09-12
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Matthias Ludwig - Datalyze Solutions
        email                : m.ludwig@datalyze-solutions.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from PyQt4 import QtGui
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from QgisCgiServer_dialog import QgisCgiServerDialog
import os.path

from qgis.core import *
from qgis.gui import *


### important
import qtreactor.qt4reactor as qt4reactor
try:
    qt4reactor.install()
except qt4reactor.ReactorAlreadyInstalledError:
    print "still installed, doing nothing"
except AttributeError:
    pass
except:
    raise

## INSTALL qt4reactor before importing the twisted stuff
from twisted.internet import reactor
from twisted.web import server    

###


class QgisCgiServer:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'QgisCgiServer_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = QgisCgiServerDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Cgi Server Plugin')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'QgisCgiServer')
        self.toolbar.setObjectName(u'QgisCgiServer')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('QgisCgiServer', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the InaSAFE toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/QgisCgiServer/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Cgi Server Plugin'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Cgi Server Plugin'),
                action)
            self.iface.removeToolBarIcon(action)

        reactor.stop()

    def run(self):        
        #from twisted.web import static, twcgi
        #root = static.File("/var/www/")
        #root.putChild("cgi-bin", twcgi.CGIDirectory("/usr/lib/cgi-bin"))
        
        from twisted.web.resource import Resource
        
        class FormPage(Resource):
            def __init__(self, iface, pluginDir):
                self.iface = iface
                self.pluginDir = pluginDir
                
            def render_GET(self, request):
                return ''

            def render_POST(self, request):
                print request.__dict__
                newdata = request.content.getvalue()
                print newdata, type(newdata)
                QtGui.QMessageBox.information(self.iface.mainWindow(), "Qgis Cgi Server Plugin", u"recieved something.\n{}".format(newdata))
                self.iface.mapCanvas().setCanvasColor(QtGui.QColor(181, 208, 208))
                self.iface.mapCanvas().refresh()

                import os
                import simplejson as json
                newdata = json.loads(newdata)

                self.iface.addRasterLayer(os.path.join(self.pluginDir, 'datasets', 'osm_mapnik.xml'), 'OSM Mapnik')
                if newdata['bbox']:
                    self.iface.mapCanvas().setExtent(QgsRectangle(newdata['bbox']['xmin'], newdata['bbox']['ymin'], newdata['bbox']['xmax'], newdata['bbox']['ymax']))
                else:
                    self.iface.mapCanvas().zoomToFullExtent()
                #self.iface.mapCanvas().setExtent(QgsRectangle(1439918, 6866401, 1536152, 6929538))
                
                return ''

        root = Resource()
        root.putChild("form", FormPage(self.iface, self.plugin_dir))

        reactor.listenTCP(8080, server.Site(root))
        reactor.run()