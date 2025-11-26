This is the document where we will explain how Practice 01 was done.

We will start by saying that we did not use AI to do the exercises, however we used it as an investigative tool about docker. 
We did not work with dockers before and we did not understand what they were, and how to do correctly their build configuration, so that is what we learnt with chatGPT. 
It told us that in order to create a docker we need a dockerfile file, and a requirements file. 
From previous subjects we already knew what a requirements file was, but we did not know what a dockerfile was, so we searched an example on the internet (https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/) and modified it according to what we wanted on the image. 
On our github repository we have a lot of files, but we do not want all of them for the docker, we want:
- the first_seminar.py file
- the api.py file
- the requirements.txt file
- the folder of example images
- the folder where modified images are saved

In addition, we decided to use FastAPI,so we had to expose port 8000, since it works on that one.
And lastly we had to write the CMD command that will create the docker with this configuration.

There were a couple of extra files that chatGPT said they were useful. One was the .dockerignore,and since it is very similar to a .gitignore we knew how to do it and what to add, and the other one was a docker-compose.yml, which was actually the last step on practice 01. 
Since docker compose allowed us to modify the first_seminar.py and api.py files without having to build and rebuild the image, we decided to implement it first, that way, if something was not working as expected, we could stop the image, edit the file where the error was found, and run it again with just <<docker-compose up>>.
Now let us explain file per file.

FIRST_SEMINAR.PY file
This file corresponds to the .py and compatible version with FastAPI of first_seminar.ipynb, which was our notebook from the first seminar. We barely had to modify anything in order to make it compatible, just define the classes and copy the functions inside. We realized that we had a couple of useless lines in our original notebook and we had an error on the serpentine function, and we took some time to improve and clean a little bit the code.

Once that was done, we started with the api.py file, which is the file that runs the API. 
API.PY file
We have never worked with API, so we tried to follow this tutorial: https://fastapi.tiangolo.com/tutorial/first-steps/
with this we knew how to originally define the functions, and we knew that inside each function we had to call the corresponding one of the first_seminar.py. 
We first found out how to get the image, that is by simply using UploadFiles and Files. (https://fastapi.tiangolo.com/tutorial/request-files/#import-file), since we have our images folder, the teacher (or any user) can select the images from that folder.
Then, the last think to know was how to return images and save them onto the result_images folder, and for that we used the answer to this discussion in stackoverflow(https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi).

So that is all for this project. We decided to just create the endpoints for the serpentine pattern reading and converting the image into grayscale because they were the 2 functions that did not require any extra parameters apart from input_file and output_file. 

* Author's notes: 
1. Nahia has had a family emergency but she has been as participant as possible.
2. On github you will find that there are a lot of commits that are related to Streamlit. 
This is due to the fact that at first we wanted to use Streamlit as an API because we were familiar with it, but actually found out that it is not an API but an UI, so although we could do this project, it would not be in the way the teacher said.
So we then tried to use both, Streamlit as the website that the user uses, with everything styled and with even an image displayer, and fastAPI as the API that ran below it, meaning that you would select a processing operation on the web (i.e. serpentine), and streamlit would call the fastapi function that was related to that operation. 
However, we were having some errors and we thought it was too confusing, so we finally decided to use only fastAPI, even though it was more simple and less User-Experience enhanced.
