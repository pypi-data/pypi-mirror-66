import os
import html
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from cairosvg import svg2png
from base64 import urlsafe_b64encode

from django.utils.html import strip_tags
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.templatetags.static import static

from wagtail.core import hooks
from wagtail.core.models import Collection
from wagtail.images.models import Image as WagtailImage
from wagtail.documents.models import Document

from .conf import setting
from .models import OpenGraphImageGeneratorSettings


OG_WIDTH = setting('IMAGE_WIDTH')
OG_HEIGHT = setting('IMAGE_HEIGHT')
OG_PADDING = setting('IMAGE_PADDING')

TEXT_START_X = OG_PADDING
TEXT_START_Y = OG_HEIGHT - OG_PADDING
COLOR_WHITE = (255, 255, 255, 255)
COLOR_BLACK = (0, 0, 0, 255)


def get_font_width(font, text):
    return font.getsize(text)[0]


def get_font_height(font, text):
    ascent, descent = font.getmetrics()
    (width, baseline), (offset_x, offset_y) = font.font.getsize(text)
    total_line_height = offset_y + (ascent - offset_y) + descent
    return total_line_height


def create_default_og_image(
    request, page, browser_output, extra_data, canvas, drawable
):
    folder = os.path.dirname(os.path.dirname(__file__))

    og_generator_settings = OpenGraphImageGeneratorSettings.for_site(request.site)

    if og_generator_settings.default_background_image:
        with og_generator_settings.default_background_image.get_willow_image() as img:
            og_default_bg_image = img.get_pillow_image()
    else:
        og_default_bg_image = None

    try:
        font_bold = ImageFont.truetype(
            '{}/wagtail_opengraph_image_generator/static/wagtail_opengraph_image_generator/fonts/opensans-bold.ttf'.format(
                folder
            ),
            42,
        )
        font_regular = ImageFont.truetype(
            '{}/wagtail_opengraph_image_generator/static/wagtail_opengraph_image_generator/fonts/opensans-regular.ttf'.format(
                folder
            ),
            42,
        )
    except OSError:
        font_bold = ImageFont.load_default()
        font_regular = ImageFont.load_default()

    overlay_type = extra_data.get('variant', 'light')
    if overlay_type == 'dark':
        if og_generator_settings.company_logo_alternative:
            with og_generator_settings.company_logo_alternative.get_willow_image() as img:
                company_logo = img.get_pillow_image()
        else:
            company_logo = None
        fade = Image.open(
            '{}/wagtail_opengraph_image_generator/static/wagtail_opengraph_image_generator/fade_black.png'.format(
                folder
            )
        )
        color = COLOR_WHITE
    else:
        if og_generator_settings.company_logo:
            with og_generator_settings.company_logo.get_willow_image() as img:
                company_logo = img.get_pillow_image()
        else:
            company_logo = None
        fade = Image.open(
            '{}/wagtail_opengraph_image_generator/static/wagtail_opengraph_image_generator/fade_white.png'.format(
                folder
            )
        )
        color = COLOR_BLACK

    # Add background image & company logo to the canvas
    fade = fade.resize((OG_WIDTH, OG_HEIGHT))
    preview_header_image = extra_data.get('background_image', None)
    og_bg_image = None
    if preview_header_image:
        with WagtailImage.objects.get(
            pk=preview_header_image
        ).get_willow_image() as img:
            og_bg_image = img.get_pillow_image()
    else:
        page_background_image = getattr(page, setting('FIELD_BACKGROUND_IMAGE'), None)
        if page_background_image and browser_output is False:
            with page_background_image.get_willow_image() as img:
                og_bg_image = img.get_pillow_image()
        else:
            og_bg_image = og_default_bg_image

    if og_bg_image:
        og_bg_image = ImageOps.fit(og_bg_image, (OG_WIDTH, OG_HEIGHT), Image.ANTIALIAS)
        canvas.paste(og_bg_image, (0, 0))
        canvas.paste(fade, (0, 0), fade)
    else:
        if color == COLOR_BLACK:
            canvas.paste(COLOR_WHITE, [0, 0, OG_WIDTH, OG_HEIGHT])
        elif color == COLOR_WHITE:
            canvas.paste(COLOR_BLACK, [0, 0, OG_WIDTH, OG_HEIGHT])
    if company_logo:
        canvas.paste(company_logo, (OG_PADDING, OG_PADDING), company_logo)

    # Prepare title lines to see where start drawing stuff
    preview_title = extra_data.get('title', None)
    if preview_title:
        og_title_lines = preview_title.split('</span></span></div></div>')
    else:
        title_field = getattr(page, setting('FIELD_TITLE'), None)
        if title_field and browser_output is False:
            og_title_lines = title_field.split('</p><p>')
        else:
            og_title_lines = None
    if og_title_lines:
        og_title_lines = list(
            filter(None, map(lambda x: strip_tags(x), og_title_lines))
        )
        num_title_lines = len(og_title_lines)
    else:
        num_title_lines = 0

    # Prepare subtitle lines to see where we start drawing stuff
    preview_text = extra_data.get('subtitle', None)
    if preview_text:
        og_text_lines = preview_text.split('</span></span></div></div>')
    else:
        subtitle_field = getattr(page, setting('FIELD_SUBTITLE'), None)
        if subtitle_field and browser_output is False:
            og_text_lines = subtitle_field.split('</p><p>')
        else:
            og_text_lines = None
    if og_text_lines:
        og_text_lines = list(filter(None, map(lambda x: strip_tags(x), og_text_lines)))
        num_lines = len(og_text_lines)
    else:
        num_lines = 0

    # Calculate font sizes to correctly ascertain starting position
    if num_title_lines > 0:
        title_height = get_font_height(font_bold, og_title_lines[0]) * (num_title_lines)
    else:
        title_height = get_font_height(
            font_bold, extra_data.get('default_title', page.title if page else '')
        )
    curY = TEXT_START_Y - title_height

    if num_lines > 0:
        curY -= get_font_height(font_regular, og_text_lines[0]) * (num_lines)

    # Convert optional page SVG icon to PNG and add it to the canvas
    logo_file = None
    preview_logo = extra_data.get('logo', None)
    if preview_logo:
        logo_file = Document.objects.get(pk=preview_logo).file
    else:
        page_logo = getattr(page, setting('FIELD_LOGO'), None)
        if page_logo and browser_output is False:
            logo_file = page_logo.file
    if logo_file:
        png_icon_str = svg2png(file_obj=logo_file)
        png_icon = Image.open(BytesIO(png_icon_str))
        curY -= png_icon.height
        canvas.paste(png_icon, (OG_PADDING, curY), png_icon)
        curY += png_icon.height + 8

    # Draw the page title
    if og_title_lines:
        for line in og_title_lines:
            line = html.unescape(line)
            drawable.text((TEXT_START_X, curY), line, font=font_bold, fill=color)
            curY += get_font_height(font_bold, line)
    else:
        drawable.text(
            (TEXT_START_X, curY),
            extra_data.get('default_title', page.title if page else ''),
            font=font_bold,
            fill=color,
        )
        curY += (
            get_font_height(
                font_bold, extra_data.get('default_title', page.title if page else '')
            )
            + 4
        )

    # Draw the subtitle lines
    if og_text_lines:
        for line in og_text_lines:
            line = html.unescape(line)  # unescape to allow entities like '&'
            drawable.text((TEXT_START_X, curY), line, font=font_regular, fill=color)
            curY += get_font_height(font_regular, line)

    return canvas


