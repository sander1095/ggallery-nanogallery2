## Description

This repository contains a template and a script to generate an HTML photo gallery using [ggallery](https://github.com/creeston/ggallery) tool.

[![npm](https://img.shields.io/badge/demo-online-008000.svg)](https://creeston.github.io/ggallery-nanogallery2)

**This is a fork of [creeston/ggallery-nanogallery2](https://github.com/creeston/ggallery-nanogallery2)** with two added features (see below): a download button in the full-image viewer, and a download button on each thumbnail. Everything else is unchanged from upstream.

## Usage

In your `ggallery` configuration file, specify the template URL:

```yaml
template:
    url: https://github.com/creeston/ggallery-nanogallery2
    parameters:
        album_routing: true | false # If disabled, website will be rendered as Single Page Application, otherwise each album will have its own route
        viewer_download_button: true | false # Adds a download button to the full-image viewer, to the left of the close button. Default: false
        thumbnail_download_button: true | false # Adds a download button to every photo thumbnail (not album covers). Default: false
```

### Added features

- **`viewer_download_button`**: adds nanogallery2's built-in download button to the top-right of the full-image viewer toolbar, next to the close button.
- **`thumbnail_download_button`**: adds nanogallery2's built-in download icon to every photo thumbnail, so users can save an image without opening the full viewer at all — useful on mobile, where tapping a thumbnail doesn't open the viewer (`touchAutoOpenDelay: -1` in the nanogallery2 config).

Both use nanogallery2's own `downloadButton`/`DOWNLOAD` toolbar actions — no custom JS was added. Note: nanogallery2's download action is a plain `<a href=... download>` click, which browsers only honor as a forced download for same-origin URLs. If your photos are hosted on a different origin than the gallery page (e.g. served directly from Azure Blob Storage, as in the [ggallery](https://github.com/creeston/ggallery) Azure Blob example), clicking download will open the image in a new tab instead of saving it directly — the user can still save it from there. Forcing a true cross-origin download would require CORS on the storage origin plus fetch-as-blob JS, which this fork intentionally doesn't add (keeping the change minimal); the plain nanogallery2 behavior was chosen instead.


## References

Template uses the following technologies:

- **[nanogallery2](https://nanogallery2.nanostudio.org/)**
- **[bulma](https://bulma.io/)**
- **[FontAwesome](https://fontawesome.com/)**


## Development

### Prerequisites

```sh
python3 -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Tests

To run the tests, use the following command:

```sh
python -m unittest discover -p *_tests.py
```