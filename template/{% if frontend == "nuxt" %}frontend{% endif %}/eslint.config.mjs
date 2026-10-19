// @ts-check
// Rules of the charter that ESLint can check, on top of @nuxt/eslint's configuration.
import withNuxt from './.nuxt/eslint.config.mjs'

export default withNuxt(
  {
    rules: {
      // [NO-ANY]: `unknown`, then a type narrowing.
      '@typescript-eslint/no-explicit-any': 'error',
    },
  },
  {
    // [API-CALLS]: a component or a page goes through a composable of its domain.
    files: ['**/*.vue'],
    rules: {
      'no-restricted-globals': ['error', { name: '$fetch', message: 'Passer par un composable (CLAUDE.md [APPELS-API]).' }],
      'no-restricted-syntax': ['error', {
        selector: "CallExpression[callee.name=/^(useApi|useFetch)$/]",
        message: 'Passer par un composable (CLAUDE.md [APPELS-API]).',
      }],
    },
  },
)
