Installation:

git clone https://github.com/philsr2/Websocket-experiments.git
cd Websocket-experiments/websockets-chat

# put chat.html where you like it
sudo cp chat.html /var/www/html/
python chat-server.py > log 2>&1 &

bring up http://your-ip/chat.html in your browser
type /nick YourNickname to change your nickname from a number.
chat...   

ToDo:

1. Make it remember the nickname.  I am not sure if a cookie will work across 
   multiple pages on the browser, but on different browsers/devices that's the 
   easiest way.
   Found a better way to do this at: 
https://www.xjavascript.com/blog/any-way-to-identify-browser-tab-in-javascript/#why-tab-identification-matters-key-use-cases
2. Persist the chat to a database.
3. Figure out image upload/storage/display.  Might use the Post bit from my first
   websockets webcam experiment.  AI suggested I use websockets to improve that.
  
