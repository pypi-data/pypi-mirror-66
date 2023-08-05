"""Defines additional contracts."""

from tablib import Dataset
from contracts import new_contract
from django.core.files.uploadedfile import InMemoryUploadedFile
from import_export.resources import Resource
from import_export.results import Result
from lib_import.resources import ImportModelResource


def makecontract(
        x,
        contract_type,
        msg=''
):
    if not isinstance(x, contract_type):
        raise ValueError(msg)


@new_contract
def InMemoryUploadedFileType(x):
    makecontract(
        x,
        InMemoryUploadedFile,
        "The element is not a InMemoryUploadedFile"
    )


@new_contract
def ResultType(x):
    makecontract(
        x,
        Result,
        "The element is not a Result"
    )


@new_contract
def DatasetType(x):
    makecontract(
        x,
        Dataset,
        "The element is not a Dataset"
    )


@new_contract
def ResourceType(x):
    makecontract(
        x,
        Resource,
        "The element is not a Resource"
    )


@new_contract
def ImportModelResourceSubclass(x):
    if not issubclass(x, ImportModelResource):
        msg = "resource_class must be a children of ImportModelResource"
        raise ValueError(msg)
