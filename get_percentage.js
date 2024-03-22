const fs = require('fs');

// Read the content of README.md
const content = fs.readFileSync('README.md', 'utf-8');

// Define a regular expression to match the percentage value
const regex = /(\d+\.\d+)\s*%/;

// Match the percentage value in the content
const match = content.match(regex);

// Check if a match is found
if (match) {
    // Extract the percentage value
    const percentage = parseFloat(match[1]);
    console.log(percentage);
} else {
    console.log('Percentage not found in README.md');
}
