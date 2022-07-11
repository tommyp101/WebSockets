# WebSockets
Getting familiar working with websockets. How to use and implement them.

$ pip install websockets

https://websockets.readthedocs.io/en/stable/


This progam creates a connect 4 game that allows multiple users to join from different browsers and internet connections.

In the first stage, I created a websocket that connects the browser to the server and vice versa.  The game starts when the server and the browser both connect to the websockets.  The browser interacts with the server by sending and receiving objects in JSON format.  The browser sends the input from the user through the browswer by "click" events that then analyzes the event to see what "type" to send to the server.  The server then uses the "type" to analyze what kind of action to send back to the browser in which the browser will update the frontend based on what the server's handler updated.  