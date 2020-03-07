import cv2

def rotate_image(img, angle):
  """逆时针旋转图片"""
  code = None
  if angle == 90:
    code = cv2.ROTATE_90_COUNTERCLOCKWISE
  elif angle == 180:
    code = cv2.ROTATE_180
  elif angle == 270:
    code = cv2.ROTATE_90_CLOCKWISE
  
  if code is None:
    rotated = img
  else:
    rotated = cv2.rotate(img, code)
  
  return rotated
