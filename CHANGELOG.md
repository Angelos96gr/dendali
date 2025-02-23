15 Dec 2024:

- Initial commit with basic functionality for uploading and viewing photo



12 Jan 2025:

- Frontend:
    - Can support sending image data to server using axios
- Setup backend
    - Can receive uploaded images on the client side as byte stream (both as raw byte and form/file data)
    - Saves the uploaded images locally

18 Jan 2025:
- Frontend
    - Submit button ui (disabling by default until all info is there)
    - Updated axios request to include email, filename and base64 encoded binary data
- Backend
    - Receive updated request structure
    - Create unique folder for each user & saved images by filename

9 Feb 2025:
 - Backend server startup

 23 Feb 2025:
 - Frontend
    - Add questionnaires
    - Size checks
    - Email validation
    - Client side validation that all entered fields are filled in
    - General refactoring with reusable checks
    - Verified requests structure is as intended
- Backend
    - Storing directories based on users email and datetime
    - Image checks after saving successful - Verification of encoding steps in frontend and decoding in backend
    - Supports sending verification of email for gmail users (tbd if used at the end)






ToDo
- Allow diselecting photos
- Unresponived page in case of server down
- datamodels
- testing of encoding steps
- encrypt images - check https
- more advanced security checks - sanitize file content validation (security checks)