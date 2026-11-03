echo "Starting Docker Installer..."

# NOTE: make sure you are in a SAFE folder to install Mini Music

mkdir minimusic-app
cd minimusic-app

# install python
ensure sudo apt install python3 python3-pip python3-venv python3-dev

docker pull ghcr.io/minimusic-app/minimusic:latest
echo "Running MiniMusic image"
docker run minimusic:latest

local $dir

echo ""
echo "Installation directory: $dir"
echo ""
echo "Installation completed successfully! 🎉"
echo "To use MiniMusic open http://localhost:8000 in your browser to start Mini Music onboarding."
