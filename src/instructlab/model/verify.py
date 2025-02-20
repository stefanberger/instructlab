# SPDX-License-Identifier: Apache-2.0

# Standard
import sys
from os.path import dirname, join
from pathlib import Path

# Third Party
import click

# First Party
from instructlab import configuration as config
from instructlab import signing, utils


@click.command()
@click.option(
    "--model-path",
    type=click.Path(),
    default=dirname(config.DEFAULT_MODEL_PATH),
    show_default=True,
    help="Path to the directory where the signed model is located.",
)
@click.option(
    "--signature",
    type=click.Path(),
    default=None,
    show_default=False,
    help="Path to the signature. By default model.sig in the model path will be used.",
)
@click.option(
    "--identity",
    help="Certificate identity to verify against."
    "Typically an email provided by the OIDC identity provider."
    "Example: a model signed using a Github account under hello@instructlab.ai would use hello@instructlab.ai.",
)
@click.option(
    "--issuer",
    help="Certificate identity's issuing authority.",
    default="https://github.com/login/oauth",
    show_default=True,
)
@click.option(
    "--yes",
    is_flag=True,
    show_default=True,
    default=False,
    help="Answer all interactive questions with 'yes'",
)
@utils.display_params
def verify(model_path, signature, identity, issuer, yes):
    """Signs a model with Sigstore"""

    if signature is None:
        signature = join(model_path, "model.sig")

    try:
        if not identity or not issuer:
            identity, issuer = signing.get_oidc_params_from_sigfile(Path(signature))
            if not signing.confirm(f"Use identity '{identity}' and issuer '{issuer}' from {signature}? [y/N] ", yes):
                sys.exit(1)
        signing.verify_model(
            model_path=Path(model_path),
            signature_file=Path(signature),
            identity=identity,
            issuer=issuer,
        )
        print(f"✅ {model_path} passed verification")
    except Exception as e:
        click.secho(f"❌ {model_path} failed verification: {e}", fg="red")
        raise click.exceptions.Exit(1)
