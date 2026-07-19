/**
 * Google Calendar → Google Sheets 読み込み専用スクリプト
 *
 * 複数のマイカレンダーからイベントを取得し、1枚のシートにマージ表示します。
 * シートからカレンダーへの書き込み・自動同期はありません。
 *
 * セットアップ:
 * 1. 拡張機能 > Apps Script でこのスクリプトを開く
 * 2. リソース > 高度なGoogleサービス > Calendar API を有効化
 * 3. CONFIG.CALENDAR_IDS に取得したいカレンダーIDを列挙（'primary' 可）
 * 4. 初回実行で権限を許可
 */

// ========== 設定 ==========
const CONFIG = {
  SHEET_NAME: 'カレンダー連携',
  /** 取得対象。'primary' はデフォルト（メイン）カレンダーに変換されます。 */
  CALENDAR_IDS: ['primary'],
  SYNC_DAYS_PAST: 30,
  SYNC_DAYS_FUTURE: 90,
  HEADERS: [
    'イベントID',
    'カレンダーID',
    'カレンダー名',
    'タイトル',
    '日付',
    '開始時間',
    '終了時間',
    'ビデオ(Meet)',
    '通知(分)',
    '説明'
  ]
};

const EVENTS_LIST_MAX_RESULTS = 2500;

// ========== 初期セットアップ ==========
/**
 * 初回セットアップ: シートを作成し、ヘッダーを設定
 * （旧版の編集トリガーが残っている場合は削除します）
 */
function setup() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(CONFIG.SHEET_NAME);

  if (!sheet) {
    sheet = ss.insertSheet(CONFIG.SHEET_NAME);
  }

  sheet.getRange(1, 1, 1, CONFIG.HEADERS.length).setValues([CONFIG.HEADERS]);
  sheet.getRange(1, 1, 1, CONFIG.HEADERS.length).setFontWeight('bold');
  sheet.setFrozenRows(1);
  sheet.autoResizeColumns(1, CONFIG.HEADERS.length);

  deleteLegacyEditTriggers();

  SpreadsheetApp.getUi().alert(
    'セットアップ完了（読み込み専用）。\n「カレンダーから読み込み」で複数カレンダーをシートに取り込めます。'
  );
}

