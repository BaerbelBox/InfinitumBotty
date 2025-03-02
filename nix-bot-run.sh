#! /usr/bin/env nix-shell
#! nix-shell -i bash -p bash python312Packages.wikipedia python312Packages.requests

# Directory of the virtual environment
#VENV="./FaustBotVEnv"

venv() {
  :
}

help() {
  echo "Simple script to manage a single faust-bot instance."
  echo "  -h  displays this help message"
  echo "  -s  starts the bot, if it is not running yet"
  echo "  -e  exits/stops the bot"
  echo "  -r  restarts the bot"
  echo "  -u  updates the bots code"
}

start() {
  venv
  echo "[=== checking if bot is already running "
  if [ -f ".pid" ]; then
    echo "[=== bot is already running "
    echo "[=== aborting start "
  else
    echo "[=== bot is not running "
    echo "[=== check if out.txt exists "
    if [ -f "out.txt" ]; then
      echo "[=== removing existing out.txt "
      rm out.txt
    else
      echo "[=== no out.txt found "
    fi
    echo "[=== checking if database already exists "
    if [ -f "faust_bot.db" ]; then
      echo "[=== database already exists "
    else
      echo "[=== no database "
      echo "[=== preparing database "
      python ReadInternationalization.py
    fi
    echo "[=== starting faust-bot "
    echo "[=== redirecting output to nohup.out "
    nohup python -u Main.py --config config.txt >out.txt &
    echo "[=== pid of bot process can be found in .pid "
    echo $! >.pid
  fi
}

stop() {
  echo "[=== checking if bot is running "
  if [ ! -f ".pid" ]; then
    echo "[=== bot is not running "
  else
    echo "[=== bot is running "
    echo "[=== killing bot process "
    kill "$(cat .pid)"
    echo "[=== removing .pid file "
    rm .pid
  fi
}

update() {
  echo "[=== stopping the bot to update it "
  stop
  echo "[=== stashing local changes "
  git stash --all
  echo "[=== update the code "
  git pull origin main
  echo "[=== reapply done local changes "
  git stash pop
  echo "[=== restarting bot instance "
  start
}

clean() {
  echo "[=== cleaning files "
  echo "[=== stopping the bot "
  stop
  echo "[=== removing output file "
  rm out.txt
  echo "[=== removing venv "
  rm -rf $VENV
}

OPTIND=1

while getopts "hseruc" opt; do
  case $opt in
  h)
    help
    exit
    ;;
  s)
    start
    ;;
  e)
    stop
    ;;
  r)
    stop
    start
    ;;
  u)
    update
    ;;
  c)
    clean
    ;;
  \?)
    echo "Invalid option: -$OPTARG" >&2
    help
    ;;
  esac
done
