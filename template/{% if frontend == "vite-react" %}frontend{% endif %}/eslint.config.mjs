// Rules of the charter that ESLint can check, on top of typescript-eslint's and React's hooks.
import { defineConfig, globalIgnores } from "eslint/config";
import reactHooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";

export default defineConfig([
  ...tseslint.configs.recommended,
  reactHooks.configs.flat.recommended,
  {
    rules: {
      // [NO-ANY]: `unknown`, then a type narrowing.
      "@typescript-eslint/no-explicit-any": "error",
    },
  },
  globalIgnores(["dist/**"]),
]);
