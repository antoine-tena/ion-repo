// Draws a colored bar beside each message of the chat: blue for the person, Claude's color for
// Claude, each under its name; gray for what came from elsewhere (another session, a task, a
// schedule), with its name. Colors are theme keys, so a custom theme (`/theme`) changes them.
// Names come from ~/.claude/chat-names.json (`/repo:names`), else git's user.name and "Claude".
// The time beside the name is when the message was first drawn: neither the props nor
// `$.session.messages` carry the message's own time, so a resumed session shows the resume's.
import type { Register } from 'claude-code'

type Origin = { kind: string; server?: string; plugin?: string }
type Names = { person: string; claude: string }
type Run = { exitCode: number; stdout: string }

const PERSON_KINDS = new Set(['unclassified', 'composer', 'bridge', 'sdk'])
const NAMES_FILE = '"$HOME/.claude/chat-names.json"'
// Names read again after this long, so a change by `/repo:names` shows without a restart.
const NAMES_TTL_MS = 10_000

const firstSeen = new Map<string, number>()
let names: { at: number; value: Promise<Names> } | undefined

const MONTHS = ['janv.', 'févr.', 'mars', 'avr.', 'mai', 'juin', 'juil.', 'août', 'sept.', 'oct.', 'nov.', 'déc.']

// HH:MM today, "2 nov. 21:11" another day.
const clockTime = (ms: number, nowMs: number): string => {
  const at = new Date(ms)
  const today = new Date(nowMs)
  const time = `${String(at.getHours()).padStart(2, '0')}:${String(at.getMinutes()).padStart(2, '0')}`
  return at.toDateString() === today.toDateString()
    ? time
    : `${at.getDate()} ${MONTHS[at.getMonth()]} ${time}`
}

const seenAt = async (now: () => Promise<number>, id: string): Promise<string> => {
  const current = await now()
  if (!firstSeen.has(id)) {
    firstSeen.set(id, current)
  }
  return clockTime(firstSeen.get(id) as number, current)
}

const output = (result: Run): string => (result.exitCode === 0 ? result.stdout.trim() : '')

const chosen = (text: string): Partial<Names> => {
  try {
    const parsed = JSON.parse(text)
    return typeof parsed === 'object' && parsed !== null ? parsed : {}
  } catch {
    return {}
  }
}

const named = (value: unknown, fallback: string): string =>
  typeof value === 'string' && value.trim() !== '' ? value.trim() : fallback

const toNames = (file: string, gitName: string): Names => {
  const choice = chosen(file)
  return { person: named(choice.person, gitName), claude: named(choice.claude, 'Claude') }
}

const sender = (origin: Origin, from?: { name?: string }): string | null => {
  if (PERSON_KINDS.has(origin.kind)) {
    return null
  }
  return from?.name ?? origin.plugin ?? origin.server ?? origin.kind
}

export const register: Register = on => {
  const currentNames = async (now: number, read: () => Promise<Names>): Promise<Names> => {
    if (names === undefined || now - names.at > NAMES_TTL_MS) {
      names = { at: now, value: read() }
    }
    return names.value
  }

  const readNames = (run: (argv: string[]) => Promise<Run>): Promise<Names> =>
    Promise.all([
      run(['sh', '-c', `cat ${NAMES_FILE} 2>/dev/null`]).then(output, () => ''),
      run(['git', 'config', 'user.name']).then(output, () => ''),
    ]).then(([file, gitName]) => toNames(file, gitName))

  on('ui.render', { component: 'UserMessage' }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const name = sender(e.props.origin, e.props.from)
    const time = await seenAt(() => $.clock.now(), e.requestId)
    const label =
      name ??
      (await currentNames(await $.clock.now(), () => readNames(argv => $.process.run(argv)))).person

    return (
      <Box flexDirection="row" marginTop={1}>
        <Box width={1} backgroundColor={name === null ? 'professionalBlue' : 'inactive'} />
        <Box flexDirection="column" flexGrow={1} marginLeft={1}>
          <Box flexDirection="row">
            {label === '' ? null : (
              <Text bold color={name === null ? 'professionalBlue' : 'inactive'}>{label}</Text>
            )}
            <Box flexGrow={1} />
            <Text dimColor>{time}</Text>
          </Box>
          <Text dimColor={name !== null}>{e.props.text}</Text>
        </Box>
      </Box>
    )
  })

  on('ui.render', { component: 'AssistantMessage' }, async ($, e, next) => {
    if (e.props.isSummary === true) {
      return next(e)
    }
    const { Box, Markdown, Text } = $.ui.resolve(e)
    const label = e.props.isFirstOfReply
      ? (await currentNames(await $.clock.now(), () => readNames(argv => $.process.run(argv))))
          .claude
      : null
    const time = e.props.isFirstOfReply ? await seenAt(() => $.clock.now(), e.requestId) : null

    return (
      <Box flexDirection="row" marginTop={e.props.isFirstOfReply ? 1 : 0}>
        <Box width={1} backgroundColor="claude" />
        <Box flexDirection="column" flexGrow={1} marginLeft={1}>
          {label === null ? null : (
            <Box flexDirection="row">
              <Text bold color="claude">{label}</Text>
              <Box flexGrow={1} />
              <Text dimColor>{time}</Text>
            </Box>
          )}
          <Markdown text={e.props.text} />
        </Box>
      </Box>
    )
  })
}
