#!/usr/bin/env bash
#!/usr/bin/env bash
# build.sh without collectstatic

set -o errexit

echo "=== Starting Django Build Process ==="

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Only migrations (skip static files)
echo "Applying database migrations..."
python manage.py migrate

echo "=== Build completed successfully! ==="