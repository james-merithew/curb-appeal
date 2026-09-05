import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(process.argv[2] || '.');
const assetsRoot = path.join(root, 'asset-library', 'svg');
const tokens = {
  color: {
    indigo900: '#17103D',
    indigo800: '#211054',
    violet600: '#5B35F5',
    violet800: '#4020B5',
    sky400: '#69B7FF',
    sky700: '#1266A6',
    marigold400: '#FFBF24',
    amber700: '#9A5700',
    lavender100: '#F2EEFF',
    lavender200: '#E2DAFF',
    white: '#FFFFFF',
  },
  type: {
    familyUI: 'Atkinson Hyperlegible, Aptos, Arial, sans-serif',
    familyWordmark: 'Nunito Sans, Aptos, Arial, sans-serif',
    weightRegular: 400,
    weightMedium: 600,
    weightBold: 750,
  },
  radius: { small: 8, medium: 14, large: 22, pill: 999 },
  spacing: { 1: 4, 2: 8, 3: 12, 4: 16, 5: 24, 6: 32, 7: 48 },
  motion: {
    scanDurationMs: 7000,
    pinDropDurationMs: 620,
    pinDropEasing: 'cubic-bezier(.2,.9,.25,1.2)',
    reducedMotion: 'instant end state',
  },
  pinHierarchy: {
    overviewPx: { estimated: 32, scannedOnSite: 36, ownerConfirmed: 40 },
    streetPx: { estimated: 40, scannedOnSite: 44, ownerConfirmed: 48 },
    selectedPx: { estimated: 52, scannedOnSite: 56, ownerConfirmed: 60 },
    receiptPx: { estimated: 24, scannedOnSite: 28, ownerConfirmed: 32 },
    liveScanDropPx: 64,
    clusterPx: 48,
    zIndex: { cluster: 10, estimated: 20, scannedOnSite: 30, ownerConfirmed: 40, matched: 50, selected: 60, liveScanDrop: 70 },
  },
  interaction: {
    touchTargetMinPx: 48,
    focusRingPx: 3,
    focusRingOffsetPx: 3,
    pressedScale: 0.97,
    sheetStopsPercent: [18, 54, 92],
  },
};

