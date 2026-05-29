#!/usr/bin/env node
/**
 * Web-Check 轻量 API 调用器
 * 直接调用 api/ 目录中的函数，绕过 Vite GUI 干扰
 * 用法: node web-check-cli.js <module> <url>
 * 模块: ip, dns, ssl, headers, tech, ports, cookies, location, redirects, subdomains, carbon
 */

import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const API_DIR = path.resolve(__dirname, '../repo/api');

const moduleName = process.argv[2];
const targetUrl = process.argv[3];

if (!moduleName || !targetUrl) {
  console.error('用法: node web-check-cli.js <模块> <域名>');
  console.error('模块: ip|dns|ssl|headers|tech|ports|cookies|location|security|redirects|subdomains|carbon|all');
  console.error('示例: node web-check-cli.js ip example.com');
  process.exit(1);
}

// 模块名映射
const MODULE_MAP = {
  'ip': 'get-ip',
  'dns': 'dns',
  'ssl': 'ssl',
  'headers': 'headers',
  'tech': 'tech-stack',
  'ports': 'ports',
  'cookies': 'cookies',
  'location': 'location',
  'security': 'http-security',
  'redirects': 'redirects',
  'subdomains': 'subdomains',
  'carbon': 'carbon',
  'screenshot': 'screenshot',
  'robots': 'robots-txt',
  'security-txt': 'security-txt',
};

const normalizeUrl = (url) => {
  return url.startsWith('http') ? url : `https://${url}`;
};

async function runModule(mod, url) {
  const filename = MODULE_MAP[mod];
  if (!filename) {
    console.error(`未知模块: ${mod}`);
    console.error(`可用: ${Object.keys(MODULE_MAP).join(', ')}`);
    process.exit(1);
  }

  const modPath = path.join(API_DIR, `${filename}.js`);
  try {
    const handlerModule = await import(modPath);
    const handler = handlerModule.default || handlerModule.handler;
    
    if (typeof handler === 'function') {
      const result = await handler(normalizeUrl(url));
      return { module: mod, result };
    } else {
      return { module: mod, error: 'handler not a function' };
    }
  } catch (e) {
    return { module: mod, error: e.message };
  }
}

async function main() {
  const url = normalizeUrl(targetUrl);
  
  if (moduleName === 'all') {
    const modules = Object.keys(MODULE_MAP);
    for (const mod of modules) {
      const res = await runModule(mod, url);
      console.log(`\n═══ ${mod.toUpperCase()} ═══`);
      console.log(JSON.stringify(res.result || {error: res.error}, null, 2));
    }
  } else {
    const res = await runModule(moduleName, url);
    console.log(JSON.stringify(res.result || {error: res.error}, null, 2));
  }
}

main().catch(e => {
  console.error('Fatal:', e.message);
  process.exit(1);
});
