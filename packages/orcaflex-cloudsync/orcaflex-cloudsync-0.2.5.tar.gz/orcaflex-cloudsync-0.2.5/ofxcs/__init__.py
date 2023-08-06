import os
import pprint
import shutil
import sys
import webbrowser
from os import getcwd
from pathlib import Path
from time import sleep

import click
from cryptography.fernet import Fernet

from ofxcloudsync import dirs, load_sync_ofx, write_sync_ofx
from ofxcloudsync.ofx_sync import run_local_sync


@click.group(chain=True)
@click.version_option()
@click.pass_context
def ofxcs(ctx):
    """Command line interface to orcaflex-cloudsync."""
    ctx.ensure_object(dict)
    sys.path.append(getcwd())


@ofxcs.command("configure")
@click.pass_context
def configure(ctx):
    """
    configures orcaflex-cloudsync
    """

    aws_cred = os.path.join(os.path.expanduser("~"), '.aws', 'credentials')
    current_config = load_sync_ofx()
    if not os.path.exists(aws_cred):
        if click.confirm('Do you want to enter access key details?'):
            key_id = click.prompt("Enter key ID", type=str)
            secret_key = click.prompt("Enter secret key", type=str)
            region = click.prompt("Enter region code", type=str)
            with open(aws_cred, 'w') as wf:
                s = f"""[default]
aws_access_key_id = {key_id}
aws_secret_access_key = {secret_key}
region = {region}"""
                wf.write(s)

        elif click.confirm('Do you want to enter request some access key details?'):
            webbrowser.open("mailto:ofxcs@agiledat.co.uk?subject=Request for ofx-cloudsync keys&body="
                         "Hi. I'd like to be able to use this cool OrcaFlex cloud sync tool.")
    bucket = click.prompt("Enter bucket name", type=str)
    try:
        os.mkdir(dirs.user_data_dir)
    except:
        pass
    pca_new = click.prompt('Where do you want to install the post-calculation action script?',
                           default=os.path.join(dirs.user_data_dir, "pca_ofx2cloud.py"))
    pca = Path(__file__).parent.parent.joinpath("ofxcloudsync", "pca_ofx2cloud.py")
    shutil.copy(pca, pca_new)
    if current_config is None:
        root_default = os.path.join(dirs.user_data_dir, "ofxsync")
    else:
        root_default = current_config['root_folder']
    root_folder = click.prompt('Where do you want to save the simulations?',
                               default=root_default)

    if (not current_config.get("key_file")) and click.confirm("Do you have a key file?"):
        key_path = click.prompt("Enter full path to key file")
    elif not current_config.get("key_file"):
        if click.confirm("Do you want to generate a key file (required to encrypt sim files)?"):
            key_path = get_keygen()
        else:
            key_path = None
    else:
        key_path = None
    sync_ofx = {
        "bucket": bucket,
        "root_folder": root_folder,
        "sync": []
    }
    if key_path:
        sync_ofx['key_file'] = key_path
    write_sync_ofx(sync_ofx)


@ofxcs.command("add")
@click.pass_context
@click.option("--folder",
              '-f',
              help="Add a folder to keep in sync.",
              type=str
              )
def add(ctx, folder):
    """add a folder to sync"""
    sync_ofx = load_sync_ofx()
    sync_ofx['sync'].append(folder)
    write_sync_ofx(sync_ofx)


@ofxcs.command("remove")
@click.pass_context
@click.option("--folder",
              '-f',
              help="Folder to stop syncing.",
              type=str
              )
@click.option("--delete",
              help="The folder will be deleted on the local drive.",
              default=False,
              is_flag=True
              )
def remove(ctx, folder, delete):
    """stop syncing a folder"""
    sync_ofx = load_sync_ofx()
    sync_ofx['sync'].remove(folder)
    write_sync_ofx(sync_ofx)
    if delete:
        folder_path = os.path.join(sync_ofx['root_folder'], folder)
        shutil.rmtree(folder_path)


@ofxcs.command("sync")
@click.pass_context
@click.option("--once",
              help="The sync will run once and exit. The default is for the sync to keep running until the user exits.",
              default=False,
              is_flag=True
              )
def sync(ctx, once):
    """sync files from cloud to local drive"""
    click.echo("Starting sync.")
    if once:
        run_local_sync()
        click.echo("Sync complete.")
    else:
        while True:
            try:
                run_local_sync()
                sleep(2)
            except KeyboardInterrupt:
                click.echo("exiting. Bye.")
                sys.exit(1)


def get_keygen():
    key_dir = click.prompt("Where do you want to save the key file?", default=dirs.user_data_dir)
    k = Fernet.generate_key()
    key_path = os.path.join(key_dir, "ofxcs.key")
    with open(key_path, 'wb') as wk:
        wk.write(k)
    if click.confirm("Do you want to update your config?"):
        config = load_sync_ofx()
        config['key_file'] = key_path
        write_sync_ofx(config)

@ofxcs.command("keygen")
def keygen():
    """generates a keyfile used to encrypt simulation data"""
    get_keygen()

@ofxcs.command("show")
def show():
    """shows the current config"""
    config = load_sync_ofx()
    click.echo(pprint.pformat(config))

