function turnDarkOn(dark) {
  
  var r = document.querySelector(":root");
  var rs = getComputedStyle(r);
  r.style.setProperty(
    "--background",
    dark ? rs.getPropertyValue("--Dbackground") : "#fff"
  );
  r.style.setProperty(
    "--BoxMajor",
    dark ? rs.getPropertyValue("--DBoxMajor") : "#444444"
  );
  r.style.setProperty(
    "--BoxMinor",
    dark ? rs.getPropertyValue("--DBoxMinor") : "#fff"
  );
  r.style.setProperty(
    "--FontMajor",
    dark ? rs.getPropertyValue("--DFontMajor") : "#444444"
  );
  r.style.setProperty(
    "--FontMinor",
    dark ? rs.getPropertyValue("--DFontMinor") : "#868686"
  );
  r.style.setProperty(
    "--nav-bg-color",
    dark ? rs.getPropertyValue("--Dnav-bg-color") : "#fff"
  );
  r.style.setProperty(
    "--searchbar",
    dark ? rs.getPropertyValue("--Dsearchbar") : "rgba(143, 209, 192, 0.11)"
  );
  r.style.setProperty(
    "--active",
    dark ? rs.getPropertyValue("--Dactive") : "#2d96f8"
  );
  r.style.setProperty(
    "--searchbar-focus",
    dark
      ? rs.getPropertyValue("--Dsearchbar-focus")
      : "rgba(143, 209, 193, 0.349)"
  );
  r.style.setProperty(
    "--placeholder",
    dark ? rs.getPropertyValue("--Dplaceholder") : "#9b9b9b"
  );
  r.style.setProperty(
    "--active-text",
    dark ? rs.getPropertyValue("--Dactive-text") : "#fff"
  );
  r.style.setProperty(
    "--setting-item-background",
    dark ? rs.getPropertyValue("--Dsetting-item-background") : "#f2f2f283"
  );
  r.style.setProperty(
    "--df-hf",
    dark ? rs.getPropertyValue("--Ddf-hf") : "rgba(143, 209, 192, 0.11)"
  );
  document
    .querySelector('meta[name="theme-color"]')
    .setAttribute(
      "content",
      dark ? rs.getPropertyValue("--Dbackground") : "#fff"
    );
}



const detectmedia = () => {
    console.log("detect media");
    if (localStorage.getItem("darkmodechoice") === "true") {
      const darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)");
      if (darkThemeMq.matches) {
        turnDarkOn(true);
      } else {
        turnDarkOn(false);
      }
    } else {
      const dark = localStorage.getItem("dark");
      if (dark === "true") {
        console.log("dark");
        turnDarkOn(true);
      }else{
        console.log("light");
        turnDarkOn(false);
      }
    }
  };

export { turnDarkOn, detectmedia };
