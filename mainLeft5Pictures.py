from picamera2 import Picamera2, Preview
import time
import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
from licence_plate import RoLicensePlate

'''
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)
picam2.capture_file("CAR0.jpg")
picam2.capture_file("CAR1.jpg")
picam2.capture_file("CAR2.jpg")
picam2.capture_file("CAR3.jpg")
picam2.capture_file("CAR4.jpg")
'''
for i in range(5):
    picture = "Images/CAR"+str(i)+".jpg"
    print(picture)
    img = cv2.imread(picture,cv2.IMREAD_COLOR)
    #img = cv2.imread('testLeftRight.jpg',cv2.IMREAD_COLOR)
    img = cv2.resize(img, (620,480) )

    # Split the image (left halve)
    height, width, _ = img.shape
    img = img[:, :width // 2]
    height, width, _ = img.shape

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200) #Perform Edge detection

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]

    screenCnt = None
    # loop over our contours

    for c in cnts:

        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")

    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
        
    # Masking the part other than the number plate
    mask = np.zeros(gray.shape,np.uint8)
    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
    new_image = cv2.bitwise_and(img,img,mask=mask)

    # Now crop
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx+1, topy:bottomy+1]

    #Read the number plate
    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    text = text[:len(text)-1]
    print(f"Detected Number is: {text}")


    plate1 = RoLicensePlate(text)
    if(plate1.is_roLicensePlate()):
        print(f"+Valid\n")
        break
    else:
        print(f"-Invalid\n")
    #cv2.imshow('image',img)
    #cv2.imshow('Cropped',Cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




'''
import cv2
import imutils
import numpy as np
import pytesseract
from licence_plate import RoLicensePlate

# Load the image
img = cv2.imread('testLeftRight.jpg', cv2.IMREAD_COLOR)
img = cv2.resize(img, (620, 480))

# Split the image into left and right halves
height, width, _ = img.shape
left_half = img[:, :width // 2]

# Convert left half to grayscale
gray = cv2.cvtColor(left_half, cv2.COLOR_BGR2GRAY)

# Blur to reduce noise
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Perform edge detection
edged = cv2.Canny(gray, 30, 200)

# Find contours
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]

screenCnt = None

# Loop over contours
for c in cnts:
    # Approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.018 * peri, True)

    # If the contour has four points, assume it's the license plate
    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print("No contour detected")
else:
    detected = 1
    cv2.drawContours(left_half, [screenCnt], -1, (0, 255, 0), 3)

# Mask the region of interest
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1)
new_image = cv2.bitwise_and(left_half, left_half, mask=mask)

# Find the coordinates of non-zero elements in the mask
(x, y) = np.nonzero(mask)

# Find the bounding box of the contour
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))

# Crop the number plate region
cropped_plate = gray[topx:bottomx + 1, topy:bottomy + 1]

# Read the number plate
text = pytesseract.image_to_string(cropped_plate, config='--psm 11')
print("Detected Number is:", text)

# Validate the number plate
plate1 = RoLicensePlate(text)
print(f"Valid? {plate1.is_roLicensePlate()}\n")

# Display the results
cv2.imshow('Left Half with Contour and License Plate', left_half)
cv2.imshow('Cropped Plate', cropped_plate)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
