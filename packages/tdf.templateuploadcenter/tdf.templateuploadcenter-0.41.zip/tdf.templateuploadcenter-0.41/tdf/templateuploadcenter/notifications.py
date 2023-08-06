# -*- coding: utf-8 -*-
from plone import api
from tdf.templateuploadcenter.tupcenter import ITUpCenter


def notifiyAboutNewVersion(tupproject, event):
    if hasattr(event, 'descriptions') and event.descriptions:
        for d in event.descriptions:
            if hasattr(d, 'interface') and d.interface is ITUpCenter and \
                    'available_versions' in d.attributes:
                catalog = api.portal.get_tool(name='portal_catalog')
                projectemail = catalog.uniqueValuesFor('tempprojectemail')
                message = 'We added a new version of LibreOffice to the ' \
                          'list.\n Please add this version to your ' \
                          'LibreOffice template release(s), if it is (they ' \
                          'are) compatible with this version.\n\n' \
                          'You could do this on your release(s). Go to the ' \
                          'release of your project and choose the command ' \
                          "'edit' from the menu bar. Go to the section " \
                          "'compatible with versions of LibreOffice' " \
                          'and mark the checkbox for the new version of ' \
                          'LibreOffice.\n\n' \
                          'Kind regards,\n\n' \
                          'The LibreOffice Extension and Template Site ' \
                          'Administration Team'
                for f in projectemail:
                    mailaddress = f
                    api.portal.send_email(
                        recipient=mailaddress,
                        sender="noreply@libreoffice.org",
                        subject="Templates Section: New Version of "
                                "LibreOffice Added",
                        body=message,
                    )
