// Rules of the charter that ESLint can check, on top of Astro's and typescript-eslint's.
import { defineConfig, globalIgnores } from "eslint/config";
import astro from "eslint-plugin-astro";
import tseslint from "typescript-eslint";

export default defineConfig([
  ...tseslint.configs.recommended,
  ...astro.configs.recommended,
  {
    rules: {
      // [NO-ANY]: `unknown`, then a type narrowing.
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
  globalIgnores(["dist/**", ".astro/**"]),
]);
