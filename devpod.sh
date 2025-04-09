#!/bin/bash

# Default values
DEFAULT_PROJECT_VERSION="1.0.0"
DEFAULT_AWS_PROFILE="default"
DEFAULT_PROJECT_PATH="."

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --project-version)
            PROJECT_VERSION="$2"
            shift 2
            ;;
        --aws-profile)
            AWS_PROFILE="$2"
            shift 2
            ;;
        --project-path)
            PROJECT_PATH="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Set defaults if not provided
PROJECT_VERSION=${PROJECT_VERSION:-$DEFAULT_PROJECT_VERSION}
AWS_PROFILE=${AWS_PROFILE:-$DEFAULT_AWS_PROFILE}
PROJECT_PATH=${PROJECT_PATH:-$DEFAULT_PROJECT_PATH}

# Get absolute path and clean it up
ABSOLUTE_PATH=$(cd "$PROJECT_PATH" && pwd)

# Extract the project name from the path (last directory name)
PROJECT_NAME=$(basename "$ABSOLUTE_PATH" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g')

# Use project name for container image
CONTAINER_IMAGE="$PROJECT_NAME"

# Set workspace directory using project name
WORKSPACE_DIR="/workspaces/${PROJECT_NAME}"

# Ensure project path exists
if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project path '$PROJECT_PATH' does not exist"
    exit 1
fi

# Create .devcontainer directory in the specified project path
mkdir -p "${PROJECT_PATH}/.devcontainer"

# Generate Dockerfile from template
sed \
    -e "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
    -e "s/{{PROJECT_VERSION}}/${PROJECT_VERSION}/g" \
    .devcontainer/Dockerfile.template > "${PROJECT_PATH}/.devcontainer/Dockerfile"

# Generate devcontainer.json from template
sed \
    -e "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
    -e "s/{{PROJECT_CONTAINER_IMAGE}}/${CONTAINER_IMAGE}/g" \
    -e "s/{{AWS_PROFILE}}/${AWS_PROFILE}/g" \
    -e "s|{{WORKSPACE_DIR}}|${WORKSPACE_DIR}|g" \
    .devcontainer/devcontainer.json.template > "${PROJECT_PATH}/.devcontainer/devcontainer.json"

# Generate build.sh from template
sed \
    -e "s/{{PROJECT_CONTAINER_IMAGE}}/${CONTAINER_IMAGE}/g" \
    .devcontainer/build.sh.template > "${PROJECT_PATH}/.devcontainer/build.sh"
chmod +x "${PROJECT_PATH}/.devcontainer/build.sh"

echo "DevPod environment setup complete for project: ${PROJECT_NAME}"
echo "Project path: ${PROJECT_PATH}"
echo "Container image name: ${CONTAINER_IMAGE}"
echo "You can now run: ${PROJECT_PATH}/.devcontainer/build.sh to build and start the container"
