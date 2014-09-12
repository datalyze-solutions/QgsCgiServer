# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QgisCgiServer
                                 A QGIS plugin
 Provides a simple cgi server integrated into qgis, so you can call internal functions from web.
                             -------------------
        begin                : 2014-09-12
        copyright            : (C) 2014 by Matthias Ludwig - Datalyze Solutions
        email                : m.ludwig@datalyze-solutions.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load QgisCgiServer class from file QgisCgiServer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .QgisCgiServer import QgisCgiServer
    return QgisCgiServer(iface)
