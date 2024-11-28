import numpy as np
import sys
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import math
import random

def generate_perlin_noise(shape, rescale=255):
    # Generate Perlin noise using numpy
    size_x, size_y = shape
    noise = np.random.rand(size_x, size_y)
    noise = np.interp(noise, (0, 1), (128, rescale)).astype(np.uint8)   
    return noise

# applies blur accordingly to perlin noise
def apply_perlin_blur(image, coeff, scale=0.002, rescale=255):
    # Resize the image for noise generation
    width, height = image.size
    resized_width = int(width * scale)
    resized_height = int(height * scale)
    
    # Generate Perlin noise
    noise = generate_perlin_noise((resized_width, resized_height), rescale=rescale)
    # Create a Pillow image from the noise
    noise_image = Image.fromarray(noise)
    # Resize the noise image back to the original size
    noise_image = noise_image.resize((width, height), Image.BICUBIC)
    # Apply the noise as a blur effect to the original image
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=coeff))
    blurred_image = Image.composite(image, blurred_image, mask=noise_image)
    return blurred_image

# applies the brightness, but not everywhere in the image
def apply_perlin_brighness(image, coeff, scale=0.002, rescale=255):
    width, height = image.size
    resized_width = int(width * scale)
    resized_height = int(height * scale)
    # Generate Perlin noise
    noise = generate_perlin_noise((resized_width, resized_height), rescale=rescale)
    # Create a Pillow image from the noise
    noise_image = Image.fromarray(noise)
    # Resize the noise image back to the original size
    noise_image = noise_image.resize((width, height), Image.BICUBIC)
    brightened = brighten(image, coeff)
    return Image.composite(image, brightened, mask=noise_image)


