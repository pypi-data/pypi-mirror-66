"""Configuration handler

The configuration is a simple dictionary. See :ref:`configuration` for
details.
"""


class Config(dict):
    """Configuration

    Example:
        .. code-block:: python

            from space.config import config

            print(config['env']['eop_missing_policy'])
            print(config.get('env', 'non-existent-field', fallback=25))

    """

    _instance = None

    def get(self, *keys, fallback=None):
        """Retrieve a value in the config, if the value is not available
        give the fallback value specified.
        """

        section, *keys = keys
        out = super().get(section, fallback)

        while isinstance(out, dict):
            key = keys.pop(0)
            out = out.get(key, fallback)

        return out

    def set(self, *args):
        """Set a value in the config dictionary

        The last argument is the value to set

        Example:

        .. code-block:: python

            config.set('aaa', 'bbb', True)
            print(config)
            # {
            #     'aaa': {
            #         'bbb': True
            #     }
            # }
        """

        # split arguments in keys and value
        *first_keys, last_key, value = args

        subdict = self
        for k in first_keys:
            subdict.setdefault(k, {})
            subdict = subdict[k]

        subdict[last_key] = value


config = Config()
