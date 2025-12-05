This is a small report for the last part of this project. 

We did not use AI to improve our code, however, we did use it to do the unit tests for the api. 

We got some errors that were easy to solve, however we got some others that were very hard, and we needed the help of AI to solve them.

Turns out that they were not actually errors.

When you run the tests you will see that "video_info" and create_BBBcontainer" raise an error. 
This is due to the fact that both endpoints use audio information. 
  - For video info one of the things we return is the audio codec
  - And for the BBB container we encode the audio in AAC, MP3 or/and AC3, depending on what the user chose.

However, the test that the AI has created does not have any audio, therefore on the CMD we see an error of "list index out of bounds" for the video info, (since video_info stores on index0 the video and on index1 the audio), and on the BBB container we see an error of ffmpeg because it cannot take and covnert the audio of a video that does not have audio.


But we have tested all of the endpoints manually with the website (since it is more intuitive) and we did not get any error, therefore we believe that everything is working as it should be.

