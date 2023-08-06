# Facial Expression Recognizer

Give the function an input and it will return a dictionary of detected faces and expression predictions.


---

## About

This is a python3 cli for Facial Expression Recognition (FER) using Keras and OpenCV.

This project uses the [haarcascade](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml) xml for facial detection.

We recommend using [our model](https://storage.googleapis.com/id-public-read/model.h5) for this application, but you may use your own as well. This project could be easily modified to do other types of object detection if you wish.

If you fork this project, please contribute back with any fixes or features the community may find useful. All PRs will go through a member of our Engineering team.

Please follow GitHub's template for bug reporting.

---

## Install
*Note this requires the installation of Tensorflow 2+*
### Using pip

`$ pip3 install fer-capture`

### From source

`$ git clone git@github.com:IntrospectData/id-fer-capture.git`

`$ python3 -m venv env`

`$ source env/bin/activate`

`(env) $ pip3 install id-fer-capture`
  - To include tensorflow:
      - `id-fer_capture[cpu]` for cpu based tensorflow
      - `id-fer_capture[gpu]` for gpu based tensorflow
---

## Use:


```python3
>>> from fer_capture.main import check_stream
>>> from fer_capture.main import check_image
>>> check_stream("/mnt/storage/face_test.mp4")
    [{'faces': {...}}, ...]
>>> check_image("/mnt/storage/face.jpeg")
    {'faces': {...}}
```
Append the argument `show=True` to either function to have a window display. You can press/hold any key for the frame to update in this mode.