/** 旧バージョンの onSheetEdit トリガーを削除 */
function deleteLegacyEditTriggers() {
  ScriptApp.getProjectTriggers().forEach(trigger => {
    if (trigger.getHandlerFunction() === 'onSheetEdit') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
}

// ========== カレンダー → シート（読み込み） ==========
function syncCalendarToSheet() {
  const now = new Date();
  const timeMin = new Date(now.getTime() - CONFIG.SYNC_DAYS_PAST * 24 * 60 * 60 * 1000).toISOString();
  const timeMax = new Date(now.getTime() + CONFIG.SYNC_DAYS_FUTURE * 24 * 60 * 60 * 1000).toISOString();
  loadCalendarEventsToSheet(timeMin, timeMax);
}

function showSyncCalendarRangeDialog() {
  const html = HtmlService.createHtmlOutput(
    '<!DOCTYPE html><html><head><base target="_top">' +
    '<meta charset="UTF-8"><style>body{font-family:sans-serif;padding:16px;font-size:14px}' +
    'label{display:block;margin:10px 0}button{margin-top:14px;padding:8px 16px}</style></head><body>' +
    '<p>取得する期間を指定してください（スクリプトのタイムゾーンの日付として解釈されます）。</p>' +
    '<label>開始日 <input type="date" id="start"></label>' +
    '<label>終了日 <input type="date" id="end"></label>' +
    '<button type="button" id="go">読み込む</button>' +
    '<script>' +
    'document.getElementById("go").onclick=function(){' +
    'var s=document.getElementById("start").value,e=document.getElementById("end").value;' +
    'if(!s||!e){alert("開始日と終了日を入力してください。");return;}' +
    'google.script.run.withSuccessHandler(function(){google.script.host.close();})' +
    '.withFailureHandler(function(err){alert(err&&err.message?err.message:String(err));})' +
    '.syncCalendarToSheetForRange(s,e);' +
    '};' +
    '</script></body></html>'
  )
    .setWidth(420)
    .setHeight(260);
  SpreadsheetApp.getUi().showModalDialog(html, 'カレンダー取得期間の指定');
}

function syncCalendarToSheetForRange(startDateStr, endDateStr) {
  if (!startDateStr || !endDateStr) {
    SpreadsheetApp.getUi().alert('開始日と終了日を指定してください。');
    return;
  }
  let start = parseDate(startDateStr.toString().trim());
  let end = parseDate(endDateStr.toString().trim());
  start.setHours(0, 0, 0, 0);
  end.setHours(23, 59, 59, 999);
  if (start.getTime() > end.getTime()) {
    SpreadsheetApp.getUi().alert('開始日は終了日より前（または同じ日）である必要があります。');
    return;
  }
  loadCalendarEventsToSheet(start.toISOString(), end.toISOString());
}

/**
 * 複数カレンダーのイベントを取得しシートに書き込む
 * @param {string} timeMin ISO 8601
 * @param {string} timeMax ISO 8601
 */
function loadCalendarEventsToSheet(timeMin, timeMax) {
  const sheet = getSheet();
  const nameById = buildCalendarNameMap();
  const resolvedIds = CONFIG.CALENDAR_IDS.map(resolveCalendarId);

  /** @type {{event: Object, calendarId: string}[]} */
  const tuples = [];

  for (const calendarId of resolvedIds) {
    let items;
    try {
      items = listAllEvents(calendarId, timeMin, timeMax);
    } catch (err) {
      throw new Error(`カレンダー「${calendarId}」の取得に失敗: ${err.message}`);
    }
    for (const event of items) {
      tuples.push({ event, calendarId });
    }
  }

  tuples.sort((a, b) => eventStartMs(a.event) - eventStartMs(b.event));

  const nameCache = Object.assign({}, nameById);
  function calendarDisplayName(id) {
    if (nameCache[id]) return nameCache[id];
    try {
      const cal = Calendar.Calendars.get(id);
      nameCache[id] = (cal && cal.summary) || id;
    } catch (e) {
      nameCache[id] = id;
    }
    return nameCache[id];
  }

  const rows = tuples.map(({ event, calendarId }) => {
    const start = event.start.dateTime ? new Date(event.start.dateTime) : new Date(event.start.date);
    const end = event.end.dateTime ? new Date(event.end.dateTime) : new Date(event.end.date);
    const isAllDay = !!event.start.date;

    let dateStr = '';
    let startTimeStr = '';
    let endTimeStr = '';

    if (isAllDay) {
      dateStr = Utilities.formatDate(start, Session.getScriptTimeZone(), 'yyyy-MM-dd');
      startTimeStr = '終日';
      endTimeStr = '終日';
    } else {
      dateStr = Utilities.formatDate(start, Session.getScriptTimeZone(), 'yyyy-MM-dd');
      startTimeStr = Utilities.formatDate(start, Session.getScriptTimeZone(), 'HH:mm');
      endTimeStr = Utilities.formatDate(end, Session.getScriptTimeZone(), 'HH:mm');
    }

    const hangoutLink =
      event.hangoutLink ||
      (event.conferenceData && event.conferenceData.entryPoints
        ? (event.conferenceData.entryPoints.find(ep => ep.entryPointType === 'video') || {}).uri || ''
        : '');

    const reminderMinutes =
      event.reminders && event.reminders.overrides
        ? event.reminders.overrides.map(r => r.minutes).join(',')
        : '';

    const calName = calendarDisplayName(calendarId);

    return [
      event.id,
      calendarId,
      calName,
      event.summary || '（無題）',
      dateStr,
      startTimeStr,
      endTimeStr,
      hangoutLink || '',
      reminderMinutes,
      event.description || ''
    ];
  });

  const lastRow = sheet.getLastRow();
  if (lastRow > 1) {
    sheet.getRange(2, 1, lastRow, CONFIG.HEADERS.length).clear();
  }

  if (rows.length > 0) {
    sheet.getRange(2, 1, rows.length, CONFIG.HEADERS.length).setValues(rows);
  }

  SpreadsheetApp.getUi().alert(
    `${resolvedIds.length} 件のカレンダーから、合計 ${rows.length} 件のイベントを読み込みました。`
  );
}

/**
 * @param {string} calendarId
 * @param {string} timeMin
 * @param {string} timeMax
 * @returns {Object[]}
 */
function listAllEvents(calendarId, timeMin, timeMax) {
  const all = [];
  let pageToken;
  do {
    const request = {
      timeMin: timeMin,
      timeMax: timeMax,
      singleEvents: true,
      orderBy: 'startTime',
      maxResults: EVENTS_LIST_MAX_RESULTS
    };
    if (pageToken) {
      request.pageToken = pageToken;
    }
    const response = Calendar.Events.list(calendarId, request);
    if (response.items && response.items.length) {
      all.push.apply(all, response.items);
    }
    pageToken = response.nextPageToken;
  } while (pageToken);
  return all;
}

/** @returns {Object<string, string>} calendarId -> 表示名 */
function buildCalendarNameMap() {
  const map = {};
  let pageToken;
  do {
    const req = { maxResults: 250 };
    if (pageToken) req.pageToken = pageToken;
    const list = Calendar.CalendarList.list(req);
    const items = list.items || [];
    items.forEach(entry => {
      if (entry.id) {
        map[entry.id] = entry.summary || entry.id;
      }
    });
    pageToken = list.nextPageToken;
  } while (pageToken);
  return map;
}

/**
 * @param {string} id Config の要素（'primary' または実ID）
 */
function resolveCalendarId(id) {
  const s = (id || '').toString().trim();
  if (!s || s === 'primary') {
    return CalendarApp.getDefaultCalendar().getId();
  }
  return s;
}

function eventStartMs(event) {
  if (event.start.dateTime) {
    return new Date(event.start.dateTime).getTime();
  }
  if (event.start.date) {
    return new Date(event.start.date).getTime();
  }
  return 0;
}

// ========== ユーティリティ ==========
function getSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(CONFIG.SHEET_NAME);
  if (!sheet) {
    throw new Error(`シート「${CONFIG.SHEET_NAME}」が見つかりません。先に setup() を実行してください。`);
  }
  return sheet;
}

function parseDate(dateStr) {
  const str = dateStr.toString().trim();
  const match = str.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (match) {
    return new Date(parseInt(match[1], 10), parseInt(match[2], 10) - 1, parseInt(match[3], 10));
  }
  const d = new Date(str);
  if (isNaN(d.getTime())) throw new Error(`日付形式が不正です: ${dateStr}`);
  return d;
}

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('カレンダー連携')
    .addItem('初期セットアップ', 'setup')
    .addItem('カレンダーから読み込み', 'syncCalendarToSheet')
    .addItem('カレンダーから読み込み（期間を指定）', 'showSyncCalendarRangeDialog')
    .addToUi();
}
