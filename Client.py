import socket

from hume import HumeBatchClient
from hume.models.config import FaceConfig
from pprint import pprint
import hume
# importing the pygame library
import pygame
import pygame.camera



def start_client():
    # Set up client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = socket.gethostname()
    host = "192.168.195.242"
    port = 8000
    client_socket.connect((host, port))

    while True:
        # Send message to server
        message = input("Client: ")

        # -----------------Capturing Image, store it locally, and obtain emotion ratings-----------
        take_the_photo()
        client = HumeBatchClient("VGWAmgc9Kmmp1A0xyEoLiO6MWQjnFNBZRESaseSkf6smMJAx")
        # urls = ["https://thumbs.dreamstime.com/z/close-up-portrait-beautiful-young-latin-hispanic-woman-sad-face-looking-miserable-melancholy-depressed-human-facial-117693898.jpg"]
        config = FaceConfig()
        models = hume.models.config.FaceConfig()
        job = client.submit_job(None, [config], files=['test.jpg'])
        # status = job.get_status()
        # print(f"Job status: {status}")
    
        job.await_complete()
        full_predictions = job.get_predictions()
        for source in full_predictions:
            predictions = source["results"]["predictions"]
            for prediction in predictions:
                emotion_dict = prediction['models']['face']['grouped_predictions'][0]['predictions'][0]['emotions']
                # js = json.loads(emotion_json)
        
        emotions = sorted(emotion_dict, key=lambda x: x['score'], reverse=True)[:5]
    
        dict_emo = {}
        for x in emotions:
            dict_emo[x['name']]=x['score']
        # --------------------Emo Prediction From Hume Got-----------------------------------------


        # response = input("Server: ")
        message = message + '\n\n\n' + str(list(dict_emo.items()))
        # client_socket.send(response.encode())
        client_socket.send(message.encode())

        # Receive response from server
        received_response = client_socket.recv(1024).decode()
        print(f"Server: {received_response}")
        

    # Close the connection
    client_socket.close()

def take_the_photo():
    camlist = pygame.camera.list_cameras()

    # if camera is detected or not
    if camlist:
    
        # initializing the cam variable with default camera
        cam = pygame.camera.Camera(camlist[0], (640, 480))
    
        # opening the camera
        cam.start()
    
        # capturing the single image
        image = cam.get_image()
    
        # saving the image
        pygame.image.save(image, "test.jpg")
    
    # if camera is not detected the moving to else part
    else:
        print("No camera on current device")

if __name__ == '__main__':
    me = input("Access Webcame?: ")
    if me[-1] == 'y':
        # initializing  the camera
        pygame.camera.init()
        camlist = pygame.camera.list_cameras()
        if camlist:
            cam = pygame.camera.Camera(camlist[0], (640, 480))
            cam.start()
        else:
            print("No camera on current device")
    else:
        print('Please give us the access to webcam')
    start_client()
