const { app, BrowserWindow, ipcMain, screen } = require('electron');
const path = require('path');
const Database = require('better-sqlite3');

// 初始化数据库
const db = new Database(path.join(app.getPath('userData'), 'prompts.db'));
db.prepare(`
  CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
`).run();

// 创建悬浮窗
function createFloatingWindow() {
  const { width: screenWidth, height: screenHeight } = screen.getPrimaryDisplay().workAreaSize;
  
  const floatingWindow = new BrowserWindow({
    width: 60,
    height: 60,
    x: screenWidth - 100,
    y: screenHeight - 100,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    skipTaskbar: true,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true
    }
  });

  floatingWindow.loadFile('floating.html');
  
  // 监听渲染进程请求
  ipcMain.on('get-prompts', (event) => {
    const prompts = db.prepare('SELECT * FROM prompts').all();
    event.reply('prompts-data', prompts);
  });
  
  ipcMain.on('copy-to-clipboard', (event, text) => {
    clipboard.writeText(text);
    event.reply('copy-success');
  });
  
  return floatingWindow;
}

app.whenReady().then(() => {
  createFloatingWindow();
  
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createFloatingWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});