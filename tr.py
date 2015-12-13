import PythonMagick
print "inside tr"
#input, output as PNG format
image = PythonMagick.Image("/home/mininet/test_udp_transcoder_local/udp_transcoder/serv_image.png")

print 'The original image size is ',image.fileSize()

#resize image
##image.transform('300x300!')

image.magick('jpg')
image.write('output.jpg')

print image.fileName()
print image.magick()
print image.size().width()
print image.size().height()
print image.quality()
print 'The transcoded image size is ',image.fileSize()
