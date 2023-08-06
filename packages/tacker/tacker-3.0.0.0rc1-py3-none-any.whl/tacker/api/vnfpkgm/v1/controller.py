# Copyright (C) 2019 NTT DATA
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from io import BytesIO
from oslo_config import cfg
from oslo_log import log as logging
from oslo_utils import excutils
from oslo_utils import uuidutils
import six
from six.moves import http_client
from six.moves import urllib
import webob
import zipfile
from zipfile import ZipFile

from tacker._i18n import _
from tacker.api.schemas import vnf_packages
from tacker.api import validation
from tacker.api.views import vnf_packages as vnf_packages_view
from tacker.common import exceptions
from tacker.conductor.conductorrpc import vnf_pkgm_rpc
from tacker.glance_store import store as glance_store
from tacker.objects import fields
from tacker.objects import vnf_package as vnf_package_obj
from tacker.policies import vnf_package as vnf_package_policies
from tacker import wsgi

LOG = logging.getLogger(__name__)


CONF = cfg.CONF


class VnfPkgmController(wsgi.Controller):

    _view_builder_class = vnf_packages_view.ViewBuilder

    def __init__(self):
        super(VnfPkgmController, self).__init__()
        self.rpc_api = vnf_pkgm_rpc.VNFPackageRPCAPI()
        glance_store.initialize_glance_store()

    def _get_vnf_package(self, id, request):
        # check if id is of type uuid format
        if not uuidutils.is_uuid_like(id):
            msg = _("Can not find requested vnf package: %s") % id
            raise webob.exc.HTTPNotFound(explanation=msg)

        try:
            vnf_package = vnf_package_obj.VnfPackage.get_by_id(
                request.context, id)
        except exceptions.VnfPackageNotFound:
            msg = _("Can not find requested vnf package: %s") % id
            raise webob.exc.HTTPNotFound(explanation=msg)
        return vnf_package

    @wsgi.response(http_client.CREATED)
    @wsgi.expected_errors((http_client.BAD_REQUEST, http_client.FORBIDDEN))
    @validation.schema(vnf_packages.create)
    def create(self, request, body):
        context = request.environ['tacker.context']
        context.can(vnf_package_policies.VNFPKGM % 'create')

        vnf_package = vnf_package_obj.VnfPackage(context=request.context)
        vnf_package.onboarding_state = (
            fields.PackageOnboardingStateType.CREATED)
        vnf_package.operational_state = (
            fields.PackageOperationalStateType.DISABLED)
        vnf_package.usage_state = fields.PackageUsageStateType.NOT_IN_USE
        vnf_package.user_data = body.get('userDefinedData', dict())
        vnf_package.tenant_id = request.context.project_id

        vnf_package.create()

        return self._view_builder.create(request, vnf_package)

    @wsgi.response(http_client.OK)
    @wsgi.expected_errors((http_client.FORBIDDEN, http_client.NOT_FOUND))
    def show(self, request, id):
        context = request.environ['tacker.context']
        context.can(vnf_package_policies.VNFPKGM % 'show')

        # check if id is of type uuid format
        if not uuidutils.is_uuid_like(id):
            msg = _("Can not find requested vnf package: %s") % id
            raise webob.exc.HTTPNotFound(explanation=msg)

        try:
            vnf_package = vnf_package_obj.VnfPackage.get_by_id(
                request.context, id,
                expected_attrs=["vnf_deployment_flavours", "vnfd"])
        except exceptions.VnfPackageNotFound:
            msg = _("Can not find requested vnf package: %s") % id
            raise webob.exc.HTTPNotFound(explanation=msg)

        return self._view_builder.show(request, vnf_package)

    @wsgi.response(http_client.OK)
    @wsgi.expected_errors((http_client.BAD_REQUEST, http_client.FORBIDDEN))
    @validation.query_schema(vnf_packages.query_params_v1)
    def index(self, request):
        context = request.environ['tacker.context']
        context.can(vnf_package_policies.VNFPKGM % 'index')

        search_opts = {}
        search_opts.update(request.GET)

        def _key_exists(key, validate_value=True):
            try:
                request.GET[key]
            except KeyError:
                return False

            return True

        all_fields = _key_exists('all_fields')
        exclude_default = _key_exists('exclude_default')
        fields = request.GET.get('fields')
        exclude_fields = request.GET.get('exclude_fields')
        filters = request.GET.get('filter')
        if not (all_fields or fields or exclude_fields):
            exclude_default = True

        self._view_builder.validate_attribute_fields(all_fields=all_fields,
            fields=fields, exclude_fields=exclude_fields,
            exclude_default=exclude_default)

        filters = self._view_builder.validate_filter(filters)

        vnf_packages = vnf_package_obj.VnfPackagesList.get_by_filters(
            request.context, read_deleted='no', filters=filters)

        return self._view_builder.index(request, vnf_packages,
                all_fields=all_fields, exclude_fields=exclude_fields,
                fields=fields, exclude_default=exclude_default)

    @wsgi.response(http_client.NO_CONTENT)
    @wsgi.expected_errors((http_client.FORBIDDEN, http_client.NOT_FOUND,
                           http_client.CONFLICT))
    def delete(self, request, id):
        context = request.environ['tacker.context']
        context.can(vnf_package_policies.VNFPKGM % 'delete')

        vnf_package = self._get_vnf_package(id, request)

        if (vnf_package.operational_state ==
                fields.PackageOperationalStateType.ENABLED or
                vnf_package.usage_state ==
                fields.PackageUsageStateType.IN_USE):
            msg = _("VNF Package %(id)s cannot be deleted as it's "
                    "operational state is %(operational_state)s and usage "
                    "state is %(usage_state)s.")
            raise webob.exc.HTTPConflict(
                explanation=msg % {
                    "id": id,
                    "operational_state": vnf_package.operational_state,
                    "usage_state": vnf_package.usage_state})

        # Delete vnf_package
        self.rpc_api.delete_vnf_package(context, vnf_package)

    @wsgi.response(http_client.ACCEPTED)
    @wsgi.expected_errors((http_client.FORBIDDEN, http_client.NOT_FOUND,
                           http_client.CONFLICT))
    def upload_vnf_package_content(self, request, id, body):
        context = request.environ['tacker.context']
        context.can(vnf_package_policies.VNFPKGM % 'upload_package_content')

        vnf_package = self._get_vnf_package(id, request)

        if vnf_package.onboarding_state != \
           fields.PackageOnboardingStateType.CREATED:
            msg = _("VNF Package %(id)s onboarding state "
                    "is not %(onboarding)s")
            raise webob.exc.HTTPConflict(explanation=msg % {"id": id,
                    "onboarding": fields.PackageOnboardingStateType.CREATED})

        vnf_package.onboarding_state = (
            fields.PackageOnboardingStateType.UPLOADING)

        vnf_package.save()

        try:
            (location, size, checksum, multihash,
            loc_meta) = glance_store.store_csar(context, id, body)
        except exceptions.UploadFailedToGlanceStore:
            with excutils.save_and_reraise_exception():
                vnf_package.onboarding_state = (
                    fields.PackageOnboardingStateType.CREATED)
                vnf_package.save()

        vnf_package.onboarding_state = (
            fields.PackageOnboardingStateType.PROCESSING)

        vnf_package.algorithm = CONF.vnf_package.hashing_algorithm
        vnf_package.hash = multihash
        vnf_package.location_glance_store = location

        vnf_package.save()

        # process vnf_package
        self.rpc_api.upload_vnf_package_content(context, vnf_package)

    @wsgi.response(http_client.ACCEPTED)
    @wsgi.expected_errors((http_client.BAD_REQUEST, http_client.FORBIDDEN,
                           http_client.NOT_FOUND, http_client.CONFLICT))
    @validation.schema(vnf_packages.upload_from_uri)
    def upload_vnf_package_from_uri(self, request, id, body):

        context = request.environ['tacker.context']
        context.can(vnf_package_policies.VNFPKGM % 'upload_from_uri')

        vnf_package = self._get_vnf_package(id, request)

        url = body['addressInformation']
        try:
            data_iter = urllib.request.urlopen(url)
        except Exception:
            data_iter = None
            msg = _("Failed to open URL %s")
            raise webob.exc.HTTPBadRequest(explanation=msg % url)
        finally:
            if hasattr(data_iter, 'close'):
                data_iter.close()

        if vnf_package.onboarding_state != \
                fields.PackageOnboardingStateType.CREATED:
            msg = _("VNF Package %(id)s onboarding state is not "
                    "%(onboarding)s")
            raise webob.exc.HTTPConflict(explanation=msg % {"id": id,
                    "onboarding": fields.PackageOnboardingStateType.CREATED})

        vnf_package.onboarding_state = (
            fields.PackageOnboardingStateType.UPLOADING)

        vnf_package.save()

        # process vnf_package
        self.rpc_api.upload_vnf_package_from_uri(context, vnf_package,
                                            body['addressInformation'],
                                            user_name=body.get('userName'),
                                            password=body.get('password'))

    @wsgi.response(http_client.OK)
    @wsgi.expected_errors((http_client.BAD_REQUEST, http_client.FORBIDDEN,
                           http_client.NOT_FOUND, http_client.CONFLICT))
    @validation.schema(vnf_packages.patch)
    def patch(self, request, id, body):
        context = request.environ['tacker.context']
        context.can(vnf_package_policies.VNFPKGM % 'patch')

        old_vnf_package = self._get_vnf_package(id, request)
        vnf_package = old_vnf_package.obj_clone()

        user_data = body.get('userDefinedData')
        operational_state = body.get('operationalState')

        if operational_state:
            if vnf_package.onboarding_state == \
                    fields.PackageOnboardingStateType.ONBOARDED:
                if vnf_package.operational_state == operational_state:
                    msg = _("VNF Package %(id)s is already in "
                            "%(operationState)s operational state") % {
                        "id": id,
                        "operationState": vnf_package.operational_state}
                    raise webob.exc.HTTPConflict(explanation=msg)
                else:
                    # update vnf_package operational state,
                    # if vnf_package Onboarding State is ONBOARDED
                    vnf_package.operational_state = operational_state
            else:
                if not user_data:
                    msg = _("Updating operational state is not allowed for VNF"
                            " Package %(id)s when onboarding state is not "
                            "%(onboarded)s")
                    raise webob.exc.HTTPBadRequest(
                        explanation=msg % {"id": id, "onboarded": fields.
                            PackageOnboardingStateType.ONBOARDED})
        # update user data
        if user_data:
            for key, value in list(user_data.items()):
                if vnf_package.user_data.get(key) == value:
                    del user_data[key]

            if not user_data:
                msg = _("The userDefinedData provided in update request is as"
                        " the existing userDefinedData of vnf package %(id)s."
                        " Nothing to update.")
                raise webob.exc.HTTPConflict(
                    explanation=msg % {"id": id})
            vnf_package.user_data = user_data

        vnf_package.save()

        return self._view_builder.patch(old_vnf_package, vnf_package)

    @wsgi.response(http_client.OK)
    @wsgi.expected_errors((http_client.BAD_REQUEST, http_client.FORBIDDEN,
                           http_client.NOT_FOUND, http_client.NOT_ACCEPTABLE,
                           http_client.CONFLICT,
                           http_client.INTERNAL_SERVER_ERROR))
    def get_vnf_package_vnfd(self, request, id):
        context = request.environ['tacker.context']
        context.can(vnf_package_policies.VNFPKGM % 'get_vnf_package_vnfd')

        valid_accept_headers = ['application/zip', 'text/plain']
        accept_headers = request.headers['Accept'].split(',')
        for header in accept_headers:
            if header not in valid_accept_headers:
                msg = _("Accept header %(accept)s is invalid, it should be one"
                        " of these values: %(valid_values)s")
                raise webob.exc.HTTPNotAcceptable(
                    explanation=msg % {"accept": header,
                                       "valid_values": ",".join(
                                           valid_accept_headers)})

        vnf_package = self._get_vnf_package(id, request)

        if vnf_package.onboarding_state != \
                fields.PackageOnboardingStateType.ONBOARDED:
            msg = _("VNF Package %(id)s state is not "
                    "%(onboarded)s")
            raise webob.exc.HTTPConflict(explanation=msg % {"id": id,
                    "onboarded": fields.PackageOnboardingStateType.ONBOARDED})

        try:
            vnfd_files_and_data = self.rpc_api.\
                get_vnf_package_vnfd(context, vnf_package)
        except exceptions.FailedToGetVnfdData as e:
            LOG.error(e.msg)
            raise webob.exc.HTTPInternalServerError(
                explanation=six.text_type(e.msg))

        if 'text/plain' in accept_headers:
            # Checking for yaml files only. This is required when there is
            # TOSCA.meta file along with single yaml file.
            # In such case we need to return single yaml file.
            file_list = list(vnfd_files_and_data.keys())
            yaml_files = [file for file in file_list if file.endswith(
                ('.yaml', '.yml'))]
            if len(yaml_files) == 1:
                request.response.headers['Content-Type'] = 'text/plain'
                return vnfd_files_and_data[yaml_files[0]]
            elif 'application/zip' in accept_headers:
                request.response.headers['Content-Type'] = 'application/zip'
                return self._create_vnfd_zip(vnfd_files_and_data)
            else:
                msg = _("VNFD is implemented as multiple yaml files,"
                        " Accept header should be 'application/zip'.")
                raise webob.exc.HTTPBadRequest(explanation=msg)
        else:
            request.response.headers['Content-Type'] = 'application/zip'
            return self._create_vnfd_zip(vnfd_files_and_data)

    def _create_vnfd_zip(self, vnfd_files_and_data):
        buff = BytesIO()
        with ZipFile(buff, 'w', zipfile.ZIP_DEFLATED) as zip_archive:
            for file_path, file_data in vnfd_files_and_data.items():
                zip_archive.writestr(file_path, file_data)

        return buff.getvalue()


def create_resource():
    body_deserializers = {
        'application/zip': wsgi.ZipDeserializer()
    }

    deserializer = wsgi.RequestDeserializer(
        body_deserializers=body_deserializers)
    return wsgi.Resource(VnfPkgmController(), deserializer=deserializer)
