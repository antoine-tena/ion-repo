import { useEffect, useState } from 'react';

import { APP_DESCRIPTION, APP_TITLE, CORE_CONNECTING, CORE_UNREACHABLE, CORE_VERSION } from './constants';
import { readCoreVersion } from './core';

export function App() {
  const [core, setCore] = useState(CORE_CONNECTING);

  useEffect(() => {
    let isMounted = true;
    async function showCore(): Promise<void> {
      let status = CORE_UNREACHABLE;
      try {
        status = `${CORE_VERSION} ${await readCoreVersion()}`;
      } catch {
        // Outside the app's window (Vite alone in a browser): no core to call.
      }
      if (isMounted) {
        setCore(status);
      }
    }
    void showCore();
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <main className="mx-auto flex min-h-screen max-w-3xl flex-col justify-center gap-4 p-6">
      <h1 className="text-3xl font-bold text-brand">{APP_TITLE}</h1>
      <p className="text-gray-600">{APP_DESCRIPTION}</p>
      <p className="text-gray-500">{core}</p>
    </main>
  );
}
