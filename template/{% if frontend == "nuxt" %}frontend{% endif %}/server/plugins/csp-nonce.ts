import { setResponseHeader } from 'h3'

const NONCE_BYTES = 24
const SCRIPT_TAG = /<script\b/g

// [CSP-NONCE]: every script carries the nonce of its request. `style-src` keeps 'unsafe-inline':
// Vue writes `style` attributes, which a nonce cannot cover. A new third-party domain is added
// here, on its directive, and justified.
function contentSecurityPolicy(nonce: string): string {
  return [
    'default-src \'self\'',
    `script-src 'self' 'nonce-${nonce}' 'strict-dynamic'`,
    'style-src \'self\' \'unsafe-inline\'',
    'img-src \'self\' data:',
    'font-src \'self\'',
    'connect-src \'self\'',
    'object-src \'none\'',
    'base-uri \'self\'',
    'form-action \'self\'',
    'frame-ancestors \'none\''
  ].join('; ')
}

export default defineNitroPlugin((nitroApp) => {
  // In development, Vite's inline scripts and its websocket need no policy. A prerendered page is
  // frozen: no nonce per request, its host sets the policy (hashes of its scripts).
  if (import.meta.dev || import.meta.prerender) return
  nitroApp.hooks.hook('render:html', (html, { event }) => {
    const nonce = btoa(String.fromCharCode(...crypto.getRandomValues(new Uint8Array(NONCE_BYTES))))
    const withNonce = (chunks: string[]) =>
      chunks.map(chunk => chunk.replace(SCRIPT_TAG, `<script nonce="${nonce}"`))
    html.head = withNonce(html.head)
    html.bodyPrepend = withNonce(html.bodyPrepend)
    html.body = withNonce(html.body)
    html.bodyAppend = withNonce(html.bodyAppend)
    setResponseHeader(event, 'Content-Security-Policy', contentSecurityPolicy(nonce))
  })
})
