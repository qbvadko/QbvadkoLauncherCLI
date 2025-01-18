from lxml import etree
import requests

def get_json_data(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    
    return response.json()

def all_vanilla_versions() -> dict:
    '''Returns all vanilla versions that Mojang offers to download'''

    releases, snapshots, old_beta, old_alpha = [], [], [], []
    
    data = get_json_data('https://launchermeta.mojang.com/mc/game/version_manifest_v2.json')['versions']
    for version in data:
        if version['type'] == 'release':
            releases.append(version['id'])

        if version['type'] == 'snapshot':
            snapshots.append(version['id'])

        if version['type'] == 'old_beta':
            old_beta.append(version['id'])

        if version['type'] == 'old_alpha':
            old_alpha.append(version['id'])
    
    return {'releases': releases, 'snapshots': snapshots, 'old_beta': old_beta, 'old_alpha': old_alpha}

def forge_stable_mc_versions() -> list:
    FORGE_API_URL = 'https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml'
    response = requests.get(FORGE_API_URL)
    response.raise_for_status()

    root = etree.fromstring(response.content)

    versions = []
    for game in root.xpath('//version/text()'):
        version = game.split('-')[0]
        if version not in versions:
            versions.append(version)

    return versions

def fabric_stable_mc_versions() -> list:
    FABRIC_API_URL = 'https://meta.fabricmc.net/v2/versions/game'

    versions = []
    for game in get_json_data(FABRIC_API_URL):
        if game['stable']:
            versions.append(game['version'])
    
    return versions

def quilt_stable_mc_versions() -> list:
    QUILT_API_URL = 'https://meta.quiltmc.org/v3/versions/game'

    versions = []
    for game in get_json_data(QUILT_API_URL):
        if game['stable']:
            versions.append(game['version'])
    
    return versions