const C = tokens.color;
const esc = (s) => s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
const mkdir = (dir) => fs.mkdirSync(dir, { recursive: true });
const wrap = (viewBox, body, label, background = '') => {
  const [,,, h] = viewBox.split(' ').map(Number);
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="${viewBox}" role="img" aria-labelledby="title desc">
  <title id="title">${esc(label)}</title><desc id="desc">EntryMap ${esc(label)} asset.</desc>
  ${background ? `<rect width="100%" height="${h}" fill="${background}"/>` : ''}
  ${body}
</svg>\n`;
};
const stroke = (body, color = C.indigo900, width = 2.5) => `<g fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round">${body}</g>`;
const assetList = [];
const add = (category, id, viewBox, body, label, meta = {}) => {
  const dir = path.join(assetsRoot, category);
  mkdir(dir);
  const file = path.join(dir, `${id}.svg`);
  fs.writeFileSync(file, wrap(viewBox, body, label, meta.background || ''));
  assetList.push({ category, id, file: path.relative(root, file).replaceAll('\\', '/'), viewBox, label, ...meta });
};

const logoMark = ({ field = C.violet600, pathFill = C.lavender200, outline = C.white, mono = null } = {}) => {
  const violet = mono || field;
  const white = mono || outline;
  const sky = mono || C.sky400;
  const gold = mono || C.marigold400;
  const lavender = mono || pathFill;
  return `<path d="M64 8C35.3 8 12 31.1 12 59.6c0 37.2 37.6 70.8 49.5 80.7a4 4 0 0 0 5 0C78.4 130.4 116 96.8 116 59.6 116 31.1 92.7 8 64 8Z" fill="${violet}" stroke="${white}" stroke-width="5"/>
  <path d="M34 66V50h60v16M42 66v35M86 66v35M42 101l22 29 22-29" fill="none" stroke="${white}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M44 101 64 130 84 101Z" fill="${lavender}"/>
  <path d="M30 53c1-11 5-19 12-26" fill="none" stroke="${sky}" stroke-width="8" stroke-linecap="round"/>
  <path d="M49 22c9-5 21-5 30 0" fill="none" stroke="${violet}" stroke-width="8" stroke-linecap="round"/>
  <path d="M86 27c7 7 11 15 12 26" fill="none" stroke="${gold}" stroke-width="8" stroke-linecap="round"/>`;
};

const wordmark = (onDark = true, monochrome = false) => {
  const entry = monochrome ? (onDark ? C.white : C.indigo900) : (onDark ? C.sky400 : C.violet800);
  const map = onDark ? C.white : C.indigo900;
  return `<g transform="translate(150 16)"><text x="0" y="70" font-family="${tokens.type.familyWordmark}" font-size="68" font-weight="750" letter-spacing="-3"><tspan fill="${entry}">entry</tspan><tspan fill="${map}">map</tspan></text></g>`;
};

add('brand', 'mark-primary', '0 0 128 148', logoMark(), 'Primary logo mark');
add('brand', 'mark-on-light', '0 0 128 148', logoMark({ outline: C.white }), 'Logo mark for light surfaces');
add('brand', 'mark-monochrome-light', '0 0 128 148', logoMark({ mono: C.white }), 'Monochrome light logo mark');
add('brand', 'mark-monochrome-dark', '0 0 128 148', logoMark({ mono: C.indigo900, outline: C.indigo900 }), 'Monochrome dark logo mark');
add('brand', 'wordmark-on-dark', '0 0 520 150', `<g transform="translate(8 1) scale(.86)">${logoMark()}</g>${wordmark(true)}`, 'EntryMap wordmark on dark', { background: C.indigo900 });
add('brand', 'wordmark-on-light', '0 0 520 150', `<g transform="translate(8 1) scale(.86)">${logoMark()}</g>${wordmark(false)}`, 'EntryMap wordmark on light', { background: C.lavender100 });
add('brand', 'wordmark-monochrome-light', '0 0 520 150', `<g transform="translate(8 1) scale(.86)">${logoMark({ mono: C.white })}</g>${wordmark(true, true)}`, 'Monochrome EntryMap wordmark', { background: C.indigo900 });
add('brand', 'app-icon', '0 0 256 256', `<rect x="0" y="0" width="256" height="256" rx="58" fill="${C.indigo900}"/><g transform="translate(64 50)">${logoMark()}</g>`, 'EntryMap app icon');
add('brand', 'favicon', '0 0 64 64', `<rect width="64" height="64" rx="15" fill="${C.indigo900}"/><g transform="translate(12 6) scale(.31)">${logoMark()}</g>`, 'EntryMap favicon');

const pinShape = (fill, outline, dashed = false) => `<path d="M48 6c-21 0-36 15.7-36 35.3 0 25.1 24.3 45.8 33.5 52.8a4 4 0 0 0 5 0C59.7 87.1 84 66.4 84 41.3 84 21.7 69 6 48 6Z" fill="${fill}" stroke="${outline}" stroke-width="4" ${dashed ? 'stroke-dasharray="7 6"' : ''}/>`;
const infoIcon = `<text x="48" y="56" text-anchor="middle" font-family="Georgia, serif" font-size="39" font-weight="700" font-style="italic" fill="${C.sky700}">i</text>`;
const personIcon = stroke(`<circle cx="48" cy="34" r="9"/><path d="M30 69c1-15 8-23 18-23s17 8 18 23Z"/>`, C.indigo900, 4);
const storeIcon = stroke(`<path d="M28 38h40l-4-12H32Z"/><path d="M30 38v30h36V38M42 68V51h13v17"/><path d="M28 38c0 5 6 7 10 3 4 4 9 4 13 0 4 4 9 4 13 0 4 4 10 2 10-3"/>`, C.white, 3.8);
const rings = (filled, color, total = 3) => Array.from({ length: total }, (_, i) => `<circle cx="${35 + i * 13}" cy="15" r="4.5" fill="${i < filled ? color : C.white}" stroke="${color}" stroke-width="2"/>`).join('');
add('pins', 'estimated', '0 0 96 104', `${rings(0, C.sky700)}${pinShape(C.white, C.sky400, true)}${infoIcon}`, 'Estimated entrance pin', { tier: 'Estimated', color: C.sky400 });
add('pins', 'scanned-on-site', '0 0 96 104', `${rings(2, C.marigold400)}${pinShape(C.marigold400, C.white)}${personIcon}`, 'Scanned on-site entrance pin', { tier: 'Scanned on-site', color: C.marigold400 });
add('pins', 'owner-confirmed', '0 0 112 104', `${rings(3, C.violet600)}${pinShape(C.violet600, C.white)}${storeIcon}<circle cx="88" cy="28" r="14" fill="${C.white}" stroke="${C.violet800}" stroke-width="3"/>${stroke('<path d="m81 28 5 5 9-11"/>', C.violet800, 3)}`, 'Owner-confirmed entrance pin', { tier: 'Owner-confirmed', color: C.violet600 });

add('halos', 'good-match', '0 0 104 104', `<circle cx="52" cy="52" r="42" fill="none" stroke="${C.indigo900}" stroke-width="5"/><circle cx="52" cy="52" r="32" fill="none" stroke="${C.sky400}" stroke-width="2" opacity=".65"/>`, 'Good match halo', { lineStyle: 'solid' });
add('halos', 'partial-match', '0 0 104 104', `<circle cx="52" cy="52" r="42" fill="none" stroke="${C.violet600}" stroke-width="5" stroke-dasharray="15 9"/>`, 'Partial match halo', { lineStyle: 'dashed' });
add('halos', 'unknown-match', '0 0 104 104', `<circle cx="52" cy="52" r="42" fill="none" stroke="${C.sky700}" stroke-width="5" stroke-linecap="round" stroke-dasharray="1 11"/>`, 'Unknown match halo', { lineStyle: 'dotted' });

const iconBodies = {
  map: '<path d="m4 7 7-3 7 3 7-3v22l-7 3-7-3-7 3Z"/><path d="M11 4v22M18 7v22"/>',
  scan: '<path d="M5 11V6a2 2 0 0 1 2-2h5M25 11V6a2 2 0 0 0-2-2h-5M5 21v5a2 2 0 0 0 2 2h5M25 21v5a2 2 0 0 1-2 2h-5"/><path d="M10 15h12M10 20h12"/>',
  profile: '<circle cx="16" cy="10" r="6"/><path d="M5 29c1-9 5-13 11-13s10 4 11 13Z"/>',
  'my-needs': '<path d="M16 28S4 20 4 11c0-7 9-10 12-4 3-6 12-3 12 4 0 9-12 17-12 17Z"/>',
  camera: '<path d="M5 10h5l2-4h8l2 4h5v17H5Z"/><circle cx="16" cy="18" r="5"/>',
  storefront: '<path d="M5 13h22L24 6H8Z"/><path d="M7 13v15h18V13M12 28v-9h8v9"/><path d="M5 13c0 4 5 5 7 2 3 3 6 3 8 0 3 3 6 3 8-2"/>',
  person: '<circle cx="16" cy="9" r="5"/><path d="M7 28c1-9 4-13 9-13s8 4 9 13Z"/>',
  info: '<circle cx="16" cy="16" r="12"/><path d="M16 14v8M16 9h.01"/>',
  correction: '<path d="m6 25 5-1 14-14-4-4L7 20Z"/><path d="m18 9 4 4M5 28h22"/>',
  freshness: '<circle cx="16" cy="16" r="12"/><path d="M16 9v8l5 3"/>',
  confidence: '<path d="M7 27V19M13 27V14M19 27V9M25 27V5"/>',
  location: '<path d="M16 29S6 21 6 12a10 10 0 0 1 20 0c0 9-10 17-10 17Z"/><circle cx="16" cy="12" r="3"/>',
  menu: '<path d="M5 8h22M5 16h22M5 24h22"/>',
  close: '<path d="m7 7 18 18M25 7 7 25"/>',
  'chevron-right': '<path d="m11 5 11 11-11 11"/>',
  'check-outline': '<circle cx="16" cy="16" r="13"/><path d="m9 16 5 5 10-12"/>',
  search: '<circle cx="14" cy="14" r="9"/><path d="m21 21 7 7"/>',
  filters: '<path d="M5 8h22M9 16h18M13 24h14"/><circle cx="9" cy="8" r="2"/><circle cx="13" cy="16" r="2"/><circle cx="17" cy="24" r="2"/>',
  photo: '<rect x="4" y="6" width="24" height="21" rx="3"/><circle cx="12" cy="13" r="3"/><path d="m7 24 7-7 5 5 3-3 4 5"/>',
  receipt: '<path d="M8 4h16v25l-4-3-4 3-4-3-4 3Z"/><path d="M12 10h8M12 15h8M12 20h5"/>',
};
for (const [id, body] of Object.entries(iconBodies)) {
  add('ui-icons', id, '0 0 32 32', stroke(body, C.violet800, 2.3), `${id.replaceAll('-', ' ')} icon`, { recommendedSizes: [24, 32, 48] });
}

const featureBodies = {
  'step-free-entry': '<path d="M5 25h22M8 25V9h15v16M13 17h8"/>',
  'ramp-visible': '<path d="M4 26h24L28 12 4 26Z"/><path d="M9 23h15M14 20h10M19 17h5"/>',
  'auto-door-button': '<rect x="5" y="4" width="14" height="24" rx="2"/><circle cx="23" cy="16" r="5"/><path d="M23 13v6M20 16h6"/>',
  'easy-grip-handle': '<rect x="5" y="4" width="15" height="24" rx="2"/><path d="M18 15h7M25 12v8"/>',
  'wide-door': '<path d="M4 27V5h10v22M18 27V5h10v22M14 16h4"/>',
  'accessibility-signage': '<rect x="5" y="4" width="22" height="24" rx="3"/><circle cx="16" cy="10" r="2"/><path d="M16 13v7M11 16h10M16 20l-4 6M16 20l5 6"/>',
  'clear-approach': '<path d="M5 27 12 5h8l7 22Z"/><path d="M16 9v4M16 18v4"/>',
  unknown: '<path d="M11 11a5 5 0 1 1 8 4c-2 1-3 3-3 5M16 26h.01"/><circle cx="16" cy="16" r="13" stroke-dasharray="4 4"/>',
};
for (const [id, body] of Object.entries(featureBodies)) {
  add('feature-icons', id, '0 0 32 32', stroke(body, id === 'unknown' ? C.sky700 : C.violet800, 2.2), `${id.replaceAll('-', ' ')} feature icon`, { recommendedSizes: [24, 32, 48] });
}

const texasFlag = `<rect x="2" y="6" width="28" height="20" rx="2" fill="${C.white}" stroke="${C.indigo900}" stroke-width="1.5"/><path d="M2 6h10v20H2Z" fill="${C.indigo900}"/><path d="M12 6h18v10H12Z" fill="${C.indigo900}"/><path d="M12 16h18v10H12Z" fill="${C.white}"/><path d="m7 11 1.2 2.5 2.8.4-2 2 .5 2.8L7 17.3l-2.5 1.4.5-2.8-2-2 2.8-.4Z" fill="${C.white}"/>`;
add('provenance', 'texas-record', '0 0 32 32', texasFlag, 'Texas public record provenance mark', { meaning: 'State record provenance only; never a trust tier' });
add('provenance', 'community-source', '0 0 32 32', stroke('<circle cx="11" cy="12" r="4"/><circle cx="21" cy="12" r="4"/><path d="M3 27c0-7 3-10 8-10s8 3 8 10M15 27c0-5 2-8 6-8s7 3 8 8"/>', C.violet800, 2.2), 'Community provenance icon');
add('provenance', 'owner-source', '0 0 32 32', stroke(iconBodies.storefront, C.violet800, 2.2), 'Owner provenance icon');
add('provenance', 'photo-source', '0 0 32 32', stroke(iconBodies.photo, C.violet800, 2.2), 'Photo provenance icon');
add('provenance', 'public-record', '0 0 32 32', stroke(iconBodies.receipt, C.violet800, 2.2), 'Public record provenance icon');

const badge = (label, icon, fill, text, outline = fill) => `<rect x="2" y="2" width="236" height="44" rx="22" fill="${fill}" stroke="${outline}" stroke-width="2"/><g transform="translate(12 8) scale(.85)">${icon}</g><text x="52" y="30" font-family="${tokens.type.familyUI}" font-size="16" font-weight="650" fill="${text}">${esc(label)}</text>`;
add('badges', 'estimated', '0 0 240 48', badge('Estimated', stroke(iconBodies.info, C.sky700, 2.2), C.white, C.indigo900, C.sky400), 'Estimated badge');
add('badges', 'scanned-on-site', '0 0 240 48', badge('Scanned on-site', stroke(iconBodies.person, C.indigo900, 2.2), C.marigold400, C.indigo900), 'Scanned on-site badge');
add('badges', 'owner-confirmed', '0 0 240 48', badge('Owner-confirmed', stroke(iconBodies.storefront, C.white, 2.2), C.violet600, C.white), 'Owner-confirmed badge');
add('badges', 'freshness-current', '0 0 240 48', badge('Seen 3 weeks ago', stroke(iconBodies.freshness, C.violet800, 2.2), C.lavender100, C.indigo900, C.lavender200), 'Current freshness badge');
add('badges', 'freshness-recheck', '0 0 280 48', `<rect x="2" y="2" width="276" height="44" rx="22" fill="${C.marigold400}" stroke="${C.indigo900}" stroke-width="2"/>${stroke('<circle cx="25" cy="24" r="10"/><path d="M25 18v7l4 2"/>', C.indigo900, 2)}<text x="46" y="30" font-family="${tokens.type.familyUI}" font-size="15" font-weight="650" fill="${C.indigo900}">Scanned 14 months ago — re-check</text>`, 'Re-check freshness badge');
for (let i = 1; i <= 3; i++) {
  const dots = [0, 1, 2].map((_, n) => `<circle cx="${157 + n * 18}" cy="24" r="6" fill="${n < i ? C.violet600 : C.white}" stroke="${C.violet800}" stroke-width="2"/>`).join('');
  add('badges', `confidence-${i}`, '0 0 220 48', `<rect x="2" y="2" width="216" height="44" rx="22" fill="${C.white}" stroke="${C.lavender200}" stroke-width="2"/><text x="18" y="30" font-family="${tokens.type.familyUI}" font-size="16" font-weight="650" fill="${C.indigo900}">Confidence</text>${dots}`, `Confidence ${i} of 3 badge`);
}

const card = (title, subtitle, art, accent = C.violet600) => `<rect x="2" y="2" width="236" height="176" rx="24" fill="${C.white}" stroke="${C.indigo900}" stroke-width="2"/><circle cx="120" cy="65" r="42" fill="${C.lavender100}"/>${art}<text x="120" y="125" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="17" font-weight="750" fill="${C.indigo900}">${esc(title)}</text><text x="120" y="148" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="12" fill="${C.indigo900}">${esc(subtitle)}</text><path d="M82 162h76" stroke="${accent}" stroke-width="5" stroke-linecap="round"/>`;
add('states', 'empty-area', '0 0 240 180', card('Map the first entrance', 'Help neighbors plan ahead', `<g transform="translate(88 27) scale(.67)">${pinShape(C.white, C.sky400, true)}${infoIcon}</g>`, C.sky400), 'Empty area state');
add('states', 'camera-permission', '0 0 240 180', card('Allow camera access', 'Only the doorway is captured', `<g transform="translate(104 49)">${stroke(iconBodies.camera, C.violet800, 2.3)}</g>`, C.marigold400), 'Camera permission state');
add('states', 'processing', '0 0 240 180', card('Checking the entrance', 'Usually under 8 seconds', `<circle cx="120" cy="65" r="30" fill="none" stroke="${C.lavender200}" stroke-width="7"/><path d="M120 35a30 30 0 0 1 28 20" fill="none" stroke="${C.violet600}" stroke-width="7" stroke-linecap="round"/><text x="120" y="73" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="24" font-weight="750" fill="${C.violet800}">7</text>`), 'Scan processing state');
add('states', 'published', '0 0 240 180', card('Entrance added', 'Thanks for helping neighbors', `<g transform="translate(82 25) scale(.72)">${pinShape(C.marigold400, C.white)}${personIcon}</g><circle cx="151" cy="50" r="13" fill="${C.white}" stroke="${C.violet800}" stroke-width="2"/>${stroke('<path d="m145 50 4 4 8-10"/>', C.violet800, 2.5)}`), 'Published success state');
add('states', 'offline', '0 0 240 180', card('Saved for later', 'Uploads when you are online', `${stroke('<path d="M93 75h54c17 0 19-25 3-29-3-18-29-21-37-7-15-5-27 8-20 20"/>', C.violet800, 3)}${stroke('<path d="m104 67 10 10 22-24"/>', C.violet800, 3)}`), 'Offline saved state');
add('states', 'recheck', '0 0 240 180', card('Could you take another look?', 'Time is context—not a grade', `<g transform="translate(90 28) scale(.62)">${pinShape(C.marigold400, C.white)}${personIcon}</g><circle cx="152" cy="53" r="12" fill="${C.white}" stroke="${C.amber700}" stroke-width="2"/>${stroke('<path d="M152 46v8l4 2"/>', C.amber700, 2)}`, C.marigold400), 'Freshness re-check state');

const keyframes = `<g transform="translate(20 20)"><path d="M32 10v100" stroke="${C.lavender200}" stroke-width="2" stroke-dasharray="4 5"/><g transform="translate(-16 -2) scale(.5)">${pinShape(C.marigold400, C.white)}${personIcon}</g><text x="60" y="22" font-family="${tokens.type.familyUI}" font-size="14" fill="${C.indigo900}">0 ms · above map</text><g transform="translate(-16 34) scale(.5)">${pinShape(C.marigold400, C.white)}${personIcon}</g><ellipse cx="32" cy="89" rx="25" ry="8" fill="none" stroke="${C.sky400}" stroke-width="3"/><text x="60" y="64" font-family="${tokens.type.familyUI}" font-size="14" fill="${C.indigo900}">420 ms · impact + ripple</text><g transform="translate(-16 66) scale(.5)">${pinShape(C.marigold400, C.white)}${personIcon}</g><text x="60" y="105" font-family="${tokens.type.familyUI}" font-size="14" fill="${C.indigo900}">620 ms · settled</text></g>`;
add('motion', 'pin-drop-keyframes', '0 0 300 150', keyframes, 'Pin drop motion keyframes', { durationMs: 620 });

const labelText = (label, color = C.indigo900, x = 130, y = 35, size = 17) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="${size}" font-weight="700" fill="${color}">${esc(label)}</text>`;
const controlButton = (label, fill, textColor, outline = fill, extra = '') => `<rect x="5" y="5" width="250" height="46" rx="16" fill="${fill}" stroke="${outline}" stroke-width="2.5"/>${extra}${labelText(label, textColor, 130, 35)}`;
add('controls', 'primary-default', '0 0 260 56', controlButton('Continue', C.violet600, C.white), 'Primary button default');
add('controls', 'primary-pressed', '0 0 260 56', `<g transform="translate(4 2) scale(.97)">${controlButton('Continue', C.violet800, C.white)}</g>`, 'Primary button pressed');
add('controls', 'primary-focus', '0 0 270 66', `<rect x="3" y="3" width="264" height="60" rx="21" fill="none" stroke="${C.sky400}" stroke-width="3"/>${controlButton('Continue', C.violet600, C.white).replaceAll('x="5"', 'x="10"').replaceAll('y="5"', 'y="10"').replaceAll('width="250"', 'width="250"').replaceAll('y="35"', 'y="40"')}`, 'Primary button keyboard focus');
add('controls', 'primary-unavailable', '0 0 260 56', controlButton('Continue', C.lavender200, C.indigo900, C.lavender200), 'Unavailable primary button without gray');
add('controls', 'scan-default', '0 0 260 56', controlButton('Scan an entrance', C.marigold400, C.indigo900, C.marigold400, `<g transform="translate(18 12) scale(.78)">${stroke(iconBodies.camera, C.indigo900, 2.3)}</g>`), 'Scan button default');
add('controls', 'scan-pressed', '0 0 260 56', `<g transform="translate(4 2) scale(.97)">${controlButton('Scan an entrance', C.marigold400, C.indigo900, C.indigo900, `<rect x="5" y="5" width="250" height="46" rx="16" fill="${C.indigo900}" opacity=".08"/><g transform="translate(18 12) scale(.78)">${stroke(iconBodies.camera, C.indigo900, 2.3)}</g>`)}</g>`, 'Scan button pressed');
add('controls', 'secondary-default', '0 0 260 56', controlButton('Not now', C.white, C.violet800, C.violet600), 'Secondary button default');
add('controls', 'secondary-pressed', '0 0 260 56', controlButton('Not now', C.lavender100, C.violet800, C.violet800), 'Secondary button pressed');
add('controls', 'quiet-action', '0 0 260 56', `${labelText('Suggest a correction', C.violet800, 142, 35)}<g transform="translate(12 12) scale(.78)">${stroke(iconBodies.correction, C.violet800, 2.3)}</g>`, 'Quiet text action');

const navState = (id, label, active, focus = false) => {
  const icon = iconBodies[id];
  return `${focus ? `<rect x="7" y="4" width="98" height="66" rx="20" fill="none" stroke="${C.sky400}" stroke-width="3"/>` : ''}<rect x="11" y="8" width="90" height="58" rx="18" fill="${active ? C.violet600 : C.indigo900}"/>${stroke(icon, C.white, 2.2).replace('<g ', '<g transform="translate(40 12) scale(.9)" ')}<text x="56" y="60" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="12" font-weight="${active ? 750 : 550}" fill="${C.white}">${label}</text>`;
};
add('navigation-states', 'map-active', '0 0 112 74', navState('map', 'Map', true), 'Map navigation active');
add('navigation-states', 'scan-active', '0 0 112 74', `${navState('scan', 'Scan', false)}<circle cx="56" cy="28" r="23" fill="none" stroke="${C.marigold400}" stroke-width="3"/>`, 'Scan navigation active');
add('navigation-states', 'profile-active', '0 0 112 74', navState('profile', 'Profile', true), 'Profile navigation active');
add('navigation-states', 'keyboard-focus', '0 0 112 74', navState('map', 'Map', true, true), 'Bottom navigation keyboard focus');

const chip = (label, fill, outline, textColor, dash = '', icon = '') => `<rect x="3" y="3" width="214" height="42" rx="21" fill="${fill}" stroke="${outline}" stroke-width="2.5" ${dash}/>${icon}${labelText(label, textColor, icon ? 126 : 110, 31, 15)}`;
add('chip-states', 'filter-default', '0 0 220 48', chip('Limited grip', C.white, C.lavender200, C.indigo900), 'Filter chip default');
add('chip-states', 'filter-selected', '0 0 220 48', chip('Limited grip', C.indigo900, C.indigo900, C.white, '', `<circle cx="26" cy="24" r="8" fill="${C.sky400}"/>${stroke('<path d="m21 24 4 4 7-9"/>', C.indigo900, 2)}`), 'Filter chip selected');
add('chip-states', 'filter-focus', '0 0 228 56', `<rect x="2" y="2" width="224" height="52" rx="25" fill="none" stroke="${C.sky400}" stroke-width="3"/>${chip('Limited grip', C.white, C.violet600, C.indigo900).replaceAll('x="3"', 'x="7"').replaceAll('y="3"', 'y="7"').replaceAll('y="31"', 'y="35"')}`, 'Filter chip keyboard focus');
add('chip-states', 'feature-fresh', '0 0 260 58', `<rect x="2" y="2" width="256" height="54" rx="16" fill="${C.white}" stroke="${C.lavender200}" stroke-width="2"/><g transform="translate(12 13)">${stroke(featureBodies['step-free-entry'], C.violet800, 2.2)}</g><text x="56" y="25" font-family="${tokens.type.familyUI}" font-size="15" font-weight="700" fill="${C.indigo900}">Step-free entry</text><text x="56" y="44" font-family="${tokens.type.familyUI}" font-size="12" fill="${C.violet800}">Seen 3 weeks ago · ●●●</text>`, 'Fresh confirmed feature chip');
add('chip-states', 'feature-aging', '0 0 290 58', `<rect x="2" y="2" width="286" height="54" rx="16" fill="${C.white}" stroke="${C.marigold400}" stroke-width="2"/><g transform="translate(12 13)">${stroke(featureBodies['wide-door'], C.violet800, 2.2)}</g><text x="56" y="25" font-family="${tokens.type.familyUI}" font-size="15" font-weight="700" fill="${C.indigo900}">Wide door</text><text x="56" y="44" font-family="${tokens.type.familyUI}" font-size="12" font-weight="650" fill="${C.indigo900}">Scanned 14 months ago — re-check</text>`, 'Aging feature chip');
add('chip-states', 'feature-unknown', '0 0 320 58', `<rect x="2" y="2" width="316" height="54" rx="16" fill="${C.lavender100}" stroke="${C.sky400}" stroke-width="2" stroke-dasharray="6 5"/><g transform="translate(12 13)">${stroke(featureBodies.unknown, C.sky700, 2.2)}</g><text x="56" y="25" font-family="${tokens.type.familyUI}" font-size="15" font-weight="700" fill="${C.indigo900}">Not yet seen</text><text x="56" y="44" font-family="${tokens.type.familyUI}" font-size="12" fill="${C.violet800}">Be the first to scan</text>`, 'Unknown feature invitation chip');

const field = (label, value, outline, helper = '', icon = '') => `<text x="8" y="16" font-family="${tokens.type.familyUI}" font-size="12" font-weight="700" fill="${C.indigo900}">${esc(label)}</text><rect x="5" y="23" width="310" height="46" rx="12" fill="${C.white}" stroke="${outline}" stroke-width="2.5"/>${icon}<text x="18" y="52" font-family="${tokens.type.familyUI}" font-size="15" fill="${value ? C.indigo900 : C.violet800}">${esc(value || helper)}</text>`;
add('field-states', 'text-empty', '0 0 320 76', field('Work email', '', C.lavender200, 'name@business.com'), 'Text field empty');
add('field-states', 'text-focused', '0 0 320 76', `<rect x="1" y="19" width="318" height="54" rx="15" fill="none" stroke="${C.sky400}" stroke-width="3"/>${field('Work email', 'owner@pageandspine.com', C.violet800)}`, 'Text field focused');
add('field-states', 'text-filled', '0 0 320 76', field('Work email', 'owner@pageandspine.com', C.violet800, '', `<g transform="translate(278 30) scale(.72)">${stroke(iconBodies['check-outline'], C.violet800, 2.2)}</g>`), 'Text field filled');
add('field-states', 'needs-attention', '0 0 320 98', `${field('Work email', 'owner@', C.marigold400)}<circle cx="17" cy="86" r="5" fill="${C.marigold400}"/><text x="29" y="91" font-family="${tokens.type.familyUI}" font-size="12" font-weight="650" fill="${C.indigo900}">Enter the complete email address</text>`, 'Field needing attention without red');

const toast = (label, detail, iconBody, accent = C.violet600) => `<rect x="2" y="2" width="336" height="68" rx="18" fill="${C.indigo900}"/><circle cx="37" cy="36" r="20" fill="${accent}"/><g transform="translate(21 20)">${stroke(iconBody, C.white, 2.2)}</g><text x="67" y="31" font-family="${tokens.type.familyUI}" font-size="15" font-weight="750" fill="${C.white}">${esc(label)}</text><text x="67" y="50" font-family="${tokens.type.familyUI}" font-size="12" fill="${C.white}">${esc(detail)}</text>`;
add('feedback', 'saved-toast', '0 0 340 72', toast('Saved', 'Your entrance update is ready.', iconBodies['check-outline']), 'Saved toast');
add('feedback', 'published-toast', '0 0 340 72', toast('Published', 'The map now includes your scan.', iconBodies.storefront, C.violet600), 'Published toast');
add('feedback', 'offline-banner', '0 0 340 72', toast('Saved for later', 'Uploads when you are back online.', iconBodies.receipt, C.sky700), 'Offline banner');
add('feedback', 'camera-permission-dialog', '0 0 340 210', `<rect x="2" y="2" width="336" height="206" rx="24" fill="${C.white}" stroke="${C.indigo900}" stroke-width="2"/><circle cx="170" cy="55" r="32" fill="${C.lavender100}"/><g transform="translate(154 39)">${stroke(iconBodies.camera, C.violet800, 2.3)}</g><text x="170" y="103" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="18" font-weight="750" fill="${C.indigo900}">Allow camera access</text><text x="170" y="127" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="13" fill="${C.indigo900}">Only the doorway is captured.</text><rect x="26" y="145" width="288" height="44" rx="14" fill="${C.marigold400}"/>${labelText('Allow camera', C.indigo900, 170, 174, 15)}`, 'Camera permission dialog');

const sheetState = (id, y, title) => `<rect x="1" y="1" width="238" height="238" rx="26" fill="${C.lavender100}" stroke="${C.indigo900}" stroke-width="2"/><rect x="8" y="${y}" width="224" height="${232-y}" rx="24" fill="${C.white}" stroke="${C.indigo900}" stroke-width="2"/><rect x="98" y="${y+10}" width="44" height="5" rx="3" fill="${C.indigo900}"/><text x="120" y="${y+44}" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="16" font-weight="750" fill="${C.indigo900}">${title}</text>`;
add('sheet-states', 'peek', '0 0 240 240', sheetState('peek', 176, 'Quick view'), 'Bottom sheet peek stop');
add('sheet-states', 'half', '0 0 240 240', sheetState('half', 92, 'Entrance details'), 'Bottom sheet half stop');
add('sheet-states', 'full', '0 0 240 240', sheetState('full', 18, 'Full receipt'), 'Bottom sheet full stop');

const progressState = (percent, stepLabel, complete = false) => {
  const dash = 251.2 * percent;
  return `<circle cx="80" cy="78" r="52" fill="${C.white}" stroke="${C.lavender200}" stroke-width="9"/><circle cx="80" cy="78" r="52" fill="none" stroke="${complete ? C.violet600 : C.marigold400}" stroke-width="9" stroke-linecap="round" stroke-dasharray="${dash} ${251.2-dash}" transform="rotate(-90 80 78)"/><text x="80" y="73" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="25" font-weight="750" fill="${C.indigo900}">${Math.round(percent*100)}%</text><text x="80" y="98" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="11" fill="${C.indigo900}">${esc(stepLabel)}</text>`;
};
add('scan-states', 'progress-start', '0 0 160 156', progressState(.08, 'Doorway framed'), 'Scan progress start');
add('scan-states', 'progress-entry-path', '0 0 160 156', progressState(.42, 'Entry path visible'), 'Scan progress entry path');
add('scan-states', 'progress-quality', '0 0 160 156', progressState(.76, 'Photo quality checked'), 'Scan progress quality');
add('scan-states', 'progress-complete', '0 0 160 156', progressState(1, 'Ready to review', true), 'Scan progress complete');

add('receipt-elements', 'provenance-row-photo', '0 0 380 74', `<rect x="2" y="2" width="376" height="70" rx="14" fill="${C.white}" stroke="${C.lavender200}" stroke-width="2"/><g transform="translate(14 21)">${stroke(iconBodies.photo, C.violet800, 2.2)}</g><text x="58" y="30" font-family="${tokens.type.familyUI}" font-size="14" font-weight="700" fill="${C.indigo900}">Photographed Tuesday</text><text x="58" y="51" font-family="${tokens.type.familyUI}" font-size="13" fill="${C.indigo900}">4 neighbors · 1 owner</text><path d="m350 27 9 10-9 10" fill="none" stroke="${C.violet800}" stroke-width="2.5"/>`, 'Photo provenance receipt row');
add('receipt-elements', 'provenance-row-texas', '0 0 420 74', `<rect x="2" y="2" width="416" height="70" rx="14" fill="${C.white}" stroke="${C.lavender200}" stroke-width="2"/><g transform="translate(14 21)">${texasFlag}</g><text x="58" y="30" font-family="${tokens.type.familyUI}" font-size="14" font-weight="700" fill="${C.indigo900}">Texas accessibility inspection</text><text x="58" y="51" font-family="${tokens.type.familyUI}" font-size="13" fill="${C.indigo900}">On record · 2019 · read-only</text>`, 'Texas provenance receipt row');
add('receipt-elements', 'suggest-correction', '0 0 380 56', `<rect x="2" y="2" width="376" height="52" rx="15" fill="${C.white}" stroke="${C.violet600}" stroke-width="2"/><g transform="translate(17 12)">${stroke(iconBodies.correction, C.violet800, 2.2)}</g><text x="58" y="35" font-family="${tokens.type.familyUI}" font-size="15" font-weight="700" fill="${C.violet800}">Suggest a correction</text><path d="m350 18 9 10-9 10" fill="none" stroke="${C.violet800}" stroke-width="2.5"/>`, 'Suggest a correction receipt action');

const hierarchyPins = (sizes, label) => {
  const entries = [
    { x: 54, size: sizes.estimated, content: `${rings(0, C.sky700)}${pinShape(C.white, C.sky400, true)}${infoIcon}`, name: 'Estimated' },
    { x: 154, size: sizes.scanned, content: `${rings(2, C.marigold400)}${pinShape(C.marigold400, C.white)}${personIcon}`, name: 'Scanned' },
    { x: 260, size: sizes.owner, content: `${rings(3, C.violet600)}${pinShape(C.violet600, C.white)}${storeIcon}`, name: 'Owner' },
  ];
  return `<text x="160" y="20" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="15" font-weight="750" fill="${C.indigo900}">${label}</text>${entries.map(e => `<g transform="translate(${e.x-e.size/2} 31) scale(${e.size/96})">${e.content}</g><text x="${e.x}" y="126" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="11" fill="${C.indigo900}">${e.name} · ${e.size}px</text>`).join('')}`;
};
add('pin-hierarchy', 'overview', '0 0 320 138', hierarchyPins({ estimated: 32, scanned: 36, owner: 40 }, 'Neighborhood overview'), 'Pin hierarchy at overview zoom');
add('pin-hierarchy', 'street', '0 0 320 138', hierarchyPins({ estimated: 40, scanned: 44, owner: 48 }, 'Street-level map'), 'Pin hierarchy at street zoom');
add('pin-hierarchy', 'selected', '0 0 320 148', `<rect width="320" height="148" rx="20" fill="${C.lavender100}"/>${hierarchyPins({ estimated: 52, scanned: 56, owner: 60 }, 'Selected entrance')}<ellipse cx="154" cy="106" rx="37" ry="12" fill="none" stroke="${C.sky400}" stroke-width="3"/><ellipse cx="154" cy="106" rx="26" ry="8" fill="none" stroke="${C.violet600}" stroke-width="2"/>`, 'Selected pin hierarchy with ripple');
add('pin-hierarchy', 'receipt', '0 0 320 138', hierarchyPins({ estimated: 24, scanned: 28, owner: 32 }, 'Cards and receipts'), 'Pin hierarchy in cards and receipts');
add('pin-hierarchy', 'mixed-cluster', '0 0 96 96', `<circle cx="48" cy="48" r="37" fill="${C.indigo900}" stroke="${C.white}" stroke-width="4"/><path d="M23 34a30 30 0 0 1 15-13" fill="none" stroke="${C.sky400}" stroke-width="7" stroke-linecap="round"/><path d="M43 18a30 30 0 0 1 18 3" fill="none" stroke="${C.violet600}" stroke-width="7" stroke-linecap="round"/><path d="M66 25a30 30 0 0 1 7 15" fill="none" stroke="${C.marigold400}" stroke-width="7" stroke-linecap="round"/><text x="48" y="61" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="30" font-weight="750" fill="${C.white}">12</text>`, 'Mixed trust-tier cluster marker', { meaning: 'Count plus tier-composition arcs; never treated as one trust tier' });
add('pin-overlays', 'selected-keyline', '0 0 112 112', `<circle cx="56" cy="56" r="49" fill="none" stroke="${C.white}" stroke-width="8"/><circle cx="56" cy="56" r="52" fill="none" stroke="${C.indigo900}" stroke-width="3"/>`, 'Selected pin keyline overlay');
add('pin-overlays', 'freshness-clock', '0 0 40 40', `<circle cx="20" cy="20" r="17" fill="${C.marigold400}" stroke="${C.white}" stroke-width="3"/>${stroke('<path d="M20 10v11l7 4"/>', C.indigo900, 2.5)}`, 'Freshness clock pin overlay');

mkdir(path.join(root, 'asset-library', 'tokens'));
fs.writeFileSync(path.join(root, 'asset-library', 'tokens', 'pin-hierarchy.json'), JSON.stringify({
  principle: 'Trust tier and contextual prominence are independent. Context may scale a pin but never changes its tier encoding.',
  sizes: tokens.pinHierarchy,
  overlays: {
    selected: 'white keyline + indigo outer line + 12% lift; preserve tier color and icon',
    goodMatch: 'solid halo', partialMatch: 'dashed halo', unknownMatch: 'dotted halo',
    freshness: 'small amber clock; never recolor the pin',
    texasRecord: 'receipt provenance only; never placed on the pin face',
  },
  overlapOrder: ['live scan drop', 'selected', 'needs match', 'owner-confirmed', 'scanned on-site', 'estimated', 'clusters'],
}, null, 2) + '\n');

fs.writeFileSync(path.join(root, 'asset-library', 'tokens', 'design-tokens.json'), JSON.stringify(tokens, null, 2) + '\n');
fs.writeFileSync(path.join(root, 'asset-library', 'tokens', 'variables.css'), `:root {\n${Object.entries(C).map(([k,v]) => `  --entrymap-${k.replace(/[A-Z]/g, m => `-${m.toLowerCase()}`)}: ${v};`).join('\n')}\n  --entrymap-font-ui: ${tokens.type.familyUI};\n  --entrymap-font-wordmark: ${tokens.type.familyWordmark};\n}\n\n@media (prefers-reduced-motion: reduce) {\n  .entrymap-motion { animation: none !important; transition: none !important; }\n}\n`);
fs.writeFileSync(path.join(root, 'asset-library', 'tokens', 'motion.css'), `.entrymap-pin-drop { animation: entrymap-pin-drop 620ms cubic-bezier(.2,.9,.25,1.2) both; }\n@keyframes entrymap-pin-drop {\n  0% { transform: translateY(-48px) scale(.86,1.08); opacity: 0; }\n  62% { transform: translateY(3px) scale(1.08,.91); opacity: 1; }\n  82% { transform: translateY(-4px) scale(.97,1.03); }\n  100% { transform: translateY(0) scale(1); }\n}\n@media (prefers-reduced-motion: reduce) { .entrymap-pin-drop { animation: none; } }\n`);

const rows = assetList.map((a, i) => {
  const x = 28 + (i % 6) * 190;
  const y = 150 + Math.floor(i / 6) * 160;
  const previewFill = a.id.includes('monochrome-light') ? C.indigo900 : C.white;
  return `<g transform="translate(${x} ${y})"><rect width="166" height="132" rx="18" fill="${C.white}" stroke="${C.lavender200}" stroke-width="2"/><rect x="39" y="8" width="88" height="88" rx="12" fill="${previewFill}"/><image href="${a.file.replace('asset-library/', '')}" x="43" y="12" width="80" height="80" preserveAspectRatio="xMidYMid meet"/><text x="83" y="108" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="12" font-weight="700" fill="${C.indigo900}">${esc(a.id)}</text><text x="83" y="124" text-anchor="middle" font-family="${tokens.type.familyUI}" font-size="10" fill="${C.violet800}">${esc(a.category)}</text></g>`;
}).join('');
const sheetH = 180 + Math.ceil(assetList.length / 6) * 160;
fs.writeFileSync(path.join(root, 'asset-library', 'entrymap-asset-catalog.svg'), wrap(`0 0 1200 ${sheetH}`, `<rect width="1200" height="${sheetH}" fill="${C.lavender100}"/><rect x="0" y="0" width="1200" height="118" fill="${C.indigo900}"/><text x="28" y="54" font-family="${tokens.type.familyWordmark}" font-size="38" font-weight="750"><tspan fill="${C.sky400}">entry</tspan><tspan fill="${C.white}">map</tspan></text><text x="28" y="87" font-family="${tokens.type.familyUI}" font-size="17" fill="${C.white}">Production asset library · ${assetList.length} editable SVG masters</text>${rows}`, 'EntryMap asset catalog'));

const manifest = {
  name: 'EntryMap production asset library',
  version: '1.0.0',
  generated: new Date().toISOString(),
  principles: [
    'Sky blue is Estimated; marigold is Scanned on-site; violet is Owner-confirmed.',
    'Every tier is encoded with shape, icon, color, and ring fill.',
    'Texas flag means state-record provenance only and is never a trust tier.',
    'No red, gray, shield, legal compliance claim, or negative state.',
  ],
  assets: assetList.map(({ file, ...rest }) => ({ ...rest, svg: file })),
};
fs.writeFileSync(path.join(root, 'asset-library', 'asset-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');

const readme = `# EntryMap production asset library\n\nThis package contains ${assetList.length} editable SVG masters plus mobile-ready PNG exports. The mockup boards remain at the ZIP root.\n\n## Brand system\n\n- Deep indigo #17103D: app chrome, high-contrast text, dark surfaces.\n- Logo violet #5B35F5: core brand mark, primary icons, Owner-confirmed pins.\n- Sky blue #69B7FF: Estimated pins and informational cues.\n- Marigold #FFBF24: Scanned on-site pins and the Scan action.\n- Pale lavender #F2EEFF: canvas and quiet supporting surfaces.\n- White #FFFFFF: sheets, cards, and dark-surface type.\n\nBody copy uses deep indigo on white or pale lavender. Accent colors are not used for small body text.\n\n## Fixed trust ladder\n\n1. **Estimated**: hollow white pin, dashed sky-blue outline, italic i, 0-of-3 ring.\n2. **Scanned on-site**: solid marigold pin, person icon, 2-of-3 ring.\n3. **Owner-confirmed**: solid violet pin, storefront icon, 3-of-3 ring, separate outlined check.\n\nDo not use shields, the word “verified” for owners, a fourth tier, red, gray, or negative grades. Texas state records are provenance only.\n\n## Folders\n\n- svg/brand: logo, wordmark, app icon, favicon, monochrome variants.\n- svg/pins: the three fixed trust tiers.\n- svg/halos: solid/dashed/dotted needs-match states.\n- svg/ui-icons: navigation, actions, trust, and receipt controls.\n- svg/feature-icons: the seven allowed visually confirmed entrance features plus unknown.\n- svg/provenance: photo, community, owner, public record, and Texas marks.\n- svg/badges: trust, freshness, and confidence components.\n- svg/states: reusable empty, permission, processing, success, offline, and re-check illustrations.\n- svg/motion: pin-drop reference frames.\n- png: raster exports organized by category and size.\n- tokens: JSON and CSS design tokens, including reduced-motion behavior.\n\n## Interaction notes\n\nPins upgrade only. Tapping any claim opens a receipt with source photo, date, method, stacked provenance, freshness, confidence, and “Suggest a correction.” Match halos communicate good/partial/unknown through line style as well as color. The live scan lasts about seven seconds; the pin drop takes 620 ms and collapses to the end state when reduced motion is enabled.\n\n## Type\n\nUse Atkinson Hyperlegible for UI where available, with Aptos/Arial fallbacks. Use Nunito Sans for the joined lowercase EntryMap wordmark when reconstructing it in code; production interfaces should use the supplied SVG wordmarks.\n`;
const interactionReadme = `\n## Interaction component library\n\n- controls: primary, scan, secondary, quiet, pressed, focused, and unavailable states.\n- navigation-states: active Map, Scan, Profile, and keyboard-focus treatments.\n- chip-states: filters plus fresh, aging, and unknown feature claims.\n- field-states: empty, focused, filled, and needs-attention without red.\n- feedback: saved, published, offline, and camera-permission patterns.\n- sheet-states: 18%, 54%, and 92% bottom-sheet stops with a visible drag handle.\n- scan-states: four progress checkpoints for the seven-second scan.\n- receipt-elements: photo, Texas record, and correction rows.\n\n## Pin hierarchy\n\nEvidence controls the base size: Estimated is smallest, Scanned on-site is four pixels larger, and Owner-confirmed is four pixels larger again. Context then scales the entire ladder: overview 32/36/40 px, street 40/44/48 px, selected 52/56/60 px, and receipts 24/28/32 px. The live scan drop briefly uses 64 px before settling. Mixed clusters use a count plus three composition arcs and never masquerade as a single trust tier. See tokens/pin-hierarchy.json.\n`;
fs.writeFileSync(path.join(root, 'asset-library', 'README.md'), readme + interactionReadme);

console.log(JSON.stringify({ root, assetCount: assetList.length, categories: [...new Set(assetList.map(a => a.category))] }, null, 2));
