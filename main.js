// Get html elements
const fileSelector = document.querySelector("#teeth-photos");
const submit_button = document.querySelector("#submit")
const preview = document.querySelector(".preview")
const email = document.querySelector("#email")
const painRadioButtons = document.querySelectorAll('input[name="pain"]')
const freqRadioButtons = document.querySelectorAll('input[name="freq"]')

const MINFILESIZE = 50 //prob corrupted or extremely poor resolution file - exact value to be determined based on clinical practise data
const MAXFILESIZE = 1e9 // to address denail of service attacks - exact value to be determined later
const KB = 1024
const emailRegex = /^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-z]+$/


const SERVERURL = "http://localhost:8000"



function arrayBufferToBase64(arrBuffer) {

  //convert to uint8 since arrayBuffer is generic binary buffer
  const uint8Buffer = new Uint8Array(arrBuffer)

  //convert each byte to string from specified utf-16 code units
  let binary = '';

  uint8Buffer.forEach((byte) => { binary += String.fromCharCode(byte) });

  //craetes a Base64-encoded ASCII string from binary string (= string whose characters are treated as binary data)
  return window.btoa(binary)

}


class ImagesCollection {

  constructor() {
    this.imageList = []
    this.imageBytes = []
    this.imageFileNames = []
  }


  async getByteImages() {


    for (let file of this.imageList) {
      let arrBuffer = await file.arrayBuffer()
      /*
      ArrayBuffer is not a JSON-compatible structure: JSON itself cannot directly serialize ArrayBuffer (or binary data). 
      Binary data needs to be either encoded (e.g., with Base64 encoding) or transmitted as part of a multipart form (multipart/form-data).
      */
      this.imageBytes.push(arrayBufferToBase64(arrBuffer))
    }
    return this.imageBytes 
  }


  getFileNames() {


    this.imageList.forEach((file) => this.imageFileNames.push(file.name))

    return this.imageFileNames

  }

  addImage(image){

    return this.imageList.push(image)
  }


}

const imageList = new ImagesCollection()


const isOkFile = (file) => {

  if (file.size > MINFILESIZE && file.size < MAXFILESIZE) {
    return true
  }
  else {
    return false
  }
}



const getSize = (item) => {

  if (item < KB) {
    return `${item} Bytes`
  }
  else if (item < 1e6) {
    return `${Math.round((item / 1e3) * 10) / 10} KBytes`
  }
  else if (item < 1e9) {
    return `${Math.round((item / 1e6) * 10) / 10} MBytes`

  }
}


function getSelectedValue(attribute) {
  const selectedRadio = document.querySelector(`input[name="${attribute}"]:checked`);

  if (selectedRadio) {
    const selectedValue = selectedRadio.value;
    return selectedValue
  } else {
    return false
  }
}





submit_button.addEventListener('click', async (event) => {

  if (!is_ready_submit()) {
    return
  }
  else {

    try {
      let images = await imageList.getByteImages()


      let postObj = { "email": email.value, "filenames": imageList.getFileNames(), "images": images }
      event.preventDefault()
      let response = await axios.post(`${SERVERURL}/upload`, postObj, {
        headers: {
          "Content-Type": "application/json"
        }
      });

      console.log(response.data);


    } catch (error) {
      console.error(error);
    }


  }

})


function is_ready_submit() {
  // Checks that the 4 items necessary for the request are there:
  // email
  // images
  // questionnaire response to pain
  // questionnaire response to last visit
  if (emailRegex.test(email.value) && (fileSelector.files.length != 0) && (getSelectedValue("pain")) && (getSelectedValue("freq"))) {
    console.log("All fields ready")
    submit_button.disabled = false
    return true

  }
  else {
    console.log("Missing fields")
    submit_button.disabled = true
    return false
  }


}


function addFormisteners() {

  painRadioButtons.forEach(radio => radio.addEventListener('change', async () => is_ready_submit()))
  freqRadioButtons.forEach(radio => radio.addEventListener('change', async () => is_ready_submit()))

  email.addEventListener('change', async () => is_ready_submit())

}


addFormisteners()


fileSelector.addEventListener('change', async (event) => {


  // Tasks to manage while there are changes in the fileSelctor
  // 1. Get FileList
  console.log("Change in fileSelector detected with file objects", fileSelector.files)

  for (let file of fileSelector.files) {
    if (isOkFile(file)) {
      imageList.addImage(file)
      showPreview()
      is_ready_submit()
    }

  }



  function showPreview() {

    // Creates a list of photos to be showin in the preview
    preview.innerHTML = ''

    for (let file of imageList.imageList) {

      console.log("Looping through :", file)
      let newItem = document.createElement("item")
      newItem.className = "item"

      let img = document.createElement("img");
      img.className = "item-el"
      img.src = URL.createObjectURL(file);

      img.onload = () => {
        console.log("Onload", img.naturalHeight, img.naturalWidth)
      }
      newItem.appendChild(img)
      preview.append(newItem)
    }
  }
});

