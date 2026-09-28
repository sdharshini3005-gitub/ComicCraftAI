from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse

from app.config import settings
from app.models.schemas import ComicRequest, GeneratedPanel
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "default_panels": settings.default_panels,
        },
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(request: Request):
    form = await request.form()

    comic_request = ComicRequest(
        story_prompt=str(form.get("story_prompt", "")),
        character_name=str(form.get("character_name", "")),
        setting=str(form.get("setting", "")),
        tone=str(form.get("tone", "Funny")),
        art_style=str(form.get("art_style", "Comic Book")),
        panel_count=int(
            form.get(
                "panel_count",
                settings.default_panels,
            )
        ),
    )

    try:
        outlines = generate_outline(comic_request)

        story_items = generate_story(outlines)

        story_map = {
            int(item["panel_number"]): item
            for item in story_items
        }

        panels = []

        for outline in outlines:
            story = story_map.get(
                outline.panel_number,
                {},
            )

            image_path = generate_image(
                outline.image_prompt,
                outline.panel_number,
            )

            panels.append(
                GeneratedPanel(
                    panel_number=outline.panel_number,
                    title=outline.title,
                    scene_description=outline.scene_description,
                    image_path=image_path,
                    caption=str(
                        story.get("caption", "")
                    ),
                    narration=str(
                        story.get("narration", "")
                    ),
                    dialogue=str(
                        story.get("dialogue", "")
                    ),
                )
            )

        layout = build_comic_layout(panels)

        return request.app.state.templates.TemplateResponse(
            "comic_preview.html",
            {
                "request": request,
                "panels": layout,
            },
        )

    except Exception as error:
        return HTMLResponse(
            f"""
            <html>
            <body>
                <h2>ComicCraft Error</h2>
                <pre>{error}</pre>
                <a href="/">Go Back</a>
            </body>
            </html>
            """,
            status_code=500,
        )


@router.post("/generate-comic/json")
async def generate_comic_json(comic_request: ComicRequest):
    outlines = generate_outline(comic_request)

    story_items = generate_story(outlines)

    story_map = {
        int(item["panel_number"]): item
        for item in story_items
    }

    panels = []

    for outline in outlines:
        story = story_map.get(
            outline.panel_number,
            {},
        )

        image_path = generate_image(
            outline.image_prompt,
            outline.panel_number,
        )

        panels.append(
            GeneratedPanel(
                panel_number=outline.panel_number,
                title=outline.title,
                scene_description=outline.scene_description,
                image_path=image_path,
                caption=str(
                    story.get("caption", "")
                ),
                narration=str(
                    story.get("narration", "")
                ),
                dialogue=str(
                    story.get("dialogue", "")
                ),
            )
        )

    return {
        "panels": [
            panel.model_dump()
            for panel in panels
        ]
    }


@router.post("/export")
async def export_comic(request: Request):
    form = await request.form()

    panels = []

    panel_count = int(
        form.get("panel_count", 0)
    )

    for i in range(1, panel_count + 1):
        panels.append(
            {
                "panel_number": i,
                "title": str(
                    form.get(f"title_{i}", "")
                ),
                "image_path": str(
                    form.get(f"image_path_{i}", "")
                ),
                "scene_description": str(
                    form.get(
                        f"scene_description_{i}",
                        "",
                    )
                ),
                "caption": str(
                    form.get(
                        f"caption_{i}",
                        "",
                    )
                ),
                "dialogue": str(
                    form.get(
                        f"dialogue_{i}",
                        "",
                    )
                ),
            }
        )

    pdf_path = save_pdf(panels)

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="comiccraft_comic.pdf",
    )


@router.get("/test-image")
async def test_image():
    image_path = generate_image(
        "A funny monkey in a magical jungle",
        1,
    )

    return {
        "status": "success",
        "image": image_path,
    }