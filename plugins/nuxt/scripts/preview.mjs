#!/usr/bin/env node
// Preview of a page on three phones and a computer: one screenshot per device, taken by the
// project's Playwright Chromium (no extra browser to install), so that Claude "sees" a page or
// a dialog the way users do.
//
// Usage, from the frontend directory:
//   node <this script> <path or URL> [--account member] [--wait-for '[role=dialog]']
//                      [--output directory] [--name prefix] [--full-page]
// (The French options of kiln 0.3 are still accepted: --compte, --attendre, --sortie, --nom,
// --pleine-page.)
//
// Reads `.playwright/config` (key=value) and `.playwright/token` at the root of the repo:
//   url=http://localhost:3000        base of relative paths
//   login_<account>=username         account of --account <account> (--account default: login=)
//   login_path=/auth/portal          login page (default); login_next=next: parameter that
//                                    returns to the target page after login
//   username_field / password_field: selectors of the fields (defaults: autocomplete)
//   locale=fr-FR                     browser language (default: the machine's)
//   ready=html[data-hydrated]        element set when the app has taken over (hydration);
//                                    without it, a form submitted too early sends a native GET
// Screenshots go to `.playwright/captures/preview/` by default.
import { existsSync, mkdirSync, readFileSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import { createRequire } from 'node:module'
import { join, resolve } from 'node:path'

// Chosen devices: the best-selling ranges worldwide and the most common screen widths. Presets
// come from Playwright; all run in Chromium (WebKit is not installed): the layout is checked,
// not Safari's engine.
const DEVICES = [
  { name: 'iphone-16', preset: 'iPhone 16' },                 // 393 px, iPhone range
  { name: 'galaxy-a55', preset: 'Galaxy A55' },               // Samsung A series
  { name: 'galaxy-s24', preset: 'Galaxy S24' },               // 360 px, most common mobile width
  { name: 'desktop', viewport: { width: 1920, height: 1080 } } // most common desktop resolution
]
const RENDER_DELAY_MS = 1500
const WAIT_TIMEOUT_MS = 15000
const OPTION_ALIASES = {
  '--compte': '--account',
  '--attendre': '--wait-for',
  '--sortie': '--output',
  '--nom': '--name',
  '--pleine-page': '--full-page'
}
// Config keys of kiln 0.3, still read.
const CONFIG_ALIASES = {
  login_suivant: 'login_next',
  champ_identifiant: 'username_field',
  champ_mot_de_passe: 'password_field',
  pret: 'ready'
}

function readArguments(argv) {
  const options = { target: null, account: null, waitFor: null, output: null, name: 'preview', fullPage: false }
  for (let index = 0; index < argv.length; index += 1) {
    const argument = OPTION_ALIASES[argv[index]] ?? argv[index]
    if (argument === '--account') options.account = argv[++index]
    else if (argument === '--wait-for') options.waitFor = argv[++index]
    else if (argument === '--output') options.output = argv[++index]
    else if (argument === '--name') options.name = argv[++index]
    else if (argument === '--full-page') options.fullPage = true
    else options.target = argument
  }
  if (!options.target) throw new Error('Missing path or URL of the page.')
  return options
}

function repoRoot(start) {
  let directory = resolve(start)
  while (!existsSync(join(directory, '.git'))) {
    const parent = resolve(directory, '..')
    if (parent === directory) return resolve(start)
    directory = parent
  }
  return directory
}

function readConfig(root) {
  const file = join(root, '.playwright', 'config')
  const config = {}
  if (!existsSync(file)) return config
  for (const line of readFileSync(file, 'utf8').split('\n')) {
    const clean = line.trim()
    if (!clean || clean.startsWith('#') || !clean.includes('=')) continue
    const position = clean.indexOf('=')
    const key = clean.slice(0, position).trim()
    config[CONFIG_ALIASES[key] ?? key] = clean.slice(position + 1).trim()
  }
  return config
}

// Login through the login page, with the target page as return parameter (`next`): we land
// there logged in without reloading, so the session the app keeps in memory stays valid.
async function logIn(page, base, config, root, account, target) {
  const key = account === 'default' || account === 'defaut' ? 'login' : `login_${account}`
  const username = config[key]
  if (!username) throw new Error(`No ${key}= in .playwright/config.`)
  const password = readFileSync(join(root, '.playwright', 'token'), 'utf8').trim()
  const portal = config.login_path ?? '/auth/portal'
  const address = new URL(portal, base)
  address.searchParams.set(config.login_next ?? 'next', target.pathname + target.search)
  await page.goto(address.href, { waitUntil: 'load' })
  await waitUntilReady(page, config)
  await page.locator(config.username_field ?? 'input[autocomplete=username]').first().fill(username)
  const field = page.locator(config.password_field ?? 'input[autocomplete=current-password]').first()
  await field.fill(password)
  await field.press('Enter')
  await page.waitForURL(url => !url.pathname.startsWith(portal), { timeout: WAIT_TIMEOUT_MS })
}

async function waitUntilReady(page, config) {
  if (config.ready) await page.locator(config.ready).waitFor({ state: 'attached', timeout: WAIT_TIMEOUT_MS })
}

// A single page, which takes the shape of each device in turn (size, density, touch, mobile
// browser): one login per run, and a dialog opened once is captured on all four. Limit: what
// the server renders according to the browser stays that of the first load; the layout
// follows each screen.
async function emulate(session, devices, device, defaultAgent) {
  const profile = device.preset ? devices[device.preset] : { viewport: device.viewport, deviceScaleFactor: 1 }
  await session.send('Emulation.setDeviceMetricsOverride', {
    width: profile.viewport.width,
    height: profile.viewport.height,
    deviceScaleFactor: profile.deviceScaleFactor ?? 1,
    mobile: Boolean(profile.isMobile)
  })
  await session.send('Emulation.setTouchEmulationEnabled', { enabled: Boolean(profile.hasTouch) })
  await session.send('Emulation.setUserAgentOverride', { userAgent: profile.userAgent ?? defaultAgent })
}

async function capture(page, session, devices, device, options, output, defaultAgent) {
  await emulate(session, devices, device, defaultAgent)
  await page.waitForTimeout(RENDER_DELAY_MS)
  const file = join(output, `${options.name}-${device.name}.png`)
  await page.screenshot({ path: file, fullPage: options.fullPage })
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)
  return { file, overflow }
}

