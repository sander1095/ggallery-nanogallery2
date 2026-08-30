from typing import cast
import unittest
from src.renderer import NanoGalleryTemplateRenderer
from ggallery.renderers.base_renderer import RendererParameters
from ggallery.model import AlbumConfig, PhotoConfig, RenderedFile


class TestNanoGalleryTemplateRenderer(unittest.TestCase):
    def setUp(self):
        self.renderer = NanoGalleryTemplateRenderer()
        self.parameters = RendererParameters(
            base_url="http://example.com/",
            title="Test Gallery",
            subtitle="A collection of test images",
            favicon="http://example.com/favicon.ico",
            albums=[
                AlbumConfig(
                    title="Album 1",
                    photos=[
                        PhotoConfig(filename="photo1.jpg", thumbnail="thumb1.jpg", title="Photo 1"),
                        PhotoConfig(filename="photo2.jpg", thumbnail="thumb2.jpg", title="Photo 2"),
                    ],
                    cover=None,
                ),
                AlbumConfig(
                    title="Album 2",
                    photos=[
                        PhotoConfig(filename="photo3.jpg", thumbnail="thumb3.jpg", title="Photo 3"),
                    ],
                    cover="cover2.jpg",
                ),
            ],
            thumbnail_height=200,
        )

    def test_render(self):
        result = self.renderer.render(self.parameters)
        self.assertIsInstance(result, RenderedFile)
        result = cast(RenderedFile, result)
        content = result.content
        self.assertIsInstance(content, str)
        content = cast(str, result.content)
        self.assertIn("<title>Test Gallery</title>", content)
        self.assertIn("src: 'cover2.jpg'", content)
        self.assertIn("src: 'photo1.jpg'", content)
        self.assertIn("srct: 'thumb1.jpg'", content)
        self.assertIn("title: 'Album 1'", content)
        self.assertIn("title: 'Photo 1'", content)

    def test_download_buttons_disabled_by_default(self):
        result = cast(RenderedFile, self.renderer.render(self.parameters))
        content = cast(str, result.content)
        self.assertIn("topRight: 'closeButton'", content)
        self.assertIn("thumbnailToolbarImage: { topLeft: '', bottomRight: '', topRight: '', bottomLeft: '' }", content)

    def test_download_buttons_enabled_via_template_parameters(self):
        self.parameters.template_parameters = {
            "viewer_download_button": True,
            "thumbnail_download_button": True,
        }
        result = cast(RenderedFile, self.renderer.render(self.parameters))
        content = cast(str, result.content)
        self.assertIn("topRight: 'downloadButton,closeButton'", content)
        self.assertIn(
            "thumbnailToolbarImage: { topLeft: '', bottomRight: '', topRight: 'DOWNLOAD', bottomLeft: '' }", content
        )


    def test_photos_keep_source_order_by_default(self):
        self.parameters.albums[0].photos = [
            PhotoConfig(filename="photo-10.jpg", thumbnail="thumb-10.jpg"),
            PhotoConfig(filename="photo-2.jpg", thumbnail="thumb-2.jpg"),
        ]
        content = self.__render()
        self.assertLess(content.index("src: 'photo-10.jpg'"), content.index("src: 'photo-2.jpg'"))

    def test_photos_sorted_by_filename_use_natural_order(self):
        self.parameters.albums[0].photos = [
            PhotoConfig(filename="photo-10.jpg", thumbnail="thumb-10.jpg"),
            PhotoConfig(filename="photo-2.jpg", thumbnail="thumb-2.jpg"),
            PhotoConfig(filename="photo-1.jpg", thumbnail="thumb-1.jpg"),
        ]
        self.parameters.template_parameters = {"photo_sorting": "filename"}
        content = self.__render()
        self.assertLess(content.index("src: 'photo-1.jpg'"), content.index("src: 'photo-2.jpg'"))
        self.assertLess(content.index("src: 'photo-2.jpg'"), content.index("src: 'photo-10.jpg'"))

    def test_album_cover_falls_back_to_first_sorted_photo(self):
        self.parameters.albums[0].photos = [
            PhotoConfig(filename="photo-10.jpg", thumbnail="thumb-10.jpg"),
            PhotoConfig(filename="photo-2.jpg", thumbnail="thumb-2.jpg"),
        ]
        self.parameters.albums[0].cover = None
        self.parameters.template_parameters = {"photo_sorting": "filename"}
        content = self.__render()
        self.assertIn("src: 'thumb-2.jpg'", content)

    def test_order_switcher_absent_by_default(self):
        content = self.__render()
        self.assertNotIn('id="order-select"', content)
        self.assertIn("const ORDER_SWITCHER_ENABLED = false;", content)

    def test_order_switcher_rendered_when_enabled(self):
        self.parameters.template_parameters = {"order_switcher": True}
        content = self.__render()
        self.assertIn('id="order-select"', content)
        self.assertIn("const ORDER_SWITCHER_ENABLED = true;", content)
        self.assertIn('<option value="date">Date</option>', content)
        self.assertIn('<option value="random">Random</option>', content)

    def test_order_switcher_labels_can_be_overridden(self):
        self.parameters.template_parameters = {
            "order_switcher": True,
            "order_switcher_labels": {"date": "Op datum", "random": "Willekeurig"},
        }
        content = self.__render()
        self.assertIn('<option value="date">Op datum</option>', content)
        self.assertIn('<option value="random">Willekeurig</option>', content)

    def test_order_switcher_only_shuffles_photos_not_album_covers(self):
        self.parameters.template_parameters = {"order_switcher": True}
        content = self.__render()
        # The shuffle walks runs of items and restarts at every album entry.
        self.assertIn("items[i].kind === 'album'", content)
        self.assertIn("function shuffleRange(items, from, to)", content)

    def test_select_mode_absent_by_default(self):
        content = self.__render()
        self.assertNotIn('id="select-toggle"', content)
        self.assertIn("const SELECT_MODE_ENABLED = false;", content)
        self.assertIn("thumbnailToolbarImage: { topLeft: '', bottomRight: '', topRight: '', bottomLeft: '' }", content)

    def test_select_mode_rendered_when_enabled(self):
        self.parameters.template_parameters = {"select_mode": True}
        content = self.__render()
        self.assertIn("const SELECT_MODE_ENABLED = true;", content)
        self.assertIn('id="select-toggle"', content)
        self.assertIn('id="select-all"', content)
        self.assertIn('id="select-none"', content)
        self.assertIn('id="download-selected"', content)
        self.assertIn('id="select-cancel"', content)
        self.assertIn(
            "thumbnailToolbarImage: { topLeft: 'SELECT', bottomRight: '', topRight: '', bottomLeft: '' }", content
        )
        self.assertIn(">Select<", content)
        self.assertIn(">Select all<", content)
        self.assertIn(">Select none<", content)
        self.assertIn(">Download<", content)
        self.assertIn(">Cancel<", content)

    def test_select_mode_labels_can_be_overridden(self):
        self.parameters.template_parameters = {
            "select_mode": True,
            "select_mode_labels": {
                "select": "Selecteren",
                "cancel": "Annuleren",
                "select_all": "Alles selecteren",
                "select_none": "Niets selecteren",
                "download": "Downloaden",
            },
        }
        content = self.__render()
        self.assertIn(">Selecteren<", content)
        self.assertIn(">Annuleren<", content)
        self.assertIn(">Alles selecteren<", content)
        self.assertIn(">Niets selecteren<", content)
        self.assertIn(">Downloaden<", content)
        self.assertIn('const DOWNLOAD_LABEL = "Downloaden";', content)

    def test_select_mode_combines_with_thumbnail_download_button(self):
        self.parameters.template_parameters = {"select_mode": True, "thumbnail_download_button": True}
        content = self.__render()
        self.assertIn(
            "thumbnailToolbarImage: { topLeft: 'SELECT', bottomRight: '', topRight: 'DOWNLOAD', bottomLeft: '' }",
            content,
        )

    def __render(self) -> str:
        result = cast(RenderedFile, self.renderer.render(self.parameters))
        return cast(str, result.content)


if __name__ == "__main__":
    unittest.main()
