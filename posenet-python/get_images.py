import argparse
import os
import cv2

parser = argparse.ArgumentParser()

parser.add_argument('--video_dir', type=str, default='./video/A.mp4')
parser.add_argument('--output_dir', type=str, default='./imagesA/')

args = parser.parse_args()


def main():
  
  if args.output_dir:
      if not os.path.exists(args.output_dir):
          os.makedirs(args.output_dir)
                
  vidcap = cv2.VideoCapture(args.video_dir)
  def getFrame(sec):
      vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
      hasFrames,image = vidcap.read()
      if hasFrames:
          
          if count <10:
            cv2.imwrite(args.output_dir + "/image"+"0000"+str(count)+".jpg", image)     # save frame as JPG file
          elif count <100:
            cv2.imwrite(args.output_dir + "/image"+"000"+str(count)+".jpg", image)
          elif count <1000:
            cv2.imwrite(args.output_dir + "/image"+"00"+str(count)+".jpg", image)
          elif count <10000:
            cv2.imwrite(args.output_dir + "/image"+"0"+str(count)+".jpg", image)
          else:
            cv2.imwrite(args.output_dir + "/image"+str(count)+".jpg", image)
          
      return hasFrames
  sec = 0
  frameRate = 1/24 #//it will capture 24 images in 1 seconnd
  count=1
  success = getFrame(sec)
  while success:
      count = count + 1
      sec = sec + frameRate
      sec = round(sec, 2)
      success = getFrame(sec)

if __name__ == "__main__":
    main()
