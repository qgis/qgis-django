"""
Plugin validator class

"""
import zipfile
import mimetypes
import re
import os
import ConfigParser

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

PLUGIN_MAX_UPLOAD_SIZE= getattr(settings, 'PLUGIN_MAX_UPLOAD_SIZE', 1048576)
PLUGIN_REQUIRED_METADATA=  getattr(settings, 'PLUGIN_REQUIRED_METADATA', ('name', 'description', 'version', 'qgisMinimumVersion'))

def validator(package):
    """
    Analyzes a zipped file, returns metadata if success, False otherwise.
    If the new icon metadata is found, an inmemory file object is also returned

    Current checks:

        * size <= PLUGIN_MAX_UPLOAD_SIZE
        * zip contains __init__.py in first level dir
        * mandatory metadata: ('name', 'description', 'version', 'qgisMinimumVersion')
        * package_name regexp: [A-Za-z][A-Za-z0-9-_]+

    """

    if package.size > PLUGIN_MAX_UPLOAD_SIZE:
        raise ValidationError( _("File is too big. Max size is %s Bytes") % PLUGIN_MAX_UPLOAD_SIZE )

    if False and package.content_type != 'application/zip':
        raise forms.ValidationError( msg )
    else:
        try:
            zip = zipfile.ZipFile( package )
        except:
            raise ValidationError( _("Could not unzip file.") )
        for zname in zip.namelist():
            if zname.find('..') != -1 or zname.find(os.path.sep) == 0 :
                raise ValidationError( _("For security reasons, zip file cannot contain path informations") )
        bad_file = zip.testzip()
        if bad_file:
            zip.close()
            del zip
            raise ValidationError( msg )

        # Checks that package_name/__init__.py exists
        namelist = zip.namelist()
        try:
            package_name = namelist[0][:namelist[0].index('/')]
        except:
            raise ValidationError( _("Cannot find a folder inside the compressed package: this does not seems a valid plugin") )

        # Cuts the trailing slash
        if package_name.endswith('/'):
            package_name = package_name[:-1]
        initname = package_name + '/__init__.py'
        metadataname = package_name + '/metadata.txt'
        if not initname in namelist and not metadataname in namelist:
            raise ValidationError(_('Cannot find __init__.py or metadata.txt in the compressed package: this does not seems a valid plugin (I searched for %s and )') % (initname, metadataname))

        # Checks metadata

        # First parse metadata.ini
        if metadataname in namelist:
            try:
                parser = ConfigParser.ConfigParser()
                parser.optionxform = str
                parser.readfp(zip.open(metadataname))
                metadata = parser.items('general')
            except ConfigParser.NoSectionError:
                raise ValidationError(_("Cannot find a section named 'general' in %s") % metadataname)
            metadata.append(('metadata_source', 'metadata.txt'))
        else:
            # Then parse __init__
            # Ugly RE: regexp guru wanted!
            initcontent = zip.read(initname)
            metadata = re.findall('def\s+([^c]\w+).*?return\s+["\'](.*?)["\']', initcontent , re.DOTALL)
            if not metadata:
                raise ValidationError(_('Cannot find valid metadata in %s') % initname)
            metadata.append(('metadata_source', '__init__.py'))

        for md in PLUGIN_REQUIRED_METADATA:
            if not md in dict(metadata) or not dict(metadata)[md]:
                raise ValidationError(_('Cannot find metadata %s') % md)

        # Process Icon
        try:
            # Strip leading dir for ccrook plugins
            if dict(metadata)['icon'].startswith('./'):
                icon_path = dict(metadata)['icon'][2:]
            else:
                icon_path = dict(metadata)['icon']
            icon = zip.read(package_name + '/' + icon_path)
            icon_file = SimpleUploadedFile(dict(metadata)['icon'], icon, mimetypes.guess_type(dict(metadata)['icon']))
        except:
            icon_file = None

        metadata.append(('icon_file', icon_file))

        zip.close()
        del zip
        # Adds package_name
        if not re.match(r'^[A-Za-z][A-Za-z0-9-_]+$', package_name):
            raise ValidationError(_("Package name must start with an ASCII letter and can contain ASCII letters, digits and the signs '-' and '_'."))
        metadata.append(('package_name', package_name))
    return metadata

