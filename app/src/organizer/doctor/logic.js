import axiosInstance from "../../ax";
import { te, ts } from "../global/errbox";

async function getinfo(slug, setdata) {
  try {
    const response = await axiosInstance.post("doc/", {
      SLUG: slug,
    });
    if (response.status === 200) {
      setdata(response.data["data"]);
    } else {
    }
    return true;
  } catch (error) {
    console.log(error.response);
    te(error.response);
  }
}

async function getbatches(ofid, setdata) {
  try {
    const response = await axiosInstance.get("get/batch/" + ofid + "/", {});
    console.log(response.data.data.data);
    if (response.status === 200) {
      setdata(response.data.data.data);
    } else {
    }
    return true;
  } catch (error) {
    console.log(error.response);
    te(error.response);
  }
}

async function gettimings(bid, setdata) {
  try {
    const response = await axiosInstance.get(
      "get/batch/timing/" + bid + "/",
      {}
    );
    console.log(response.data.data);
    if (response.status === 200) {
      setdata(response.data.data);
    } else {
    }
    return true;
  } catch (error) {
    console.log(error);
  }
}

async function book(slug, batchid, time) {
  try {
    const response = await axiosInstance.post("book/", {
      slug: slug,
      batchid: batchid,
      time: time,
    });

    if (response.status === 200) {
      ts("appionment booked");
    } else {
    }
    return true;
  } catch (error) {
    te("error")
  }
}
export { getinfo, getbatches, gettimings, book };
