# UI

## Considerations
#### Babel vs Vite SWC
Chose Babel as the React compiler due to its portability to older browsers and strong community of plugins for future customization. SWC is faster, but from my experience, Babel is fine for most UI applications.

## Setup Instructions
### Environment Setup
1. Install [Node.js](https://nodejs.org/en/download)
2. Install [Vite](https://vite.dev/guide/#manual-installation)

### Building and Running
1. Install UI dependencies
    ```
    cd ui
    npm install
    ```
2. Run application using ```npx vite```
3. Open the application using the URL: ```http://localhost:5173/```


### IDE Setup
We use Visual Studio Code (VS Code) as our IDE for development. Open the project root in VS Code.

Set up automatic linting in your IDE:

1. In the VS Code marketplace, install [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) and [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode).

2. Make sure that the **Code Actions on Save** configuraiton in **Settings** is configured as such:
    ```js
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": true // automatically fix basic lint after file save
    },
    ...
    "eslint.validate": [
        "typescript",
        "typescriptreact"
    ]
    ...
    ```