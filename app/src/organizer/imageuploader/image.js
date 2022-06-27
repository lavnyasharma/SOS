import React, { useRef, useState } from "react";
import Cropper from "react-cropper";
import "cropperjs/dist/cropper.css";
import "../../css/image.css";
import { useHistory } from "react-router-dom";
import { Uploadimage } from "./ico";
const Demo = () => {
  const history = useHistory();
  const cropperRef = useRef(null);
  const [src, setSrc] = useState(null);

  const [cropResult, setCropResult] = useState(null);
  const onCrop = () => {
    const imageElement = cropperRef.current;
    const cropper = imageElement.cropper;
    setCropResult(cropper.getData());
    var image = new Image();
    image.id = "pic";
    image.className = "img";
    image.onclick = () => {
      document.getElementById("cpr").style.display = "block";
    };
    image.src = cropper.getCroppedCanvas().toDataURL();
    document.getElementById("result").innerHTML = "";
    document.getElementById("result").appendChild(image);
  };
  return (
    <>
      <div
        style={{
          height: "100%",
          width: "100%",
        }}
        id="image-cropper"
        className="image-main"
      >
        <div className="head">
          <div className="parts">
            <div
              className="back"
              onClick={() => {
                history.goBack();
              }}
            >
              back
            </div>
          </div>
          <div className="parts"></div>
          <div className="parts"></div>
          <div className="parts">
            <button className="back" onClick={onCrop}>
              upload
            </button>
          </div>
        </div>
        <div className="image-body">
          <div class="image-upload" id="upldbtn">
            <span>Import from device</span>

            <input
              type="file"
              onChangeCapture={(e) => {
                const file = e.target.files[0];
                const imageSrc = URL.createObjectURL(file);
                setSrc(imageSrc);
                document.getElementById("cpr").style.display = "block";
                document.getElementById("upldbtn").style.display = "none";
              }}
            />
          </div>
          <div className="result-wrapper">
            <div class="cropped-result" id="result"></div>
          </div>
        </div>
      </div>
      <div id="cpr" class="crpr" style={{ display: "none", zIndex: "9999" }}>
        <div
          className="close"
          onClick={() => {
            document.getElementById("cpr").style.display = "none";
            document.getElementById("upldbtn").style.display = "flex";
          }}
        >
          Close
        </div>
        <div
          className="crop"
          onClick={() => {
            document.getElementById("cpr").style.display = "none";
            onCrop();
          }}
        >
          Crop
        </div>
        <Cropper
          src={src}
          style={{
            height: 600,
            width: "auto",

            zIndex: "9999",
          }}
          
          resizable={true}
          guides={true}
          rotatable={true}
          dragMode="move"
          cropBoxMovable={true}
          zoomable={false}
          responsive={true}
          viewMode={1}
          movable={false}
          ref={cropperRef}
          highlight={true}
          background={false}
          modal={false}
          boxcolor="#fff"
        />
      </div>
    </>
  );
};

export default Demo;
