from app.models.schemas import (
    ComicRequest,
    GeneratedPanel,
)

from app.services.layout_builder import (
    build_comic_layout
)


def test_request_validation():

    request = ComicRequest(

        story_prompt=
            "A fox explores a forest",

        character_name=
            "Milo",

        setting=
            "Forest",

        tone=
            "funny",

        art_style=
            "comic book",

        panel_count=
            5
    )

    assert request.panel_count == 5


def test_layout_builder():

    panels = [

        GeneratedPanel(

            panel_number=1,

            title="The Beginning",

            scene_description=
                "A fox enters a forest.",

            image_prompt=
                "comic fox forest",

            narration=
                "Milo enters the forest.",

            dialogue=
                "Hello!",

            caption=
                "Morning",

            image_path=
                "/static/panels/test.png",
        )
    ]

    layout = build_comic_layout(
        panels
    )

    assert len(layout) == 1

    assert (
        layout[0]["panel_number"]
        == 1
    )