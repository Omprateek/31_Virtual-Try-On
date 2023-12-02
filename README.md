# Virtual Try-On App

## Setup

1. Install the required Python packages:

   ```bash
   pip install flask opencv-python mediapipe
   ```
   
## How to Run

Execute the following command in the terminal:

```bash
python app.py
```markdown

## File Structure

- **app.py**: Contains the Flask web application and integrates hand tracking to overlay a virtual accessory (watch) on the user's hand in real-time.
- **templates/index.html**: HTML template for the user interface.
- **assets/Watch3.png**: Image of the virtual accessory (watch) with a transparent background.

## Dependencies

- Flask: Web framework for Python.
- OpenCV: Library for computer vision tasks.
- MediaPipe: Framework for building multimodal applied machine learning solutions.

## Usage

1. Run the application using `python app.py`.
2. Open a web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).
3. Move your hand in front of the webcam to see the virtual accessory (watch) overlay on your hand in real-time.
4. Click the "Full Screen" button to enter or exit full-screen mode.

## Credits

- [Flask](https://flask.palletsprojects.com/): Web framework for Python.
- [OpenCV](https://opencv.org/): Library for computer vision tasks.
- [MediaPipe](https://mediapipe.dev/): Framework for building multimodal applied machine learning solutions.
- [Bootstrap](https://getbootstrap.com/): Front-end component library.