# curves a right/left half of image (impression of book page scanned)
# side --> 0 = left, 1 = right; 
# coeff1 = kernel size, coeff2 = wave length, coeff3 = amplitude
def curveSide(image, side, coeff1, coeff2, coeff3):
    if(side == 0):
        return image
    class Deformer():
        def transform(self, x, y):
            y = y + math.fabs(x - self.w // 2) * coeff3 * math.sin(x/coeff2)
            return x, y
        def transform_rectangle(self, x0, y0, x1, y1):
            return (*self.transform(x0, y0),
                *self.transform(x0, y1),
                *self.transform(x1, y1),
                *self.transform(x1, y0),
                )
        def getmesh(self, img):
            self.w, self.h = img.size
            gridspace = coeff1
            
            target_grid = []
            if(side == 1):
                for x in range(0, self.w // 2, gridspace):
                    for y in range(0, self.h, gridspace):
                        target_grid.append((x, y, x + gridspace, y + gridspace))
            else:
                for x in range(self.w // 2, self.w, gridspace):
                    for y in range(0, self.h, gridspace):
                        target_grid.append((x, y, x + gridspace, y + gridspace))

            source_grid = [self.transform_rectangle(*rect) for rect in target_grid]

            res = [t for t in zip(target_grid, source_grid)]
            if(side == 1):
                res.append(((self.w//2, 0, self.w, self.h),(self.w // 2, 0, self.w // 2, self.h, self.w, self.h, self.w, 0)))
            else:
                res.append(((0, 0, self.w // 2, self.h),(0, 0, 0, self.h, self.w//2, self.h, self.w // 2, 0)))
            return res
    return ImageOps.deform(image, Deformer())
# erodes
def erosion(image, coeff):
    if(coeff == 0):
        return image
    return image.filter(ImageFilter.MinFilter(coeff))
# dilates
def dilation(image, coeff):
    if(coeff == 0):
        return image
    return image.filter(ImageFilter.MaxFilter(coeff))
# downscales (hurts quality)
def downscale(image, coeff):
    if(coeff == 0):
        return image
    w, h = image.size
    image = image.resize((w // coeff, h // coeff))
    image = image.resize((w, h))
    return image

# brightens image by <coeff>
def brighten(image, coeff):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(coeff)

# enhances color by <coeff>
def balance_color(image, coeff):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(coeff)

# changes contrast by <coeff>
def contrast(image, coeff):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(coeff)

# sharpens image by <coeff>
def sharpen(image, coeff):
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(coeff)

# causes image to loose black colour for brownish (washed look)
def colorize(image, coeff):
    if(coeff == 0):
        return image
    image_new = ImageOps.colorize(image = image.convert("L"), black = (210, 180, 140), white = "white")
    return Image.blend(image, image_new, coeff)

# blends pictures together, watermark by <coeff> percantage, 
# flip = 0, the watermark stays the same
# flip = 1 -> flip left_right
# flip = 2 -> flip top_bottom
# flip = 3 -> flip left_right & top_bottom
def add_watermark(image, watermark, coeff, flip):
    if(flip == 0):
        return image
    else:
        watermark = Image.open(watermark)
    if(image.mode != watermark.mode):
        watermark = watermark.convert(image.mode)
    if((flip == 1) | (flip == 3)):
        watermark = watermark.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if((flip == 2) | (flip == 3)):
        watermark = watermark.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    # resize if neccessary:
    watermark = watermark.resize(image.size)
    
    # perlin noise for adaptive blending
    width, height = image.size
    resized_width = int(width * 0.001)
    resized_height = int(height * 0.001)
    # Generate Perlin noise
    noise = generate_perlin_noise((resized_width, resized_height), rescale=255)
    # Create a Pillow image from the noise
    noise_image = Image.fromarray(noise)
    # Resize the noise image back to the original size
    noise_image = noise_image.resize((width, height), Image.BICUBIC)

    watermark = Image.composite(image, watermark, mask=noise_image)
    return Image.blend(image, watermark, coeff)   

# randomly puts black & white pixels on image, by percantage <coeff>
def salt_pepper(image, coeff):
    w, h = image.size
    pepper = coeff / 100
    num = (math.floor(w * h * pepper))
    x_p = random.sample(range(w), num // h)
    y_p = random.sample(range(h), num // w)
    x_s = random.sample(range(w), num // h)
    y_s = random.sample(range(h), num // w)
    for i in range(len(x_p)):
        for j in range(len(y_p)):
            a =  random.randrange(100)
            if(x_p[i] + a >= w):
                a = 0 - a
            b = random.randrange(100)
            if(y_p[j] + b >= h):
                b = 0 - b
            image.putpixel((x_p[i] + a, y_p[j] + b), (0, 0, 0))  
    for i in range(len(x_s)):
        for j in range(len(y_s)):
            a =  random.randrange(100)
            if(x_s[i] + a >= w):
                a = 0 - a
            b = random.randrange(100)
            if(y_s[j] + b >= h):
                b = 0 - b
            image.putpixel((x_s[i] + a, y_s[j] + b), (255, 255, 255)) 
    return image

# rotates picture for <coeff> degrees counterclookwise, fills blank with tan color
def rotate(image, coeff):
    return image.rotate(coeff, expand = True, fillcolor = (210, 180, 140))  # color is <tan>

################################################################################################################
################################################################################################################
# MAIN:



if(len(sys.argv) < 2):
    print("Please provide input image")
if(len(sys.argv) < 18):
    print("Please provide all the arguments for image processing")



###  erosion  dilation  downscale brighten, contrast, sharpen, rotate, side, c1, c2, c3, salt-pepper, watermark, flip, colorize, kernel size for blur
###     2         3         4         5         6        7       8       9   10  11  12      13           14      15      16             17         

image = Image.open(sys.argv[1])

new_image = erosion(image, int(sys.argv[2]))
new_image = dilation(new_image, int(sys.argv[3]))
new_image = colorize(new_image, float(sys.argv[16]))
new_image = downscale(new_image, int(sys.argv[4]))
new_image = apply_perlin_brighness(new_image, float(sys.argv[5]))
new_image = contrast(new_image, float(sys.argv[6]))
new_image = sharpen(new_image, float(sys.argv[7]))

new_image = add_watermark(new_image, sys.argv[14], 0.1, int(sys.argv[15]))
new_image = curveSide(new_image, int(sys.argv[9]), int(sys.argv[10]), float(sys.argv[11]), float(sys.argv[12]))
new_image = rotate(new_image, float(sys.argv[8]))
new_image = salt_pepper(new_image, float(sys.argv[13]))

new_image = apply_perlin_blur(new_image, int(sys.argv[17]))
file_name = os.path.splitext(os.path.basename(sys.argv[1]))
file_path = os.path.dirname(sys.argv[1])
new_path = os.path.join(file_path, file_name[0] + "_modified" + file_name[1])

new_image.save(new_path, "PNG")