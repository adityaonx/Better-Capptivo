const fs = require('fs');
console.log("Size:", fs.statSync('public/mockups/macbook.png').size);
