# XR-Object-Quest3

There are three main codes that should be explained. These are object_recognition_server.py, AutoRaycast.cs and ObjectReceiver.cs. For the last two codes, you can find them from Assets/Raycast folder.

In the object_recognition_server.py code, YOLO object detection model is used to detect the objects. Before running this code, there should be made some adjustments. In the 29th and 69th lines of the code, you have to change the screen resolution according to your computer resolution. Also, in the 54th line of the code, you have to change the IP address so that you can send the object information to Unity.

In the ObjectReceiver.cs code, the only change you must do is that changing the IP address in the 18th line of the code. Both of the IP addresses must be same.

In the AutoRaycast.cs code, again you have to adjust screen resolution in 202nd and 203rd line of the code. Since we are using Meta Casting app to detect the objects and its resolution is 1280x720, we have used these information in these lines of the code too.

In our Python code, we are capturing our laptop screen, so to see the Quest3's video, we are using Meta Casting. The user must open the Meta Casting in the fullscreen after running the Python code.

To start the application, firstly one has to run the Python code, after that one should open the application from Quest3. Python automatically connects with Unity and starts sending object coordinates.


