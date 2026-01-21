#! /bin/zsh


BASE_DIR="/home/andriomdac/FastAPIOpiniated/"


xfce4-terminal \
  --title="shell" \
  --working-directory="$BASE_DIR" \
  --command="zsh -c 'source ./api/.venv/bin/activate; exec zsh'" &
xfce4-terminal \
  --title="nvim" \
  --working-directory="$BASE_DIR" \
  --command="zsh -c 'source ./api/.venv/bin/activate && nvim .; exec zsh'" &
# xfce4-terminal \
#   --title="docker" \
#   --working-directory="$BASE_DIR" \
#   --command="zsh -c 'docker-compose up --build; exec zsh'" &
xfce4-terminal \
  --title="posting" \
  --working-directory="$BASE_DIR/api/" \
  --command="zsh -c 'source .venv/bin/activate && posting; exec zsh'" &
xfce4-terminal \
  --title="fastapi server" \
  --working-directory="$BASE_DIR/api/" \
  --command="zsh -c 'source .venv/bin/activate && fastapi dev main.py; exec zsh'" &
