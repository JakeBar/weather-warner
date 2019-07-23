#!/bin/bash

lint() {
    changed_files=$(git diff HEAD --name-only --diff-filter=d)
    committed_files=$(git diff origin/master... --name-only --)
    pipenv run pre-commit run -v --files $changed_files $committed_files
}

show_help_information() {
cat << EOF

Available subcommands:

    logs:   Follow the logs for the app container
    test:   Run one or more tests
    lint:   Run isort, flake8 and black on changed files
    shell:   Open a shell_plus session

    Other arguments are passed to manage.py by default.

EOF
}

cmd="${1:-}"
shift || true

if [[ -z "$cmd" ]]; then
    show_help_information >&2; exit 1
fi

case "$cmd" in
    logs) docker-compose logs --tail=100 -f django
        ;;
    test) docker-compose run --rm django pytest "$@"
        ;;
    lint) lint
        ;;
    shell) docker-compose run --rm django python -Wall manage.py shell_plus
        ;;
    *) docker-compose run --rm django python -Wall manage.py "$cmd" "$@"
        ;;
esac
