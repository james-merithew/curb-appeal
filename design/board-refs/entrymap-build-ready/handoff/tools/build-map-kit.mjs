import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const root = path.resolve(process.argv[2] || '.');
const svgDir = path.join(root, 'map-kit', 'svg');
fs.mkdirSync(svgDir, { recursive: true });

const C = {
  indigo: '#1E1142', violet: '#4F34DB', sky: '#76BCFD', marigold: '#FDB327',
  path: '#CFBCEE', lavender: '#F5F2FC', lavender2: '#E8E1F7', white: '#FFFFFF'
};
const pinHref = id => `../../asset-library/svg/pins/${id}.svg`;
const haloHref = id => `../../asset-library/svg/halos/${id}.svg`;

function defs() {
  return `<defs>
    <filter id="lift" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="${C.indigo}" flood-opacity=".20"/></filter>
    <pattern id="paper" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="3" cy="3" r=".8" fill="${C.violet}" opacity=".045"/></pattern>
  </defs>`;
}

function mapBase() {
  return `<g id="land"><rect width="1170" height="800" rx="42" fill="${C.lavender}"/><rect width="1170" height="800" rx="42" fill="url(#paper)"/></g>
  <g id="blocks" fill="${C.lavender2}" stroke="${C.path}" stroke-width="3">
    <path d="M45 48H300L270 208H35Z"/><path d="M355 45H615L585 205H325Z"/><path d="M670 40H1115L1080 200H640Z"/>
    <path d="M25 275H250L225 470H20Z"/><path d="M310 272H535L515 470H285Z"/><path d="M600 265H820L798 468H575Z"/><path d="M885 258H1145L1122 463H860Z"/>
    <path d="M35 545H360L330 760H20Z"/><path d="M425 540H760L735 760H395Z"/><path d="M825 535H1148L1125 758H795Z"/>
  </g>
  <g id="roads" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M-20 235C260 255 540 245 1190 220" stroke="${C.path}" stroke-width="62" opacity=".55"/>
    <path d="M-20 235C260 255 540 245 1190 220" stroke="${C.white}" stroke-width="48"/>
    <path d="M270 -20C285 250 275 505 370 830" stroke="${C.path}" stroke-width="62" opacity=".55"/>
    <path d="M270 -20C285 250 275 505 370 830" stroke="${C.white}" stroke-width="48"/>
    <path d="M610 -30C600 230 590 520 760 830" stroke="${C.path}" stroke-width="62" opacity=".55"/>
    <path d="M610 -30C600 230 590 520 760 830" stroke="${C.white}" stroke-width="48"/>
    <path d="M-30 510C340 490 690 500 1200 485" stroke="${C.path}" stroke-width="62" opacity=".55"/>
    <path d="M-30 510C340 490 690 500 1200 485" stroke="${C.white}" stroke-width="48"/>
  </g>
  <g id="places" fill="${C.sky}" opacity=".34"><circle cx="92" cy="98" r="24"/><circle cx="1040" cy="675" r="42"/><circle cx="960" cy="88" r="20"/><path d="M990 600c45-30 88-20 115 18-5 58-48 91-108 75-20-27-21-62-7-93Z"/></g>
  <g id="labels" fill="${C.indigo}" font-family="Atkinson Hyperlegible, Arial, sans-serif" font-weight="700" letter-spacing="3">
    <text x="455" y="227" font-size="24" transform="rotate(-2 455 227)">WILLOW ST</text>
    <text x="330" y="420" font-size="22" transform="rotate(82 330 420)">5TH AVE</text>
    <text x="672" y="420" font-size="22" transform="rotate(83 672 420)">OAK ALLEY</text>
  </g>`;
}

function image(href, x, y, w, h, id = '') { return `<image${id ? ` id="${id}"` : ''} href="${href}" x="${x}" y="${y}" width="${w}" height="${h}"/>`; }
function pins(withHalos = false, selected = false) {
  return `<g id="halos">${withHalos ? `${image(haloHref('unknown-match'),168,283,96,96)}${image(haloHref('partial-match'),522,329,108,108)}${image(haloHref('good-match'),834,280,120,120)}` : ''}</g>
  <g id="pins" filter="url(#lift)">
    ${image(pinHref('estimated'),180,290,72,78,'pin-estimated')}
    ${image(pinHref('scanned-on-site'),535,337,82,90,'pin-scanned')}
    ${image(pinHref('owner-confirmed'),850,288,92,100,'pin-owner')}
  </g>
  <g id="selection">${selected ? `<circle cx="576" cy="380" r="66" fill="none" stroke="${C.white}" stroke-width="10"/><circle cx="576" cy="380" r="73" fill="none" stroke="${C.indigo}" stroke-width="4"/>` : ''}</g>`;
}