def create_og_image(request, page, browser_output=False, extra_data={}):
    # Set up canvas and drawable
    canvas = Image.new('RGB', (OG_WIDTH, OG_HEIGHT))
    drawable = ImageDraw.Draw(canvas)

    # Delegate creation to a custom hook function if there is one registered
    custom_hook = hooks.get_hooks('wagtail_opengraph_image_generator_generation')
    if custom_hook:
        canvas = custom_hook[-1](
            request, page, browser_output, extra_data, canvas, drawable
        )
    else:
        canvas = create_default_og_image(
            request, page, browser_output, extra_data, canvas, drawable
        )

    # Create image
    # Append random string to avoid S3 CDN cache issues
    og_file_name = 'og_{}_{}.png'.format(
        page.slug if page else 'preview',
        urlsafe_b64encode(os.urandom(6)).decode('utf-8'),
    )
    buf = BytesIO()
    canvas.save(buf, format='PNG')
    buf.seek(0)

    if browser_output:
        return buf
    else:
        # Get correct Collection or create if it doesn't exist
        try:
            collection = Collection.objects.get(name=setting('COLLECTION_NAME'))
        except Collection.DoesNotExist:
            collection = Collection(name=setting('COLLECTION_NAME'))
            root_collection = Collection.get_first_root_node()
            root_collection.add_child(instance=collection)

        # Clear other/older versions of the page's generated OG images
        WagtailImage.objects.filter(title=og_file_name, collection=collection).delete()

        # Convert Django image to Wagtail image
        django_image = InMemoryUploadedFile(
            buf, 'open_graph_image', og_file_name, 'image/png', buf.tell(), None
        )
        wagtail_image = WagtailImage(
            title=og_file_name, file=django_image, collection=collection
        )
        wagtail_image.save()

        # Return new OG image
        return wagtail_image
