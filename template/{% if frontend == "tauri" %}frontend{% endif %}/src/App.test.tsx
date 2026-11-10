import { renderToString } from 'react-dom/server';
import { describe, expect, it } from 'vitest';

import { App } from './App';
import { APP_TITLE } from './constants';

describe('App', () => {
  it('shows the title of the app', () => {
    expect(renderToString(<App />)).toContain(APP_TITLE);
  });
});
