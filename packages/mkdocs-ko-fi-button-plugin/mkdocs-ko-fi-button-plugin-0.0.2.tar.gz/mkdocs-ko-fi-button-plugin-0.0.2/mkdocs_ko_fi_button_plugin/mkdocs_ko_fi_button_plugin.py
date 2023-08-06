import sys
import string
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class KofiButtonPlugin(BasePlugin):

    config_scheme = (
            ('color', config_options.Type(str, default='#29abe0')),
            ('text', config_options.Type(str, default='Support Me on Ko-fi')),
            ('id', config_options.Type(str)),
            ('javascript_path', config_options.Type(str, default='widgets/widget_2.js')),
            ('javascript_f1', config_options.Type(str, default='kofiwidget2.init')),
            ('javascript_f2', config_options.Type(str, default='kofiwidget2.draw'))
    )

    def on_page_markdown(self, markdown, **kwargs):
        plugin_name = "ko-fi-button"
        hex_length = 6

        for config in ['color', 'text', 'id', 'javascript_path', 'javascript_f1', 'javascript_f2']:
            # Check for non-existing config values.
            if not self.config[config]:
                sys.exit("Config '{}' is missing for {} plugin.".format(config, plugin_name))
            else:
                # Strip whitespace from all config values
                self.config[config] = self.config[config].strip()

                # Check for empty config values
                if self.config[config] == '':
                    sys.exit("The value of config '{}' is empty for {} plugin.".format(config, plugin_name))

        # Temporarily remove the '#' from the color hex
        self.config['color'] = self.config['color'].replace('#', '')

        # Check the lenght of the color value
        if len(self.config['color']) != hex_length:
            sys.exit("Incorrect length of config 'color' for {} plugin.".format(plugin_name))

        # Check if the color value is hexadecimal
        if not all(c in string.hexdigits for c in self.config['color']):
            sys.exit("Config 'color' is not a hexadecimal value for {} plugin.".format(plugin_name))

        # Prepend the color hex with '#'
        self.config['color'] = "#" + self.config['color']

        # Look for the Ko-fi markdown {{ko-fi}} and replace it
        markdown = markdown.replace("{{ko-fi}}", "<script type='text/javascript' src='https://ko-fi.com/{}'></script><script type='text/javascript'>{}('{}', '{}', '{}');{}();</script>".format(self.config['javascript_path'], self.config['javascript_f1'], self.config['text'], self.config['color'], self.config['id'], self.config['javascript_f2']))

        return markdown

