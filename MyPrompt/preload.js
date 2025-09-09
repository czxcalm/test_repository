const { contextBridge, ipcRenderer, clipboard } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getPrompts: () => ipcRenderer.send('get-prompts'),
  onPromptsData: (callback) => ipcRenderer.on('prompts-data', callback),
  copyToClipboard: (text) => {
    clipboard.writeText(text);
    return true;
  }
});