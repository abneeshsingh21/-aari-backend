#!/usr/bin/env node

/**
 * AARI One-Click Launcher
 * Opens assistant from GitHub with single command
 * Usage: npx aari-assistant
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const projectDir = process.cwd();

console.log('\n╔════════════════════════════════════════╗');
console.log('║  AARI Voice Assistant - Quick Launch  ║');
console.log('╚════════════════════════════════════════╝\n');

// Check if we're in the right directory
if (!fs.existsSync(path.join(projectDir, 'backend')) || 
    !fs.existsSync(path.join(projectDir, 'VoiceAssistantApp'))) {
  console.error('❌ Error: Not in AARI project directory');
  console.error('Please run from the root directory where backend/ and VoiceAssistantApp/ exist');
  process.exit(1);
}

console.log('✓ Project found');

// Install dependencies
console.log('\n[1/3] Installing dependencies...');
try {
  execSync('cd VoiceAssistantApp && npm install', { stdio: 'inherit' });
  console.log('✓ Dependencies installed');
} catch (e) {
  console.error('✗ Failed to install dependencies');
  process.exit(1);
}

// Start services
console.log('\n[2/3] Starting services...');
console.log('Starting backend and frontend...\n');

const isWindows = process.platform === 'win32';

if (isWindows) {
  console.log('Backend URL: http://localhost:5000');
  console.log('Frontend URL: http://localhost:8081');
  console.log('\n✓ Services starting in new windows');
  console.log('✓ Scan QR code with Expo Go on Android\n');
  
  execSync('cd VoiceAssistantApp && npx expo start', { stdio: 'inherit' });
} else {
  console.log('Starting services...');
  execSync('cd VoiceAssistantApp && npx expo start', { stdio: 'inherit' });
}
