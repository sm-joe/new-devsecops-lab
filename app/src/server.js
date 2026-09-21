const express = require("express");

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    service: "new-devsecops-lab",
    status: "healthy"
  });
});

app.get("/health", (req, res) => {
  res.status(200).json({
    status: "ok"
  });
});

app.get("/api/info", (req, res) => {
  res.json({
    application: "DevSecOps Lab",
    version: "1.0.0"
  });
});

if (require.main === module) {
  app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
  });
}

module.exports = app;