#!/bin/bash
# Double-click this file to preview the site in your normal browser.
# Close the Terminal window (or press Ctrl-C) when you're done.

cd "$(dirname "$0")" || exit 1

PORT=8765

# Rebuild if the generator is available, otherwise just serve what's there.
if command -v python3 >/dev/null 2>&1; then
  python3 build.py >/dev/null 2>&1 && echo "Rebuilt." || echo "Serving existing dist/ (build skipped)."
fi

if [ ! -d dist ]; then
  echo "No dist/ folder found. Run: python3 build.py"
  read -r -p "Press return to close."
  exit 1
fi

# Free the port if a previous preview is still running.
lsof -ti tcp:$PORT 2>/dev/null | xargs kill 2>/dev/null

cd dist || exit 1
echo ""
echo "  Ash's website is running at  http://localhost:$PORT"
echo "  Leave this window open while you browse."
echo "  Press Ctrl-C to stop."
echo ""

( sleep 1; open "http://localhost:$PORT" ) &
python3 -m http.server $PORT