function emptyCard() {
  return `<g id="annotations" filter="url(#lift)"><rect x="330" y="250" width="510" height="285" rx="36" fill="${C.white}" stroke="${C.path}" stroke-width="4"/>
  ${image(pinHref('estimated'),535,275,100,110)}
  <text x="585" y="420" text-anchor="middle" fill="${C.indigo}" font-family="Atkinson Hyperlegible, Arial, sans-serif" font-size="31" font-weight="700">No entrances mapped here yet</text>
  <text x="585" y="460" text-anchor="middle" fill="${C.indigo}" font-family="Atkinson Hyperlegible, Arial, sans-serif" font-size="21">Be the first to help neighbors plan ahead.</text>
  <rect x="420" y="485" width="330" height="52" rx="22" fill="${C.marigold}"/><text x="585" y="519" text-anchor="middle" fill="${C.indigo}" font-family="Atkinson Hyperlegible, Arial, sans-serif" font-size="22" font-weight="700">Scan an entrance</text></g>`;
}

function cluster() {
  return `<g id="pins" filter="url(#lift)"><circle cx="585" cy="385" r="76" fill="${C.indigo}" stroke="${C.white}" stroke-width="8"/><path d="M535 335a70 70 0 0 1 45-23" fill="none" stroke="${C.sky}" stroke-width="13" stroke-linecap="round"/><path d="M592 313a70 70 0 0 1 45 23" fill="none" stroke="${C.marigold}" stroke-width="13" stroke-linecap="round"/><path d="M644 350a70 70 0 0 1 5 48" fill="none" stroke="${C.violet}" stroke-width="13" stroke-linecap="round"/><text x="585" y="405" text-anchor="middle" fill="${C.white}" font-family="Atkinson Hyperlegible, Arial, sans-serif" font-size="50" font-weight="800">12</text></g>`;
}

function placement() {
  return `${pins(true,false)}<g id="annotations" fill="${C.indigo}" font-family="Atkinson Hyperlegible, Arial, sans-serif"><path d="M216 390v90" stroke="${C.indigo}" stroke-width="3" stroke-dasharray="7 7"/><path d="M576 438v70" stroke="${C.indigo}" stroke-width="3" stroke-dasharray="7 7"/><path d="M896 398v82" stroke="${C.indigo}" stroke-width="3" stroke-dasharray="7 7"/><text x="216" y="510" text-anchor="middle" font-size="22">anchor: entrance threshold</text><text x="576" y="538" text-anchor="middle" font-size="22">halo sits outside trust pin</text><text x="896" y="510" text-anchor="middle" font-size="22">tier controls base size</text></g>`;
}

function safeAreas() {
  return `<g id="annotations" font-family="Atkinson Hyperlegible, Arial, sans-serif"><rect x="0" y="0" width="1170" height="104" fill="${C.indigo}" opacity=".92"/><text x="40" y="64" fill="${C.white}" font-size="26" font-weight="700">App chrome / search / filters</text><rect x="0" y="535" width="1170" height="265" fill="${C.white}" opacity=".92" stroke="${C.violet}" stroke-width="4"/><text x="40" y="590" fill="${C.indigo}" font-size="26" font-weight="700">Bottom-sheet zone</text><rect x="36" y="126" width="1098" height="380" rx="30" fill="none" stroke="${C.marigold}" stroke-width="6" stroke-dasharray="16 12"/><text x="585" y="165" text-anchor="middle" fill="${C.indigo}" font-size="24" font-weight="700">Keep selected pins inside this visible map zone</text></g>`;
}

const variants = [
  ['base-map', 'Editable base with stable map layers', ''],
  ['before-profile', 'Trust pins before a needs profile is applied', pins(false,false)],
  ['after-profile', 'The same pins with solid/dashed/dotted match halos', pins(true,false)],
  ['selected-business', 'Selected Scanned on-site entrance with independent keyline', pins(true,true)],
  ['empty-area', 'Invitation-led empty-area state', emptyCard()],
  ['mixed-cluster', 'Mixed evidence cluster with composition arcs', cluster()],
  ['pin-placement', 'Pin anchors, hierarchy, and halo placement', placement()],
  ['safe-areas', 'Map visibility zones beneath chrome and sheets', safeAreas()]
];

for (const [id, description, overlay] of variants) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1170 800" role="img" aria-labelledby="title desc"><title id="title">EntryMap ${id}</title><desc id="desc">${description}</desc>${defs()}${mapBase()}${overlay || '<g id="halos"/><g id="pins"/><g id="selection"/><g id="annotations"/>'}</svg>`;
  fs.writeFileSync(path.join(svgDir, `${id}.svg`), svg, 'utf8');
}

const manifest = {
  version: 1,
  dimensions: { width: 1170, height: 800 },
  disclaimer: 'Illustrative demo artwork only; not geographic truth, routing data, or a production map provider.',
  layers: ['land','blocks','roads','labels','places','halos','pins','selection','annotations'],
  canonicalColors: C,
  variants: variants.map(([id, description]) => ({ id, description, svg: `map-kit/svg/${id}.svg`, png: `map-kit/png/${id}.png` }))
};
fs.writeFileSync(path.join(root, 'map-kit', 'map-kit-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
console.log(JSON.stringify({ result: 'PASS', variants: variants.length }));
