const fs = require("fs");
const content = fs.readFileSync("README.md", "utf-8");
const match = content.match(/(\d+\.\d+)\s*%/);

if (match) {
  const percentage = parseFloat(match[1]);
  console.log(percentage); 
} else {
  console.error("Percentage not found in README.md");
  process.exit(1);
}
