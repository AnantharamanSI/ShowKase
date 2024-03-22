import React, { useState } from 'react';
import './App.css';

const useCloudflareWorkers = true;
const workersURL = 'https://red-hill-1188.i-anantharaman-s.workers.dev/pdf?';

function App() {
  const [step, setStep] = useState(1);
  const [uploadedImageURLs, setUploadedImageURLs] = useState([]);
  const [images, setImages] = useState([]);
  const [masks, setMasks] = useState([]);
  const [formData, setFormData] = useState({
    bedrooms: 0,
    bathrooms: 0,
    city: '',
    state: '',
    price: '',
    sqFoot: '',
  });

  const handleFormChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    for (const key in formData) {
      if (!formData[key]) {
        // If any key has an empty value, return false
        return
      }
    }
    document.getElementById('submit-form').removeAttribute('disabled');

  };

  const handleImageUpload = (event) => {
    const files = event.target.files;
    const newImages = Array.from(files).map((file) => URL.createObjectURL(file));

    if (uploadedImageURLs.length + newImages.length > 1) {
      alert('You can only upload up to 1 images.');
      return;
    }

    setUploadedImageURLs((prevImages) => [...prevImages, ...newImages]);
    setImages((prevImages) => [...prevImages, ...Array.from(files)]);
  };

  const handleMoveForward = (e) => {
    e.preventDefault();
    // console.log('data', uploadedImageURLs, images)
    document.getElementById('cover-spin').style.display = "block";
    const js = {
      bed: parseInt(formData.bedrooms),
      bath: parseInt(formData.bathrooms),
      city: formData.city,
      state: formData.state,
      acre_lot: parseFloat(formData.sqFoot) / 430000,
      house_size: parseInt(formData.sqFoot),
      price: parseInt(formData.price),
    };

    const imageData = new FormData();
    // imageData.append('files', images);
    images.forEach((file, index) => {
      imageData.append(`file${index}`, file);
    });
    imageData.append('data', JSON.stringify(js))
    console.log('image data form', imageData)

    process_data(imageData).then((result) => {
      console.log('result:', result);
      document.getElementById('cover-spin').style.display = "";
      useCloudflareWorkers ? handleWorkers(result) : setStep(3);
    })
  };

  function handleWorkers(result) {
    const js = {
      'masks' : result["masks"],
    } 
    var url = workersURL;
    Object.entries(formData).forEach(([key, value]) => {
      if (value) { // Only append if value is not empty
        // convert value to string if it is a number
        if (typeof value === 'integer' || typeof value === 'float') {
          value = value.toString();
        }
        url = url.concat(key + "=" + value + "&");
        // console.log('url:', url);
      }
    });
    Object.entries(result["result"]).forEach(([key, value]) => {
      if (value) { // Only append if value is not empty
        // convert value to string if it is a number
        if (typeof value === 'integer' || typeof value === 'float' || typeof value == 'object') {
          value = value.toString();
        }
        url = url.concat(key + "=" + value + "&");
        // console.log('url:', url);
      }
    });
    Object.entries(js).forEach(([key, value]) => {
      if (value) { 
        if (typeof value === 'integer' || typeof value === 'float' || typeof value === "object") {
          value = value.toString();
        }
        url = url.concat(key + "=" + value + "&");
      }
    });
    // return url;
    window.location.href = url;
  }

  async function process_data(data) {
    const response = await fetch('/members', {
      method: 'POST',
      body: data,
      // headers: { 'Content-Type': 'multipart/form-data' },
    });
    const result = await response.json();
    return result
  }

  return (
    <div className="app">
      <header className="header">
        <div class="nice-large-bold">ShowKase</div>
        <div class="nice-small-bold">Your AI-powered Property Valuator</div>
      </header>

      <main className="main">
        <div className="container">
          <div className="wrapper">
            {step === 1 && (
              <div className="property-form">
                <div id="cover-spin"></div>
                <form onSubmit={handleMoveForward}>
                  <div class="form-container">
                    <div className="form-group">
                      <label htmlFor="bedrooms" class="fields">Bedrooms:</label>
                      <select
                        id="bedrooms"
                        name="bedrooms"
                        value={formData.bedrooms}
                        onChange={handleFormChange}>
                        <option value="none" selected hidden>None</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                      </select>
                    </div>
                    <div className="form-group">
                      <label htmlFor="bathrooms" class="fields">Bathrooms:</label>
                      <select
                        id="bathrooms"
                        name="bathrooms"
                        value={formData.bathrooms}
                        onChange={handleFormChange}>
                        <option value="none" selected hidden>None</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3</option>
                        <option value="4">4</option>
                      </select>
                    </div>
                  </div>
                  <div class="form-container">
                    <div className="form-group">
                      <label htmlFor="city" class="fields">City:</label>
                      <input
                        type="text"
                        id="city"
                        name="city"
                        value={formData.city}
                        onChange={handleFormChange}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlFor="state" className='fields'>State:</label>
                      <select
                        id="state"
                        name="state"
                        value={formData.state}
                        onChange={handleFormChange}>
                        <option value="none" selected hidden>None Selected</option>
                        <option value="Alabama">Alabama</option>
                        <option value="Alaska">Alaska</option>
                        <option value="Arizona">Arizona</option>
                        <option value="Arkansas">Arkansas</option>
                        <option value="California">California</option>
                        <option value="Colorado">Colorado</option>
                        <option value="Connecticut">Connecticut</option>
                        <option value="Delaware">Delaware</option>
                        <option value="Florida">Florida</option>
                        <option value="Georgia">Georgia</option>
                        <option value="Hawaii">Hawaii</option>
                        <option value="Idaho">Idaho</option>
                        <option value="Illinois">Illinois</option>
                        <option value="Indiana">Indiana</option>
                        <option value="Iowa">Iowa</option>
                        <option value="Kansas">Kansas</option>
                        <option value="Kentucky">Kentucky</option>
                        <option value="Louisiana">Louisiana</option>
                        <option value="Maine">Maine</option>
                        <option value="Maryland">Maryland</option>
                        <option value="Massachusetts">Massachusetts</option>
                        <option value="Michigan">Michigan</option>
                        <option value="Minnesota">Minnesota</option>
                        <option value="Mississippi">Mississippi</option>
                        <option value="Missouri">Missouri</option>
                        <option value="Montana">Montana</option>
                        <option value="Nebraska">Nebraska</option>
                        <option value="Nevada">Nevada</option>
                        <option value="New Hampshire">New Hampshire</option>
                        <option value="New Jersey">New Jersey</option>
                        <option value="New Mexico">New Mexico</option>
                        <option value="New York">New York</option>
                        <option value="North Carolina">North Carolina</option>
                        <option value="North Dakota">North Dakota</option>
                        <option value="Ohio">Ohio</option>
                        <option value="Oklahoma">Oklahoma</option>
                        <option value="Oregon">Oregon</option>
                        <option value="Pennsylvania">Pennsylvania</option>
                        <option value="Rhode Island">Rhode Island</option>
                        <option value="South Carolina">South Carolina</option>
                        <option value="South Dakota">South Dakota</option>
                        <option value="Tennessee">Tennessee</option>
                        <option value="Texas">Texas</option>
                        <option value="Utah">Utah</option>
                        <option value="Vermont">Vermont</option>
                        <option value="Virginia">Virginia</option>
                        <option value="Washington">Washington</option>
                        <option value="West Virginia">West Virginia</option>
                        <option value="Wisconsin">Wisconsin</option>
                        <option value="Wyoming">Wyoming</option>
                      </select>
                    </div>
                  </div>
                  <div class="form-container">
                    <div className="form-group">
                      <label htmlFor="price" class="fields">Price:</label>
                      <input
                        type="number"
                        id="price"
                        name="price"
                        min="50000"
                        max="5000000"
                        value={formData.price}
                        onChange={handleFormChange}
                      />
                    </div>
                    <div className="form-group">
                      <label htmlFor="sqFoot" class="fields">Sq. Foot:</label>
                      <input
                        type="number"
                        id="sqFoot"
                        name="sqFoot"
                        min="700"
                        max="3000"
                        value={formData.sqFoot}
                        onChange={handleFormChange}
                      />
                    </div>
                  </div>
                  <div class="form-container">
                    <div className="form-group">
                      <label htmlFor="images" class="fields">Upload Images:</label>
                      <div className="image-upload">
                        <input
                          type="file"
                          id="images"
                          name="images"
                          multiple
                          accept="image/*"
                          onChange={handleImageUpload}
                        />
                        {/* <button className="upload-button">
                        <i className="fas fa-upload"></i> Add Images
                      </button> */}
                      </div>
                      <div className="image-preview">
                        {uploadedImageURLs.map((imageUrl, index) => (
                          <div key={index} className="image-container">
                            <img src={imageUrl} alt={`Uploaded Image ${index + 1}`} />
                          </div>
                        ))}
                      </div>
                    </div>
                    <button class="submit-button" id="submit-form" type="submit" disabled="disabled">
                      Generate Report
                    </button>
                  </div>
                </form>
              </div>
            )}
            {step === 2 && (
              <div id="loading-bar-spinner" class="spinner"><div class="spinner-icon"></div></div>
            )}
            {step === 3 && (
              <div>
                <h1>Property Assessment Report</h1>
                <iframe
                  src="/gen_pdf"
                  type="application/pdf"
                  width="800px"
                  height="600px"
                ></iframe>
              </div>
            )}
          </div>
        </div>
      </main >
    </div >
  );
}

export default App;