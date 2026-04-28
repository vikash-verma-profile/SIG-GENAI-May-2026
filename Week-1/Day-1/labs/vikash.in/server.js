const path = require("path");
const express = require("express");

const app = express();

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.render("pages/home", { title: "Vikash — Home", active: "home" });
});

app.get("/about", (req, res) => {
  res.render("pages/about", { title: "Vikash — About", active: "about" });
});

app.get("/contact", (req, res) => {
  res.render("pages/contact", {
    title: "Vikash — Contact",
    active: "contact",
    sent: false,
    name: "",
  });
});

app.post("/contact", (req, res) => {
  const name = typeof req.body?.name === "string" ? req.body.name.trim() : "";
  res.render("pages/contact", {
    title: "Vikash — Contact",
    active: "contact",
    sent: true,
    name,
  });
});

const port = Number(process.env.PORT) || 3000;
app.listen(port, () => {
  // eslint-disable-next-line no-console
  console.log(`vikash.in running on http://localhost:${port}`);
});

