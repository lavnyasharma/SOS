import { React, useState, useEffect } from "react";
import "../../../css/LikedItems.css";
import { useHistory } from "react-router-dom";
import { HeartIcon } from "../../footer/ico";

function HeadBar(props) {
  const history = useHistory();

  // back button
  const backHandel = () => {
    history.goBack();
  };
  const Icon = props.icon;
  return (
    <div className="header">
      <div className="small-part head-display-svg"
      onClick={()=>{
          if (props.back) {
            backHandel();
          }
      }}>
        <Icon />
      </div>
      <div className="big-part">
        <div className="head-wrapper">
          <div className="head-input">{props.name}</div>
        </div>
      </div>
      <div className="small-part-2"></div>
    </div>
  );
}
const ResultItem = (props) => {
  return (
    <div className="result-item ">
      <div
        className="result-child"
        style={{ backgroundColor: props.color }}
      ></div>
    </div>
  );
};
const Body = () => {
  return (
    <div className="body">
      <ResultItem color="pink" />
    </div>
  );
};

function LikedItem() {
  const [height, setHeight] = useState(window.innerHeight - 58 - 0.6 * 16);
  useEffect(() => {
    window.addEventListener("resize", () => {
      setHeight(window.innerHeight - 58 - 0.6 * 16);
    });
    document.title = "Liked Items";
  }, []);
  return (
    <div className="Liked-Main">
      <HeadBar name="Liked items" icon={HeartIcon} back={false} />
      <div className="head small-title-font">
        <span></span>
      </div>
      <div className="li-main" style={{ height: height }}>
        <Body />
      </div>
    </div>
  );
}

export { LikedItem, HeadBar };
