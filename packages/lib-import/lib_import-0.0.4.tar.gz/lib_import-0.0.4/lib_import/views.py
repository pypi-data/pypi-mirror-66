
import logging
from tablib import Dataset

from contracts import contract
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView
from import_export.results import Result

from lib_import.exceptions import ImportError
from lib_import.contracts import (
    InMemoryUploadedFileType,
    ResultType,
    DatasetType,
    ResourceType,
    ImportModelResourceSubclass,
)

logger = logging.getLogger(__name__)


class ImportMixin:

    @contract(
        request=HttpRequest,
        resource_class='ImportModelResourceSubclass',
        skip_update=bool,
        filename='str[<256]|None',
        returns='tuple(ResultType,str|None)',
    )
    def import_file(
            self,
            request,
            resource_class,
            skip_update,
            filename=None
    ):
        """Imports data from file into database."""

        input_file = self.get_file(request, filename)
        dataset, error_msg = self.file_to_dataset(input_file)
        logger.debug('dataset %s', dataset)
        if dataset is None:
            result = Result()
        else:
            resource = self.initialize_resource(
                resource_class,
                skip_update
            )
            result = self.dataset_to_database(
                resource,
                dataset
            )

        return result, error_msg

    @contract(
        request=HttpRequest,
        filename='str[<256]|None',
        returns='InMemoryUploadedFileType'
    )
    def get_file(self, request, filename):
        """Extracts file from request."""
        if filename is None:
            # If filename is not defined, gets it
            filename = self.get_filename(request)

        # If file with name filename is present in request files, gets file
        # Otherwise, raises an error
        if filename in request.FILES:
            input_file = request.FILES[filename]
        else:
            logger.error(
                'Filename %s in not in request.FILES %s',
                filename,
                request.FILES,
            )
            raise ImportError
        logger.debug(
            "INPUT FILE \n file %s \n field_name %s \n name %s \n content_type %s \n size %s \n charset %s \n",
            input_file.file,
            input_file.field_name,
            input_file.name,
            input_file.content_type,
            input_file.size,
            input_file.charset,
        )
        return input_file

    @contract(
        request=HttpRequest,
        returns='str[<256]',
    )
    def get_filename(self, request):
        n_files = len(request.FILES)
        if n_files == 0:
            logger.error(
                'No file in request'
            )
            raise ImportError
        elif n_files == 1:
            filename = [elm for elm in request.FILES][0]
            return filename
        else:
            logger.error(
                'Several files are present in the request. A filename must be'
                'provided'
            )
            raise ImportError

    @contract(
        input_file='InMemoryUploadedFileType',
        returns='tuple(DatasetType|None,str|None)'
    )
    def file_to_dataset(self, input_file):
        """Extracts data from file into a dataset."""
        file_encoding = self.file_encoding()
        file_format = self.file_format()
        try:
            decoded_file = input_file.read().decode(file_encoding)
            logger.debug(
                'file %s field_name %s name %s content_type %s size %s charset %s',
                input_file.file,
                input_file.field_name,
                input_file.name,
                input_file.content_type,
                input_file.size,
                input_file.charset,
            )
        except UnicodeDecodeError:
            logger.warning(
                'UnicodeDecodeError %s %s',
                file_format,
                input_file,
            )
            dataset = None
            error_msg = _('msg_error_UnicodeDecodeError')
        else:
            dataset = Dataset().load(
                decoded_file,
                format=file_format,
            )
            error_msg = None

        return dataset, error_msg

    @contract(returns='str[<100]')
    def file_encoding(self):
        """Gets file encoding."""

        return 'utf-8'

    @contract(returns='str[<100]')
    def file_format(self):
        """Gets file format."""

        return 'csv'

    @contract(
        resource_class='ImportModelResourceSubclass',
        skip_update=bool,
        returns='ResourceType',
    )
    def initialize_resource(
        self,
        resource_class,
        skip_update
    ):
        # TODO case resource without init
        resource = resource_class(skip_update)

        return resource

    @contract(
        resource='ResourceType',
        dataset=Dataset,
        returns=Result
    )
    def dataset_to_database(self, resource, dataset):
        """Saves data from dataset into database."""

        result = resource.import_data(
            dataset,
            dry_run=False,
        )
        # TODO : maybe put in a transaction

        return result

    @contract(
        result=Result,
        error_msg='str|None',
        context=dict,
        returns=dict,
    )
    def adapt_context(self, result, error_msg, context={}):
        context = self.rows_infos_to_context(
            result,
            context=context
        )
        context['error_msg'] = error_msg

        return context

    @contract(
        result=Result,
        context=dict,
        returns=dict,
    )
    def rows_infos_to_context(self, result, context={}):
        context['new_rows'] = result.totals['new']
        context['update_rows'] = result.totals['update']
        context['delete_rows'] = result.totals['delete']
        context['skip_rows'] = result.totals['skip']
        context['error_rows'] = result.totals['error']
        context['invalid_rows'] = result.totals['invalid']
        logger.debug('context %s', context)

        return context


class ImportView(
        FormView,
        ImportMixin
):

    resource_class = None
    filename = None
    template_name = None
    form_class = None

    def post(self, request, *args, **kwargs):
        """Imports file data to database."""
        skip_update = self.set_skip_update(request)
        logger.debug('skip_update %s', skip_update)
        result, error_msg = self.import_file(
            request=request,
            resource_class=self.resource_class,
            skip_update=skip_update,
        )
        self.context = self.adapt_context(result, error_msg)
        self.context['form'] = self.form_class()
        self.request = request
        return super().post(self, request, *args, **kwargs)

    def form_valid(self, form):
        return render(
            self.request,
            self.template_name,
            context=self.context,
        )

    @contract(
        request=HttpRequest,
        returns=bool,
    )
    def set_skip_update(self, request):
        import_type = request.POST.get('import_type')
        if import_type == 'create_only':
            skip_update = True
        else:
            skip_update = False

        return skip_update