// The Chromium expected by the project's Playwright version installs on first run (a few
// seconds afterwards): a new machine or a Playwright upgrade has nothing to do.
async function launchChromium(chromium) {
  try {
    return await chromium.launch()
  } catch (error) {
    if (!String(error.message).includes('Executable doesn')) throw error
    execFileSync('npx', ['playwright', 'install', 'chromium'], { stdio: 'ignore' })
    return chromium.launch()
  }
}

async function main() {
  const options = readArguments(process.argv.slice(2))
  const root = repoRoot(process.cwd())
  const config = readConfig(root)
  const load = createRequire(join(process.cwd(), 'package.json'))
  const { chromium, devices } = load('@playwright/test')
  const base = config.url ?? 'http://localhost:3000'
  const url = new URL(options.target, base).href
  const output = resolve(options.output ?? join(root, '.playwright', 'captures', 'preview'))
  mkdirSync(output, { recursive: true })
  const browser = await launchChromium(chromium)
  try {
    // No size imposed by Playwright: the emulation of each device gives it.
    const context = await browser.newContext({ locale: config.locale ?? Intl.DateTimeFormat().resolvedOptions().locale, viewport: null })
    const page = await context.newPage()
    const session = await context.newCDPSession(page)
    const target = new URL(url)
    if (options.account !== null) await logIn(page, base, config, root, options.account, target)
    else await page.goto(url, { waitUntil: 'load', timeout: WAIT_TIMEOUT_MS * 2 })
    await waitUntilReady(page, config)
    if (options.waitFor) await page.locator(options.waitFor).first().waitFor({ timeout: WAIT_TIMEOUT_MS })
    const defaultAgent = await page.evaluate(() => navigator.userAgent)
    for (const device of DEVICES) {
      const { file, overflow } = await capture(page, session, devices, device, options, output, defaultAgent)
      console.log(`${device.name}\t${file}${overflow ? '\tHORIZONTAL OVERFLOW' : ''}`)
    }
  } finally {
    await browser.close()
  }
}

main().catch((error) => {
  console.error(`preview: ${error.message}`)
  process.exit(1)
})
