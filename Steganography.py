from flask import Flask, request, render_template, redirect, flash, send_file, url_for
from PIL import Image
import os


app = Flask(__name__)
app.secret_key = "super secret key"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def upload_file() :
    return render_template("applications.html")

@app.route('/upload', methods = ['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'static/')
    print(target)

    if not os.path.isdir(target) :
        os.mkdir(target)

    file1 = request.files['img1']
    destination = "/".join([target, "img1.png"])
    file1.save(destination)

    file2 = request.files['img2']
    destination = "/".join([target, "img2.png"])
    file2.save(destination)



    #url1 = 'C:/Users/Aryaman agarwal/PycharmProjects/Steganography'

    #input1 = Image.open('C:/Users/Aryaman agarwal/PycharmProjects/Steganography/test/img1.png')
    #input2 = Image.open('C:/Users/Aryaman agarwal/PycharmProjects/Steganography/test/img2.png')

    input1 = Image.open(file1)
    input2 = Image.open(file2)

    merged_image = Steganography.merge(input1, input2)
    destination = "/".join([target, "output1.png"])
    merged_image.save(destination)

    out = Image.open('output1.png')
    rev = Steganography.unmerge(out)
    rev.save('outrev.png')

    flash("Images Uploaded Successfully!")
    return redirect('/')

@app.route('/downloadImg', methods = ['GET'])
def download_img() :
    p = "output1.png"
    return send_file(p, as_attachment=True)



class Steganography(object) :
 
 def __int_to_bin(rgb) : 
  r, g, b = rgb
  return ('{0:08b}'.format(r),
          '{0:08b}'.format(g),
          '{0:08b}'.format(b))

 def __bin_to_int(rgb) : 
  r, g, b = rgb
  return (int(r, 2),
          int(g, 2),
          int(b, 2))

 def __merge_rgb(rgb1, rgb2) : 
  r1, g1, b1 = rgb1
  r2, g2, b2 = rgb2

  rgb = (r1[:4] + r2[:4],
         g1[:4] + g2[:4],
         b1[:4] + b2[:4])

  return rgb

 def merge(img1, img2) : 
  if img2.size[0] > img1.size[0] or img2.size[1] > img1.size[1] : 
   raise ValueError('Image 2 should not be larger than Image 1')

  pixel_map1 = img1.load()
  pixel_map2 = img2.load()

  new_image = Image.new(img1.mode, img1.size)
  pixels_new = new_image.load()

  const_wht_rgb = Steganography.__int_to_bin((0, 0, 0))

  for i in range(img1.size[0]) : 
   for j in range(img1.size[1]) :

    rgb1 = Steganography.__int_to_bin(pixel_map1[i, j])
   
    if i <  img2.size[0] or j < img2.size[1] : 
     rgb2 = Steganography.__int_to_bin(pixel_map2[i, j])

    else :      
     rgb2 = const_wht_rgb

    rgb = Steganography.__merge_rgb(rgb1, rgb2)

    pixels_new[i, j] = Steganography.__bin_to_int(rgb)

  return new_image

 def unmerge(img):

  pixel_map = img.load()

  new_image = Image.new(img.mode, img.size)
  pixels_new = new_image.load()

  original_size = img.size

  for i in range(img.size[0]):
   for j in range(img.size[1]):
     r, g, b = Steganography.__int_to_bin(pixel_map[i, j])

     rgb = (r[4:] + '0000',
            g[4:] + '0000',
            b[4:] + '0000')

     pixels_new[i, j] = Steganography.__bin_to_int(rgb)

     if pixels_new[i, j] != (0, 0, 0):
      original_size = (i + 1, j + 1)

  new_image = new_image.crop((0, 0, original_size[0], original_size[1]))

  return new_image 



if (__name__ == "__main__"):

    app.run(debug=True)
