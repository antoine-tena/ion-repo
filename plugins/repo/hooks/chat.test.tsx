import { expect, test } from 'claude-code/testing'

// The bar is the first child of the row the mod draws.
const barColor = async (ui: { find: (q: object) => Promise<any> }) =>
  (await ui.find({ type: 'Box' }))?.children?.[0]?.props?.backgroundColor

const NOON = new Date(2026, 10, 3, 12, 5).getTime()

const userMessage = (requestId: string, origin: object, from?: object) => ({
  plugin: 'repo',
  component: 'UserMessage',
  requestId,
  surface: 'terminal',
  props: { text: 'hello', origin, isExpanded: false, ...(from === undefined ? {} : { from }) },
} as const)

const ran = (stdout: string) => ({ value: { exitCode: stdout === '' ? 1 : 0, stdout, stderr: '' } })

// No ~/.claude/chat-names.json: git's user.name and "Claude".
const GIT_NAME = (_: unknown, e: { argv: string[] }) =>
  ran(e.argv[0] === 'git' ? 'antoine-tena\n' : '')

test("the person's message gets a blue bar, their git name and the time", async ($, on) => {
  on('clock.now', () => ({ value: NOON }))
  on('process.run', GIT_NAME)
  const ui = await $.ui.mount(userMessage('m1', { kind: 'unclassified' }))
  expect((await ui.find({ type: 'Text', text: /12:05/ }))?.text).toBe('12:05')
  expect((await ui.find({ type: 'Text', text: /antoine-tena/ }))?.text).toBe('antoine-tena')
  expect(await barColor(ui)).toBe('professionalBlue')
  await ui.unmount()
})

test("the person's message typed in the prompt box gets a blue bar, not 'composer'", async ($, on) => {
  on('clock.now', () => ({ value: NOON }))
  on('process.run', GIT_NAME)
  const ui = await $.ui.mount(userMessage('m3', { kind: 'composer' }))
  expect(await ui.find({ type: 'Text', text: /composer/ })).toBeUndefined()
  expect(await barColor(ui)).toBe('professionalBlue')
  await ui.unmount()
})

test('a message from another session gets a gray bar and its name', async ($, on) => {
  on('clock.now', () => ({ value: NOON }))
  const ui = await $.ui.mount(userMessage('m2', { kind: 'peer' }, { name: 'ion-host' }))
  expect((await ui.find({ type: 'Text', text: /ion-host/ }))?.text).toBe('ion-host')
  expect(await barColor(ui)).toBe('inactive')
  await ui.unmount()
})

test("Claude's reply gets a bar in Claude's color and Claude's name", async ($, on) => {
  on('clock.now', () => ({ value: NOON }))
  on('process.run', GIT_NAME)
  const ui = await $.ui.mount({
    plugin: 'repo',
    component: 'AssistantMessage',
    requestId: 'r1',
    surface: 'terminal',
    props: { text: 'done', isFirstOfReply: true },
  })
  expect((await ui.find({ type: 'Text', text: /^Claude$/ }))?.text).toBe('Claude')
  expect(await barColor(ui)).toBe('claude')
  await ui.unmount()
})

test('the names chosen with /repo:names replace the real ones', async ($, on) => {
  // Later than the names read by the tests above, so they are read again.
  on('clock.now', () => ({ value: NOON + 3_600_000 }))
  on('process.run', (_, e) =>
    e.argv[0] === 'git' ? ran('antoine-tena') : ran('{"person": "Antoine", "claude": "Ion"}'),
  )
  const ui = await $.ui.mount(userMessage('m4', { kind: 'composer' }))
  expect((await ui.find({ type: 'Text', text: /^Antoine$/ }))?.text).toBe('Antoine')
  await ui.unmount()
  const reply = await $.ui.mount({
    plugin: 'repo',
    component: 'AssistantMessage',
    requestId: 'r2',
    surface: 'terminal',
    props: { text: 'done', isFirstOfReply: true },
  })
  expect((await reply.find({ type: 'Text', text: /^Ion$/ }))?.text).toBe('Ion')
  await reply.unmount()
})

test("Claude's reply shows the time on its name's line, the first of the reply only", async ($, on) => {
  on('clock.now', () => ({ value: NOON }))
  on('process.run', GIT_NAME)
  const first = await $.ui.mount({
    plugin: 'repo',
    component: 'AssistantMessage',
    requestId: 'r3',
    surface: 'terminal',
    props: { text: 'done', isFirstOfReply: true },
  })
  expect((await first.find({ type: 'Text', text: /12:05/ }))?.text).toBe('12:05')
  await first.unmount()
  const next = await $.ui.mount({
    plugin: 'repo',
    component: 'AssistantMessage',
    requestId: 'r4',
    surface: 'terminal',
    props: { text: 'more', isFirstOfReply: false },
  })
  expect(await next.find({ type: 'Text', text: /12:05/ })).toBeUndefined()
  await next.unmount()
})

test('a message first drawn another day shows its date before the time', async ($, on) => {
  let now = new Date(2026, 10, 2, 21, 11).getTime()
  on('clock.now', () => ({ value: now }))
  on('process.run', GIT_NAME)
  const yesterday = await $.ui.mount(userMessage('m5', { kind: 'composer' }))
  expect((await yesterday.find({ type: 'Text', text: /21:11/ }))?.text).toBe('21:11')
  await yesterday.unmount()
  now = NOON
  const today = await $.ui.mount(userMessage('m5', { kind: 'composer' }))
  expect((await today.find({ type: 'Text', text: /21:11/ }))?.text).toBe('2 nov. 21:11')
  await today.unmount()
})
