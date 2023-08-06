# MkDocs Ko-fi Button Plugin

*An mkdocs plugin that let's you easily add a Ko-fi buttons with markdown*  
The plugin looks for jinja style tags like `{{ko-fi}}` and replaces it with the Ko-fi button. In addition to the already existing Ko-fi markdown support it's possible to configure the text and color.

## Setup

Install the plugin using pip:

``` bash
pip install mkdocs-ko-fi-button-plugin
```

Activate the plugin in `mkdocs.yml`:

``` bash
plugins:
    - search
    - ko-fi-button
```

## Config

* `text` - The text on the Ko-fi button. Default: "Support Me on Ko-fi".
* `color` - The color of the button in hex format. Default: #29abe0
* `id` - Your Ko-fi ID. Can be found on your Ko-fi profile. Mandatory configuration.

For example:

``` bash
plugins:
    - search
    - ko-fi-button:
        text: 'My cool text'
        color: '#547884'
        id: 'my_id'
```

