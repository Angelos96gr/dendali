<b>Dental health assessment</b>

- Upload photo
- If quality check is passed, photo is processed using AI.
- A health assessment report is sent to the email of the user with info about the general health of the teeth and potential emergency situation
- A list of nearby dentists is provided to followup an appointment




<b>Features</b>

- Client side validation- We check that the uploaded file(s):
    1. is image type (.jpeg, .png)
    2. has certain size i.e., huge files are dropped to avoid DOS and very small files are probably corrupted or very low quality.

- Secure client to server communication - We encyrpt transferred data provided by the user such 
as email and the uploaded image data.

- Server side validation and archiving - We check that the received information is correct:
    1. The provided images are not blurred, have the expected histogram and can eventually be processed to make the diagnosis. The accepted images are stored under the users credentials.
    2. The email of the user is verified
    3. Send status update to client about progress and if everything went fine.


- AI-based assessment. The AI-models have been trained based on dental images annotated by clinical experts. The uploaded images are processed to determine the dental health of the user.
A report is sent to the user's email.



<b>Getting</b>

To work with this repo you need to:

1. Setup the backend i.e., start the server. You can do that by running `./backend_startup.sh`. This activates the virtual environment, install dependencies and starts server

2. Interact with frontend. You can start the the frontend using different ways. Easiest is probably with a left-clicking on <i>dental_assessment_webpage</i> and selecting 'Open with live server'


For contributions:
1. create a branch e.g., `git checkout -b <branch_name>` e.g., `git checkout-b j1/processing-pipeline`
2. make any changes (note: any changes are automatically put into effect i.e., you dont need to take the frontend down and then up again). For changes in backend, you might need to restart backend server.
3. add changes you want to keep `git add <filename>`
4. commit changes with message `git commit -m <my_message>`
5. create pull request `git push origin <branch_name>`