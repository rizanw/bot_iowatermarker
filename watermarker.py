from PIL import Image


def watermark_with_transparency(input_image_path,
                                output_image_path,
                                watermark_image_path,
                                position):
    base_image = Image.open(input_image_path)
    watermark = Image.open(watermark_image_path)

    init = base_image.size[0] / 4
    scale = round(watermark.size[0] / init)
    width = (watermark.size[0]/scale)
    height = (watermark.size[1]/scale)

    w, h = base_image.size
    h = int(7)
    w = int(w / 2 - width / 2)
    position = (w, h)

    watermark = watermark.resize((int(width), int(height)), Image.ANTIALIAS)

    transparent = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, position, mask=watermark)
    transparent.save(output_image_path, "PNG")

# if __name__ == '__main__':
#     img = 'static/temp/data.jpg'
#     watermark_with_transparency(img, 'lighthouse_watermarked3.jpg',
#                                 'static/watermark.png', position=(0, 0))
