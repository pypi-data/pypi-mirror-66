Changelog
=========

0.41 (2020-04-26)
-----------------

- Move strings from unicode to save_unicode [Andreas Mantke]
- Pep8 fixes [Andreas Mantke]
- Add missing definition for context in function
  getLatestRelease on tupproject module [Andreas Mantke]
- Update localization files [Andreas Mantke]


0.40 (2020-03-31)
-----------------

- Pep8 fixes [Andreas Mantke]
- Add new module for mail to a project owner [Andreas Mantke]
- Update localization files and German localization [Andreas Mantke]


0.39 (2020-02-07)
-----------------

- Fix typos in install.txt and wrong imports in tupsmallproject
  module [Andreas Mantke]
- Change to @implementer in the releasecustomurl module for Python-3
  compatibility [Andreas Mantke]
- Change the messagefactory entry for compatiblity to current Plone
  versions [Andreas Mantke]
- Update the mailtoauthor module for compatibility with current Plone
  versions and Python-3
- Update localization files.


0.38 (2020-02-01)
-----------------

- Update localization files [Andreas Mantke]


0.37 (2020-01-29)
-----------------

- Add information about messages to the small project owner and from
  small template projects and update documentation in HTML and
  PDF file format. [Andreas Mantke]
- Add further versions of LibreOffice to the Template Center [Andreas Mantke]


0.36 (2020-01-11)
-----------------

- Bind project publication workflow to small template
  projects too [Andreas Mantke]
- Move CHANGES.txt, README and LICENSE to the main directory [Andreas Mantke]
- Add new interface and browserlayer for installation and
  uninstall and add new profiles for uninstall to setup [Andreas Mantke]
- Fix missing pointer to an element of a list for file extension
  validation [Andreas Mantke]
- Move contributors list to the root folder [Andreas Mantke]
- Reorder edit form of the template center module and add
  a new register [Andreas Mantke]
- Small text fixes in release and linked release [Andreas Mantke]
- Add user documentation and create a HTML and a PDF version
  of it [Andreas Mantke]
- Update localization files and German localization [Andreas Mantke]
- Adapt the MANIFEST.in to the current structure of the add-on [Andreas Mantke]


0.35 (2019-09-19)
-----------------

- Fix a typo in the notifications module [Andreas Mantke]
- Improve quotation marks in the notification module [Andreas Mantke]
- Pep8 fixes [Andreas Mantke]
- Update localization files and German localization. [Andreas Mantke]


0.34 (2019-09-07)
-----------------

- Fix the name of the searched portal_catalog index in the
  notifications module [Andreas Mantke]


0.33 (2019-09-07)
-----------------

- Improve the message to the sender of the contact to author
  form. [Andreas Mantke]
- Send notifications about a new product version not to all users of
  the site, but only to the project contact addresses. [Andreas Mantke]
- Update localization files and German localization. [Andreas Mantke]

0.32 (2019-08-16)
-----------------

- Fix regular expressions for validation of file extensions [Andreas Mantke]


0.31 (2019-07-28)
-----------------

- Remove an old function from the smalltemplateproject module [Andreas Mantke]
- Use only the first value of the catalog search tuple for the pattern
  of the regular expressions. {Andreas Mantke]
- Remove default values of the fields for the allowed file extensions,
  because this didn't work with the validation functions [Andreas Mantke]
- Update localization template and translation into Germnan [Andreas Mantke]

0.30 (2019-07-20)
-----------------

- Fix the validator for linked release files and its message
  text [Andreas Mantke]
- Fix the IContextAwareDefaultFactory in the linked release
  module [Andreas Mantke]

0.29 (2019-07-19)
-----------------

- Fix constraints for some options to upload and link template files in
  the release and the linked release module [Andreas Mantke]


0.28 (2019-07-16)
-----------------

- Add a title to fields description and product_description of the
  tupcenter and remove their description entry [Andreas Mantke]
- Add fields to submit allowed image and template file extensions
  instead of formerly hard coded file extensions for both to give
  more flexibility to the site administrator [Andreas Mantke]
- Add new indexes to the portal_catalog to hold the values of
  allowed image and template file extensions [Andreas Mantke]
- Create a new validator for image file extensions inside the
  tupproject module and move the validation to this validator
  [Andreas Mantke]
- Create new validators for template file extensions inside the
  tuprelease and the tuplinkedrelease module and move the
  validation to this validator [Andreas Mantke]
- Add new fields to display the currently allowed image and
  template file extensions to the tupproject, the tuprelease and
  the tuplinkedrelease [Andreas Mantke]
- Add subscribers for the messaging functions of the
  tupsmallproject module to configure.zcml [Andreas Mantke]
