import axiosInstance from "../../../ax";

async function getsosData(token, setData) {
  try {
    const response = await axiosInstance.post("guest/get/", {
      token: token,
    });
    console.log(response);
    if (response.status === 200) {
      console.log(response.data);
      setData(response.data);
    } else {
    }
    console.log(response.status);
  } catch (error) {}
}
async function getsosallData(setData) {
  try {
    const response = await axiosInstance.post("guest/all/", {});
    console.log(response);
    if (response.status === 200) {
      console.log(response.data.hh);
      setData(response.data.hh);
    } else {
    }
    console.log(response.status);
  } catch (error) {}
}

export { getsosData, getsosallData };
