#!/usr/bin/env python

"""Utilities for verifying docker image integrity and signatures."""

# TODO: Revamp interfaces to conform with https://github.com/opencontainers/image-spec/blob/master/media-types.md

from .manifests import (
    ArchiveManifest,
    DeviceMapperRepositoryManifest,
    Manifest,
    RegistryV2Manifest,
)
from .signers import GPGSigner, PKISigner, Signer
from .imageconfig import ImageConfig, SignatureTypes
from .imagename import ImageName
from .imagesources import (
    ArchiveImageSource,
    DeviceMapperRepositoryImageSource,
    ImageSource,
    RegistryV2ImageSource,
)
from .utils import FormattedSHA256


__version__ = "1.0.0"
