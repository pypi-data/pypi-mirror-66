from nalej_platformer.utils import print_debug
from nalej_platformer.config import Configuration


def load_configuration(ctx):
    resources_path = ctx.obj['RESOURCES_PATH']
    config = Configuration.load_from_file(resources_path)

    config.find_missing_binaries()
    config.validate()

    ctx.obj['CONFIGURATION'] = config
