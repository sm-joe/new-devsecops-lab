const test = require("node:test");
const assert = require("node:assert/strict");

test("application metadata is correct", () => {
  const application = {
    name: "new-devsecops-lab",
    status: "healthy"
  };

  assert.equal(application.name, "new-devsecops-lab");
  assert.equal(application.status, "healthy");
});