# Face Webcam

## Depedencies

### Python

---

- face\_recognition
- pillow
- cv2
- numpy

### NPM

---

- express
- child\_process
- jpeg\-js
- socket.io

## What it does

Takes in images constantly from your webcam and processes it with the face\_recognition library. ( You can check it out from here [face\_recognition](https://github.com/ageitgey/face_recognition))
Then sends it to the node.js code in a form of a binary buffer. In the node.js code it changes the image data to a jpeg data format. The it passes it to the backend code, and to the front end code through socket.io which changes the images constantly on the web.

## How to download

```shell
git clone https://github.com/james0248/face_webcam.git
```