- Remove old and unnecessary functions for the validation of
  image and template file extensions [Andreas Mantke]
- Update localization template and German translation file [Andreas Mantke]


0.27 (2019-06-13)
-----------------

- Project view for stable releases changed thus a release date is only
  shown, if there is a publishing date for a release within a
  project available. {Andreas Mantke]
- Update localization template and German translation file [Andreas Mantke]


0.26 (2019-05-28)
-----------------

- Change fallback email sender and recipient from hard coded to the variable
  site email address [Andreas Mantke]
- Remove redundant source code [Andreas Mantke]
- Update localization template and German localization [Andreas Mantke]


0.25 (2019-05-09)
-----------------

- Add a new email form to send feedback to a project author with recaptcha
  protection and link it from the project and the smallproject
  view [Andreas Mantke]
- Pep8 fixes [Andreas Mantke]
- Update localization template and German localization [Andreas Mantke]


0.24 (2019-04-16)
-----------------

- Structure the tupproject edit mode with register [Andreas Mantke]
- Update German localization [Andreas Mantke]
- Improve the edit dialog and split it into more register for the release and
  the linked release module. [Andreas Mantke]
- Change from plone.directives form to plone.autoform directives for
  the release and the linked release module [Andreas Mantke]
- Update German localization [Andreas Mantke]


0.23 (2019-03-30)
-----------------

- Add a new module for small templates projects [Andreas Mantke]
- New function to search and display categories for template
  projects and small template projects [Andreas Mantke]
- CSS fix [Andreas Mantke]
- Change listing of categories, licenses and compatility to a
  portal_catalog search [Andreas Mantke]
- Update German localization [Andreas Mantke]

0.22 (2018-12-16)
-----------------

- CSS fix [Andreas Mantke]
- PEP8 fixes [Andreas Mantke]
- Change over to supermodel.directives for primary fields and fieldsets [Andreas Mantke]
- Change from plone.directives form.mode to plone.autoform directives.mode [Andreas Mantke]

0.21 (2018-11-26)
-----------------

- Move the messaging about the creation of new projects to
  the tupprojects module [Andreas Mantke]
- Changed the email address for notifications about projects and (linked) releases
  from hard coded to variable and added a validation for the email address [Andreas Mantke]
- Improve the templates project workflow [Andreas Mantke]
- Update German localization [Andreas Mantke]


0.20 (2018-10-25)
-----------------

- Remove inline css style and add css styles for the table on
  project view into the css-layout file [Andreas Mantke]
- Added a new notify subscriber for modifications of
  projects to get an information about the content of
  the text fields. The content of the text fields will
  be forwarded by email. [Andreas Mantke]
- Add specific workflow permissions for private project
  objects.[Andreas Mantke]
- Update buildout.cfg to Plone 5.1 [Andreas Mantke]


0.19 (2018-09-03)
-----------------

- Add a function for search and display the compatibility from the indexes of
  the portal_catalog [Andreas Mantke]
- Add an optional field to give users an information how to search for older
  versions, if they are removed from the compatibility list in the tupcenter.py
  [Andreas Mantke]
- Update localization template and localization into German. [Andreas Mantke]


0.18 (2018-08-12)
-----------------

- Added a workflow for template projects [Andreas Mantke]
- Update of the localization to German. [Andreas Mantke]
- Marked some message strings as utf-8. [Andreas Mantke]


0.17 (2018-07-21)
-----------------

- Added download links for unstable release files to the project view, which
  are displayed, if there is no stable release [Andreas Mantke]
- Add an information about the current status to the message for
  the project manager, send for changing the workflow state. [Andreas Mantke]
- Fixed a few localization issues in the views of tuprelease and
  tupreleaselink and updated localization template file and
  localization into German. [Andreas Mantke}



0.16 (2018-06-27)
-----------------

- Adding a function to collect the latest unstable release and a slot in
  the project view to present such releases to the user [Andreas Mantke]
- Updated string format handling to modern method in tupcenter.py
  and tupproject.py [Andreas Mantke]
- Add a function for search and display the license from the indexes of
  the portal_catalog [Andreas Mantke]
- Update of the German localization [Andreas Mantke]


0.15 (2018-02-03)
-----------------

- Heading for release details and changelog will be hidden in the view
  tupreleases and tupreleaselink view, if there is no content for this
  topics [Andreas Mantke]
- Add a further explanation for publishing a release and linked release
  and a link to the advanced state change. [Andreas Mantke]
- Update versions of LibreOffice [Andreas Mantke]
- Update of the internationalization template and the po-file and localilization for the
  German language [Andreas Mantke]


