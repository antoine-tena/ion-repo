// Draws a colored bar beside each message of the chat: blue for the person, Claude's color for
// Claude, gray for what came from elsewhere (another session, a task, a schedule), with its name.
// Colors are theme keys, so a custom theme (`/theme`) changes them.
import type { Register } from 'claude-code'

type Origin = { kind: string; server?: string; plugin?: string }

const PERSON_KINDS = new Set(['unclassified', 'bridge', 'sdk'])

const firstSeen = new Map<string, number>()

const clockTime = (ms: number): string => {
  const at = new Date(ms)
  return `${String(at.getHours()).padStart(2, '0')}:${String(at.getMinutes()).padStart(2, '0')}`
}

const seenAt = async (now: () => Promise<number>, id: string): Promise<string> => {
  if (!firstSeen.has(id)) {
    firstSeen.set(id, await now())
  }
  return clockTime(firstSeen.get(id) as number)
}

const sender = (origin: Origin, from?: { name?: string }): string | null => {
  if (PERSON_KINDS.has(origin.kind)) {
    return null
  }
  return from?.name ?? origin.plugin ?? origin.server ?? origin.kind
}

export const register: Register = on => {
  on('ui.render', { component: 'UserMessage' }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const name = sender(e.props.origin, e.props.from)
    const time = await seenAt(() => $.clock.now(), e.requestId)

    return (
      <Box flexDirection="row" marginTop={1}>
        <Box width={1} backgroundColor={name === null ? 'professionalBlue' : 'inactive'} />
        <Box flexDirection="column" flexGrow={1} marginLeft={1}>
          <Box flexDirection="row">
            {name === null ? null : <Text bold color="inactive">{name}</Text>}
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
    const { Box, Markdown } = $.ui.resolve(e)

    return (
      <Box flexDirection="row" marginTop={e.props.isFirstOfReply ? 1 : 0}>
        <Box width={1} backgroundColor="claude" />
        <Box flexDirection="column" flexGrow={1} marginLeft={1}>
          <Markdown text={e.props.text} />
        </Box>
      </Box>
    )
  })
}
