import os
import cv2

def clearDirectory(directory_path):
    '''
    Thank you OpenAI
    '''
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            clearDirectory(item_path)
            os.rmdir(item_path)

def compressImage(imgPath):
    # Load image and break down path
    img = cv2.imread(imgPath)
    split = imgPath.split("/")

    # Enter Compressed directory
    os.chdir('Compressed/')

    # Create new/Enter pre-existing directory to write compressed image
    if split[-2] not in os.listdir():
        os.mkdir(split[-2])
        os.chdir(split[-2] + '/')
        cv2.imwrite(split[-1], img)
    else:
        os.chdir(split[-2] + '/')
        cv2.imwrite(split[-1], img)

    # Exit all the way back to original directory
    os.chdir('../../')

def compressVideo(vidPath):
    '''
    https://www.opencvhelp.org/tutorials/advanced/video-compression/
    '''
    cap = cv2.VideoCapture(vidPath)
    split = vidPath.split("/")

    if split[-2] not in os.listdir('Compressed/'):
        os.mkdir('Compressed/' + split[-2])

    output_file = 'Compressed/' + '/'.join(split[-2:])

    # Get video details (width, height, and frames per second)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # You can use other codecs like 'XVID', 'MJPG', 'DIVX', etc.
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break  # Break the loop if no frames are read

        out.write(frame)

    # Release the video capture and writer objects
    cap.release()
    out.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()

clearDirectory('Compressed/')
rootdir = 'ImagesAndVideos/'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if not(".DS_Store" in os.path.join(subdir, file)):
            if os.path.join(subdir, file).endswith(".png"):
                compressImage(os.path.join(subdir, file))
            elif os.path.join(subdir, file).endswith(".mp4"):
                compressVideo(os.path.join(subdir, file))
            else:
                print("What the fuck")

print("Done")
