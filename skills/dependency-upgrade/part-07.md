## Breaking Change Handling

### Identifying Breaking Changes

```bash
# Check the changelog directly
curl https://raw.githubusercontent.com/facebook/react/master/CHANGELOG.md
```

### Codemod for Automated Fixes

```bash
# Run jscodeshift with transform URL
npx jscodeshift -t <transform-url> <path>

# Example: Rename unsafe lifecycle methods
npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/rename-unsafe-lifecycles.js src/

# For TypeScript files
npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/rename-unsafe-lifecycles.js --parser=tsx src/

# Dry run to preview changes
npx jscodeshift -t https://raw.githubusercontent.com/reactjs/react-codemod/master/transforms/rename-unsafe-lifecycles.js --dry src/
```

### Custom Migration Script

```javascript
// migration-script.js
const fs = require("fs");
const glob = require("glob");

glob("src/**/*.tsx", (err, files) => {
  files.forEach((file) => {
    let content = fs.readFileSync(file, "utf8");

    // Replace old API with new API
    content = content.replace(
      /componentWillMount/g,
      "UNSAFE_componentWillMount",
    );

    // Update imports
    content = content.replace(
      /import { Component } from 'react'/g,
      "import React, { Component } from 'react'",
    );

    fs.writeFileSync(file, content);
  });
});
```
