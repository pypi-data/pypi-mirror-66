import sys
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class KofiButtonPlugin(BasePlugin):

    config_scheme = (
            ('color', config_options.Type(str, default='#29abe0')),
            ('text', config_options.Type(str, default='Support Me on Ko-fi')),
            ('id', config_options.Type(str)) # perhaps default=''
    )

    def on_page_markdown(self, markdown, **kwargs):
        # Check for the mandatory id config
        if not self.config['id']:
            sys.exit("Missing mandatory 'id' config for ko-fi-button plugin.")

        # Check the hex
        if not '#' in self.config['color']:
            self.config['color'] = "#" + self.config['color']

        # Look for the Ko-fi markdown {{ko-fi}}
        
        markdown = markdown.replace("{{ko-fi}}", "<script type='text/javascript' src='https://ko-fi.com/widgets/widget_2.js'></script><script type='text/javascript'>kofiwidget2.init('{}', '{}', '{}');kofiwidget2.draw();</script>".format(self.config['text'], self.config['color'], self.config['id']))

        return markdown

