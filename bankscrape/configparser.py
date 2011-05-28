from ConfigParser import SafeConfigParser

__all__ = ['get_items']

def get_items(options):
    config = SafeConfigParser()
    config.read(options.configfile)
    return dict(config.items(options.configsection))

