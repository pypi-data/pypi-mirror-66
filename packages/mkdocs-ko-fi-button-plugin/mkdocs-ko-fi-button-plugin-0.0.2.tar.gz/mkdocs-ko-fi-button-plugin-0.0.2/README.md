# MkDocs Ko-fi Button Plugin

*An mkdocs plugin that let's you easily add a Ko-fi buttons with markdown*  
The plugin looks for jinja style tags like `{{ko-fi}}` and replaces it with a Ko-fi button. It is possible to configure the text and color of the button.

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

## Advanced config

In case the Ko-fi javascript is changed on the server side it is possible to configure the path and function calls. This will make it possible to still be able to get a working Ko-fi button widget until this plugin has been updated.

* `javascript_path` - The relative path to the javascript from https://ko-fi.com/. Default: "widgets/widget_2.js"
* `javascript_f1` - The init function. Default: "kofiwidget2.init"
* `javascript_f2` - The draw function. Default: "kofiwidget2.draw"

