const express = require("express");
const cookieParser = require("cookie-parser");
const Tokens = require("csrf");

const app = express();
const port = process.env.PORT || 3000;
const tokens = new Tokens();

app.use(express.json());
app.use(cookieParser());

/*
 * CSRF protection
 *
 * Each client receives a unique CSRF secret in an HTTP-only cookie.
 * The client obtains a CSRF token from /api/csrf-token and sends it
 * back using the X-CSRF-Token header for state-changing requests.
 */
function getCsrfSecret(req, res) {
  let secret = req.cookies.csrfSecret;

  if (!secret) {
    secret = tokens.secretSync();

    res.cookie("csrfSecret", secret, {
      httpOnly: true,
      sameSite: "lax",
      secure: process.env.NODE_ENV === "production"
    });
  }

  return secret;
}

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
    application: "New DevSecOps Lab",
    version: "1.0.0"
  });
});

/*
 * Generate a CSRF token for the client.
 */
app.get("/api/csrf-token", (req, res) => {
  const secret = getCsrfSecret(req, res);
  const token = tokens.create(secret);

  res.json({
    csrfToken: token
  });
});

/*
 * Validate CSRF token for state-changing requests.
 */
app.use((req, res, next) => {
  const stateChangingMethods = ["POST", "PUT", "PATCH", "DELETE"];

  if (!stateChangingMethods.includes(req.method)) {
    return next();
  }

  const secret = req.cookies.csrfSecret;
  const token = req.get("X-CSRF-Token");

  if (!secret || !token || !tokens.verify(secret, token)) {
    return res.status(403).json({
      error: "Invalid or missing CSRF token"
    });
  }

  next();
});

app.post("/api/profile", (req, res) => {
  res.status(200).json({
    message: "Profile updated successfully",
    profile: req.body
  });
});

if (require.main === module) {
  app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
  });
}

module.exports = app;
