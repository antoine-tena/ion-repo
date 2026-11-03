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

const GIT_NAME = { value: { exitCode: 0, stdout: 'antoine-tena\n', stderr: '' } }

test("the person's message gets a blue bar, their git name and the time", async ($, on) => {
  on('clock.now', () => ({ value: NOON }))
  on('process.run', () => GIT_NAME)
  const ui = await $.ui.mount(userMessage('m1', { kind: 'unclassified' }))
  expect((await ui.find({ type: 'Text', text: /12:05/ }))?.text).toBe('12:05')
  expect((await ui.find({ type: 'Text', text: /antoine-tena/ }))?.text).toBe('antoine-tena')
  expect(await barColor(ui)).toBe('professionalBlue')
  await ui.unmount()
})

test("the person's message typed in the prompt box gets a blue bar, not 'composer'", async ($, on) => {
  on('clock.now', () => ({ value: NOON }))
  on('process.run', () => GIT_NAME)
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

test("Claude's reply gets a bar in Claude's color", async $ => {
  const ui = await $.ui.mount({
    plugin: 'repo',
    component: 'AssistantMessage',
    requestId: 'r1',
    surface: 'terminal',
    props: { text: 'done', isFirstOfReply: true },
  })
  expect(await barColor(ui)).toBe('claude')
  await ui.unmount()
})
