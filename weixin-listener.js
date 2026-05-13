#!/usr/bin/env node
/**
 * Standalone WeChat (微信) iLink Bot listener v2
 */
const BASE_URL = 'https://ilinkai.weixin.qq.com';
const TOKEN = 'ed7b608aca57@im.bot:0600000a089a9bfcb0db1ef964dc25db859000';

const BASE_INFO = {
  client_version: 65799,
  app_id: 'wx2c687af3c28c3491',
  bot_agent: 'OpenClaw'
};

let getUpdatesBuf = '';
let consecutiveFailures = 0;
const MAX_FAILURES = 3;

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}`;
  console.log(line);
}

async function makeRequest(endpoint, body, timeoutMs = 15000) {
  const url = `${BASE_URL}/${endpoint}`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${TOKEN}`,
      'AuthorizationType': 'ilink_bot_token',
    },
    body: JSON.stringify(body),
    signal: controller.signal,
  });
  clearTimeout(timer);
  const text = await res.text();
  return { status: res.status, body: text };
}

async function notifyStart() {
  try {
    const r = await makeRequest('ilink/bot/msg/notifystart', { base_info: BASE_INFO });
    log(`notifyStart: ${r.status} ${r.body.substring(0, 80)}`);
    return r;
  } catch (e) {
    log(`notifyStart ignored: ${e.message}`);
    return null;
  }
}

async function pollLoop() {
  const body = {
    base_info: BASE_INFO,
    get_updates_buf: getUpdatesBuf,
    timeout: 35000,
  };

  const r = await makeRequest('ilink/bot/getupdates', body, 45000);
  consecutiveFailures = 0;

  let data;
  try { data = JSON.parse(r.body); } catch { data = {}; }

  if (data.errcode && data.errcode !== 0) {
    log(`API error: errcode=${data.errcode} errmsg=${data.errmsg}`);
    if (data.errcode === -14) {
      log('SESSION EXPIRED!');
      return false;
    }
    return true;
  }

  if (data.get_updates_buf) {
    getUpdatesBuf = data.get_updates_buf;
  }

  const msgs = data.msgs || [];
  for (const msg of msgs) {
    const from = msg.from_user_id || '?';
    const to = msg.to_user_id || '?';
    const items = (msg.item_list || []).map(i => ({
      type: i.type,
      text: i.text_content || i.content || '',
      img: i.img_content?.md5sum || '',
    }));

    log(`MSG from=${from} to=${to} type=${msg.message_type} items=${items.length}`);
    for (const item of items) {
      if (item.type === 1) log(`  TEXT: ${item.text.substring(0, 200)}`);
      else if (item.type === 3) log(`  IMAGE: ${item.img}`);
      else log(`  OTHER(${item.type}): ${item.text.substring(0, 100)}`);
    }
  }

  return true;
}

async function main() {
  log('=== WeChat iLink Bot Listener v2 ===');
  log(`Account: ed7b608aca57-im-bot`);
  log(`Token: ${TOKEN.substring(0, 25)}...`);
  log('Starting...');

  await notifyStart();

  let running = true;
  let cycle = 0;
  while (running) {
    cycle++;
    try {
      running = await pollLoop();
    } catch (e) {
      consecutiveFailures++;
      log(`Poll error (${consecutiveFailures}/${MAX_FAILURES}): ${e.message}`);
      if (consecutiveFailures >= MAX_FAILURES) {
        log('Too many failures, backing off 30s');
        await new Promise(r => setTimeout(r, 30000));
        consecutiveFailures = 0;
      }
    }
    if (cycle % 5 === 0) log(`Heartbeat: ${cycle} cycles done`);
  }

  log('Listener stopped');
}

main().catch(e => { console.error(`Fatal: ${e.message}`); process.exit(1); });