0.14 (2018-01-07)
-----------------

- Fixed a Tal-expression in the views of release and linked release [Andreas Mantke].


0.13 (2017-09-19)
-----------------

- Notification about a new entry in the review list added [Andreas Mantke].


0.12 (2017-04-12)
-----------------

- Screenshot displayed on mouse click in scale large on project page [Andreas Mantke]
- Fix for display projects of current user [Andreas Mantke]
- Improve the messaging for new projects according to the review status
  and remove  not necessary i18-domain declarations [Andreas Mantke]
- Update of localisation template and German localisation [Andreas Mantke]



0.11 (2017-03-03)
-----------------

- Fix of the header of the German localization file. [Andreas Mantke]
- Fix field related issues [Victor Fernandez de Alba]
- Fix views and project_logo conditions [Victor Fernandez de Alba]
- Fix templates responsive classes and use the Bootstrap ones [Victor Fernandez de Alba]
- Fix optional fields for additional file fields marked as required [Victor Fernandez de Alba]
- Add categorization behavior to the custom contenttypes [Victor Fernandez de Alba]
- Unify the license list [Victor Fernandez de Alba]
- Fix search issues in templates [Victor Fernandez de Alba]
- Fix rough edges in some use cases [Victor Fernandez de Alba]
- Transfer code to proper class method to fix unicode errors on template [Victor Fernandez de Alba]
- Add support for querying the release compatibility versions of inner releases from projects [Victor Fernandez de Alba]
- Set the max length of a release name/numbering to twelf [Andreas Mantke]
- Spellcheck fix in own_projects.pt [Andreas Mantke]
- Add an index for the project contact address to the portal catalog [Andreas Mantke]
- Add missing file links to the view template of the releases and add the file name to the download link
  [Andreas Mantke]
- Add missing file links to the view of the project view for current releases [Andreas Mantke]
- Add a missing string and missing space to the template center view [Andreas Mantke]
- Fix catalog search to the Title index in case of special () characters [Victor Fernandez de Alba]
- Improvement for the error messages and instructions on tupprojects [Andreas Mantke]
- Improved error message for source code question on tupreleases and linked tupreleases [Andreas Mantke]
- Added a description to the install instructions field and removed the default value (text) [Andreas Mantke]
- Add guard in case that a malformed query was entered, return empty record [Victor Fernandez de Alba]
- Update of the localisation template and the German localisation [Andreas Mantke]

0.10 (2016-09-07)
-----------------

- Add German localization [Andreas Mantke]
- Update of the localisation template file [Anddreas Mantke]
- Fixing and adding localisation tags [Andreas Mantke]
- Fix ressource registry css URL [Victor Fernandez de Alba]


0.9 (2016-08-21)
----------------

- Adding file extension validation to the linked release module [Andreas Mantke]
- Adding image file extension validation to the project module [Andreas Mantke]
- Added a validator for the uniqueness of the naming of release and linked release [Andreas Mantke]
- Changed the compatibility list in the project view to a text line [Andreas Mantke].


0.8 (2016-07-11)
----------------

- CSS-Style fixes
- Markup style fix [Andreas Mantke]
- PEP-8-Fixes [Andreas Mantke]


0.7 (2016-05-27)
----------------

- Added a validator for the uniqueness of the release and linked release naming and
  and the corresponding adapter [Andreas Mantke]
- Changed the compatibility list in the project view to a text line [Andreas Mantke]


0.6 (2016-05-20)
----------------

- Smaller fixes on the project view the project view template:
  removed an obsolete div tag and made logo and project description heading
  conditional, changed the heading for the current release down the hierarchy
  [Andreas Mantke]
- Fix in the project view for the link to css file [Andreas Mantke]


0.5 (2016-05-14)
----------------

- Added a css style for release install instructions [Andreas Mantke]
- Fix for getting the title of the project [Andreas Mantke]
- Removed the column one from project and (linked) release views [Andreas Mantke]


0.4 (2016-04-05)
----------------

- Fixed the screenshot definition in the tupcenter-view [Andreas Mantke]
- Added a missing comma in a listing of tupcenter.py [Andreas Mantke]
- Changed in setup.py from History.txt to CHANGES.txt [Andreas Mantke]
- Update of the internationalisation template file [Andreas Mantke]
- Removed obsolet History.txt [Andreas Mantke]


0.3 (2016-03-12)
----------------

- Fixed an import in tupcenter.py [Andreas Mantke]


0.2 (2016-03-11)
----------------

- Nothing changed yet.


0.1 (2016-03-11)
----------------

- Package created using templer
  [Andreas Mantke]