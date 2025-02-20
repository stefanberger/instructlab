# SPDX-License-Identifier: Apache-2.0

# Standard
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
    help="Path to the directory of the model to be signed.",
)
@click.option(
    "--sig_out",
    type=click.Path(),
    default=None,
    show_default=False,
    help="Path to save the Sigstore bundle file after signing.",
)
@click.option(
    "--use-ambient-credentials",
    is_flag=True,
    show_default=True,
    default=False,
    help="use ambient credentials (also known as Workload Identity)",
)
@click.option(
    "--identity-token",
    type=click.STRING,
    default=None,
    show_default=False,
    help="Optional identity token",
)
@utils.display_params
def sign(model_path, sig_out, use_ambient_credentials, identity_token):
    """Signs a model with Sigstore"""
    if sig_out is None:
        sig_out = join(model_path, "model.sig")

    try:
        signing.sign_model(
            model_path=Path(model_path),
            sig_out=Path(sig_out),
            use_ambient_credentials=use_ambient_credentials,
            identity_token=identity_token,
        )
    except Exception as e:
        click.secho(f"Could not sign model in {model_path}: {e}", fg="red")
        raise click.exceptions.Exit(1)
