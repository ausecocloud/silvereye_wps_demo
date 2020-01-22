import os
import os.path

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.response import FileResponse

from swiftclient.utils import generate_temp_url
from pywps import configuration as config

from silvereye_wps_demo.pywps.swiftstorage import get_temp_url_key


@view_config(route_name='outputs')
def outputs(request):
    # If Swift enabled, use that
    if config.get_config_value('server', 'storage') == 'SwiftStorage':
        # TODO: maybe use server:outputpath here?
        container = config.get_config_value('SwiftStorage', 'container')
        # TODO: TEMP_URL_KEY not needed in pywps
        temp_url_key = get_temp_url_key()

        path_prefix = '/v1/AUTH_{}/{}/'.format(os.environ['OS_PROJECT_ID'], container)
        temp_url = generate_temp_url(
            path=path_prefix + '/'.join(request.matchdict['filename']),
            seconds=60 * 60 * 24,  # temp url valid for 24hrs
            key=temp_url_key,
            method='GET',
            # prefix=True,
            # iso8601=True,
            # ip_range=???
        )
        return HTTPFound(location='https://swift.rc.nectar.org.au' + temp_url)

    # Default to just serving the file for FileStorage
    output_dir = config.get_config_value('server', 'outputpath') + "/"
    path = os.path.join(output_dir, '/'.join(request.matchdict['filename']))
    response = FileResponse(path, request)
    return response
