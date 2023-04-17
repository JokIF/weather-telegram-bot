#!/usr/bin/env bash
set -e

poetry="poetry run"

${poetry} alembic upgrade head

${poetry} pybabel compile -D "SQLW" -d ./locales

starter="exec ${poetry} python -O -m main_bot"

case "$1" in
  start)
      ${starter} start
      ;;

  *)
    "$@"

esac
