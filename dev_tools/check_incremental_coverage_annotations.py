import os
import sys

from dev_tools import prepared_env, shell_tools

from dev_tools.incremental_coverage import check_for_uncovered_lines


def main():
    if len(sys.argv) < 2:
        print(
            shell_tools.highlight(
                'Must specify a comparison branch (e.g. "origin/master" or "HEAD~1").',
                shell_tools.RED,
            )
        )
        sys.exit(1)
    comparison_branch = sys.argv[1]

    env = prepared_env.PreparedEnv(
        github_repo=None,
        actual_commit_id=None,  # local uncommitted files
        compare_commit_id=comparison_branch,
        destination_directory=os.getcwd(),
        virtual_env_path=None,
    )

    uncovered_count = check_for_uncovered_lines(env)
    if uncovered_count:
        sys.exit(1)


if __name__ == "__main__":
    main()