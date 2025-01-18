from pathlib import Path
import subprocess
import random
import uuid

import yaml
from simple_term_menu import TerminalMenu
from minecraft_launcher_lib import fabric, quilt
from minecraft_launcher_lib.command import get_minecraft_command

from utils import quilt_stable_mc_versions, fabric_stable_mc_versions

CONFIGS_DIR = 'configs'

def get_launcher_settings():
    with open(Path(CONFIGS_DIR, 'launcher_settings.yaml')) as file:
        launcher_settings = yaml.safe_load(file)

    return launcher_settings

def get_launch_options():
    with open(Path(CONFIGS_DIR, 'launch_options.yaml')) as file:
        launch_options = yaml.safe_load(file)

    return launch_options

def update_launch_options(data):
    with open(Path(CONFIGS_DIR, 'launch_options.yaml'), 'w') as file:
        yaml.dump(data, file, sort_keys=False)

GAME_DIR = get_launch_options()['game_dir']
VERSIONS_DIR = Path(GAME_DIR, 'versions')

def main():
    match input('---> '):
        case 'install':
            args = ['Fabric', 'Quilt']
            menu = TerminalMenu(args)

            selected = args[menu.show()]

            if selected == 'Fabric':
                versions = fabric_stable_mc_versions()

                menu = TerminalMenu(versions)

                selected_version = versions[menu.show()]

                if TerminalMenu(["Yes", "No"], title=f"[Install this version?][version: {selected_version}][loader: fabric]").show(): return  # noqa: E701
                
                fabric.install_fabric(selected_version, GAME_DIR, callback={'setStatus': lambda logs: print(logs)})

            if selected == 'Quilt':
                versions = quilt_stable_mc_versions()

                menu = TerminalMenu(versions)

                selected_version = versions[menu.show()]

                if TerminalMenu(["Yes", "No"], title=f"[Install this version?][version: {selected_version}][loader: quilt]").show(): return  # noqa: E701
                
                quilt.install_quilt(selected_version, GAME_DIR, callback={'setStatus': lambda logs: print(logs)})

        case 'launch':
            installed_versions = [directory.name for directory in VERSIONS_DIR.iterdir()]

            menu = TerminalMenu(installed_versions)

            selected_version = installed_versions[menu.show()]

            if TerminalMenu(["Launch", "Refuse"], title=f"[Launch this version?][{selected_version}]").show(): return  # noqa: E701

            launch_options = get_launch_options()

            if launch_options['username'] == '':
                launch_options['username'] = f'PLAYER {random.randrange(100, 1000)}'
                update_launch_options(launch_options)

            if launch_options['uuid'] == '':
                launch_options['uuid'] = str(uuid.uuid4())
                update_launch_options(launch_options)

            command = get_minecraft_command(selected_version, GAME_DIR, launch_options)
            subprocess.run(command)

        case 'versions':
            args = ['Show installed versions', 'Show fabric versions', 'Show quilt versions']
            menu = TerminalMenu(args)

            selected = args[menu.show()]

            if selected == 'Show installed versions':
                print([directory.name for directory in VERSIONS_DIR.iterdir()])

            if selected == 'Show fabric versions':
                print(fabric_stable_mc_versions())

            if selected == 'Show quilt versions':
                print(quilt_stable_mc_versions())

if __name__ == "__main__":
    while True: 
        print('[commands][install, launch, versions]')
        main()