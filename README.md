## Description

This repository contains a template and a script to generate an HTML photo gallery using [ggallery](https://github.com/creeston/ggallery) tool.

[![npm](https://img.shields.io/badge/demo-online-008000.svg)](https://creeston.github.io/ggallery-nanogallery2)

**This is a fork of [creeston/ggallery-nanogallery2](https://github.com/creeston/ggallery-nanogallery2)** with two groups of added features (see below): download buttons, and control over the order photos appear in. Every added parameter defaults to off, so with no `parameters` set this template renders exactly like upstream.

## Usage

In your `ggallery` configuration file, specify the template URL:

```yaml
template:
    url: https://github.com/sander1095/ggallery-nanogallery2
    parameters:
        album_routing: true | false # If disabled, website will be rendered as Single Page Application, otherwise each album will have its own route
        viewer_download_button: true | false # Adds a download button to the full-image viewer, to the left of the close button. Default: false
        thumbnail_download_button: true | false # Adds a download button to every photo thumbnail (not album covers). Default: false
        photo_sorting: filename | source # `filename` sorts each album's photos by filename, `source` keeps data source order. Default: source
        order_switcher: true | false # Adds a dropdown next to the theme toggle for switching between the rendered order and a random one. Default: false
        order_switcher_labels: # Optional labels for that dropdown. Defaults: "Date" and "Random"
            date: "Op datum"
            random: "Willekeurig"
```

### Download buttons

Both download options use nanogallery2's own `downloadButton`/`DOWNLOAD` toolbar actions — no custom JS was added. Verified (via Playwright, against photos hosted on a different origin — Azure Blob Storage — than the gallery page itself) that this forces a real browser download rather than just opening the image in a new tab, so no CORS configuration or custom fetch-as-blob JS is needed on the storage side.

### Photo order

`ggallery` hands the template whatever order its data source produced. For the local data source that is a bare `os.listdir()`, whose order Python documents as arbitrary — NTFS happens to return entries sorted, ext4 returns them in hash order. So the same photos can render in a completely different order depending on which machine ran the build.

`photo_sorting: filename` removes that dependency by sorting each album's photos in the renderer instead. The sort is natural, not lexicographic, so `photo-2.jpg` comes before `photo-10.jpg` whether or not filenames are zero-padded.

`order_switcher: true` adds a `<select>` to the top right of the navbar, next to the theme toggle, offering the rendered order or a random one. The chosen order is written to an `order` query parameter (`?order=date`, `?order=random`) so it survives a reload and can be shared; an unrecognised value falls back to `date`.

Switching order re-orders the `items` array and re-initializes the gallery, rather than using nanogallery2's own `gallerySorting`. That option is applied per nav level, so it would miss photos rendered at level 1 on `album_routing` album pages. Working on the array covers both layouts and never reorders album covers — only the runs of photos between them, so each photo stays in its own album. Because re-initializing returns to the album overview, the album being viewed is reopened afterwards via nanogallery2's `displayItem` API.


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