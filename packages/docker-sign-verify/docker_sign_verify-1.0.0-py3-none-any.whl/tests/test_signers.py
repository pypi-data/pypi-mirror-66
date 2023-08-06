#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""Signer tests."""

import os
import tempfile
import shutil

from pathlib import Path

import pytest

from docker_sign_verify import GPGSigner, PKISigner


@pytest.fixture()
def gpgsigner(request):
    """Provides a GPGSinger instance."""
    homedir = Path(tempfile.mkdtemp())

    def _remove_homedir():
        shutil.rmtree(homedir)

    request.addfinalizer(_remove_homedir)
    signer = GPGSigner(None, "testing", homedir)
    # pylint: disable=protected-access
    signer._debug_init_store()

    return signer


@pytest.fixture()
def pkisigner(request):
    """Provides a PKISigner instance."""
    keypair = tempfile.mkstemp()[1]

    def _remove_keypair():
        os.remove(keypair)

    request.addfinalizer(_remove_keypair)
    signer = PKISigner(keypair, "testing")
    # pylint: disable=protected-access
    signer._debug_init_keypair()
    return signer


# def test_gpgsigner(caplog, gpgsigner: GPGSigner):
@pytest.mark.skip(
    reason="Fails on systems with GPG2 without loopback agent configured: https://github.com/isislovecruft/python-gnupg/issues/257"
)
def test_gpgsigner(gpgsigner: GPGSigner):
    """Test configuration signing and verification using GPG."""

    # TODO: Figure out why this isn't working ...
    # caplog.set_level(logging.FATAL, logger="gnupg")

    data = b"TEST DATA"

    # Generate a signature for the test data ...
    signature = gpgsigner.sign(data)
    assert "PGP SIGNATURE" in signature

    # Verify the generated signature against the test data ...
    result = gpgsigner.verify(data, signature)
    assert result.valid
    assert gpgsigner.keyid == result.key_id
    assert result.status == "signature valid"


def test_pkisigner(pkisigner: PKISigner):
    """Test configuration signing and verification using PKI."""

    data = b"TEST DATA"

    # Generate a signature for the test data ...
    signature = pkisigner.sign(data)
    assert "PKI SIGNATURE" in signature

    # Verify the generated signature against the test data ...
    result = pkisigner.verify(data, signature)
    assert result["valid"]
    assert result["keypair_path"] == pkisigner.keypair_path
    assert result["type"] == "pki"
