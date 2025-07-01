---
title: "Ethereum toolkit integration with browser (hardhat + solc-js)"
date: 2025-01-21
categories: [eth0-rag]
tags: [ethereum, ai, rag, brainstorming, hackathon, development]

# Turn off any right‐side elements you don’t want
author_profile: false
related: false
share: false
toc: false

sidebar:
  nav: "categories"
classes: "wide"
---

Given your goal of **getting a working prototype today**, I recommend starting with **Hardhat + solc-js**, as it's **easier to integrate in a decentralized manner**, runs directly in the browser with WebAssembly (WASM), and doesn’t require additional infrastructure like server-side APIs for compilation.

Once the prototype is up and running, you can explore integrating **Foundry** later for advanced features like fuzz testing and performance optimization.

---

### **Step-by-Step Lean Toolkit Integration Plan (Hardhat + solc-js)**

#### **1. High-Level Overview**
1. Use **CodeMirror** for the front-end code editor (which you already have).
2. Integrate **solc-js** for in-browser Solidity compilation.
3. Set up basic **project templates** (ERC20, ERC721) for quick deployment.
4. Deploy contracts using **ethers.js** and connect to MetaMask.
5. Create a simple **output console** to show compilation and deployment results.
6. Later, extend with Hardhat for advanced dev flow (testing, debugging).

---

### **2. Toolkit Selection**
We will start with:

- **Frontend:** `CodeMirror` (already in your app).
- **Compilation:** `solc-js` (browser-based, avoids server costs).
- **Deployment:** `ethers.js` (to interact with Ethereum network).
- **Wallet Connection:** MetaMask.
- **File Handling:** LocalStorage or IndexedDB for persistence.

---

### **3. Implementation Plan (Tasks & Commands)**

#### **A. Set Up the Dependencies**
1. Install required packages:
   ```bash
   npm install solc ethers codemirror
   ```

2. Import them in your frontend app:
   ```javascript
   import solc from 'solc';
   import { ethers } from 'ethers';
   import CodeMirror from 'codemirror';
   import 'codemirror/mode/javascript/javascript';
   ```

---

#### **B. Add Solidity Code Editor**
Modify your existing CodeMirror implementation to support Solidity:

```html
<textarea id="editor"></textarea>

<script>
  const editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
      mode: "javascript",
      theme: "dracula",
      lineNumbers: true,
      value: `// Write your Solidity contract here\n` +
             `pragma solidity ^0.8.0;\n\n` +
             `contract MyContract {\n  uint256 public count;\n\n  function increment() public {\n    count++;\n  }\n}`,
  });
</script>
```

---

#### **C. Compile Solidity Code in the Browser**
Add a button to compile the Solidity code and show output:

```html
<button id="compile-btn">Compile</button>
<pre id="output"></pre>

<script>
  document.getElementById("compile-btn").addEventListener("click", async () => {
      const sourceCode = editor.getValue();
      const input = {
          language: 'Solidity',
          sources: {
              'contract.sol': { content: sourceCode }
          },
          settings: { outputSelection: { '*': { '*': ['abi', 'evm.bytecode'] } } }
      };

      const output = JSON.parse(solc.compile(JSON.stringify(input)));

      if (output.errors) {
          document.getElementById("output").innerText = output.errors.map(err => err.formattedMessage).join("\n");
      } else {
          const bytecode = output.contracts['contract.sol'].MyContract.evm.bytecode.object;
          const abi = output.contracts['contract.sol'].MyContract.abi;
          document.getElementById("output").innerText = "Compilation Successful! \n\n" + JSON.stringify(abi, null, 2);
          
          localStorage.setItem("compiledBytecode", bytecode);
          localStorage.setItem("contractABI", JSON.stringify(abi));
      }
  });
</script>
```

---

#### **D. Deploy Contract Using MetaMask and ethers.js**
Once compiled, deploy it directly to Ethereum testnet.

```html
<button id="deploy-btn">Deploy to Testnet</button>

<script>
  document.getElementById("deploy-btn").addEventListener("click", async () => {
      if (!window.ethereum) {
          alert("Please install MetaMask!");
          return;
      }

      const provider = new ethers.providers.Web3Provider(window.ethereum);
      await provider.send("eth_requestAccounts", []);

      const signer = provider.getSigner();
      const bytecode = localStorage.getItem("compiledBytecode");
      const abi = JSON.parse(localStorage.getItem("contractABI"));

      const factory = new ethers.ContractFactory(abi, bytecode, signer);
      document.getElementById("output").innerText = "Deploying...";

      try {
          const contract = await factory.deploy();
          await contract.deployed();
          document.getElementById("output").innerText = `Contract deployed at: ${contract.address}`;
      } catch (error) {
          document.getElementById("output").innerText = "Error: " + error.message;
      }
  });
</script>
```

---

#### **E. Store Projects in Browser Storage**
To allow users to save their work locally:

```javascript
document.getElementById("save-btn").addEventListener("click", () => {
    localStorage.setItem("savedContract", editor.getValue());
    alert("Contract saved!");
});

document.getElementById("load-btn").addEventListener("click", () => {
    const savedContract = localStorage.getItem("savedContract");
    if (savedContract) {
        editor.setValue(savedContract);
    } else {
        alert("No saved contract found.");
    }
});
```

---

### **4. UX Enhancements (To Make It Feel Like a True IDE)**
Once the core functionality is in place, add:

1. **Tab System:**  
   Allow users to open multiple Solidity files at once (use IndexedDB for persistence).

2. **Preset Templates:**  
   Add quick templates for common contracts (ERC20, ERC721, etc.).

3. **Compile Warnings Panel:**  
   Display warnings separately for better debugging experience.

4. **Dark Mode Support:**  
   Use a toggle for better developer experience.

---

### **5. Deployment Steps**
Once everything is working locally, deploy to production:

```bash
npm run build
```

1. Host it on **Vercel** or **GitHub Pages** for a quick demo.
2. Share the link with users to start experimenting.

---

### **6. Stretch Goals for Future Enhancements**
Once the basic features are done, consider:

- **Integrating Hardhat for local testing and deployment.**
- **Allowing Foundry integration (as API-based compilation).**
- **Adding a chat AI assistant to suggest improvements in code.**
- **Connecting with decentralized storage like IPFS for contract storage.**

---

### **7. Summary of Today's Plan**

1. **Set up the dependencies:** `solc-js, ethers.js, codemirror`.
2. **Add the Solidity editor with basic contract templates.**
3. **Compile Solidity code directly in the browser.**
4. **Deploy compiled contracts using MetaMask and ethers.js.**
5. **Enable saving/loading contracts locally.**
6. **Polish the UX with tabs, dark mode, and project templates.**
7. **Deploy the MVP and share for feedback.**

---

### **8. What You’ll Achieve Today**
By following this plan, you’ll have a **fully functional Ethereum IDE** capable of:

1. Writing Solidity code.
2. Compiling contracts in the browser.
3. Deploying them to Ethereum testnets.
4. Storing and managing project files locally.

---

If you're ready, start implementing and I’ll be here to troubleshoot any issues you run into. 🚀

[Written by GPT-4o]