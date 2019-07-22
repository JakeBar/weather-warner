#!/bin/bash

lint() {
    changed_files=$(git diff HEAD --name-only --diff-filter=d)
    committed_files=$(git diff origin/master... --name-only --)
    pipenv run pre-commit run -v --files $changed_files $committed_files
}

show_help_information() {
cat << EOF

Available subcommands:

    lint:   Run isort, flake8 and black on changed files

EOF
}

cmd="${1:-}"
shift || true

if [[ -z "$cmd" ]]; then
    show_help_information >&2; exit 1
fi

case "$cmd" in
    lint) lint
        ;;
esac
