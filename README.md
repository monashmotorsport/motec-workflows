# Monash Motorpsort Workflows

This repository contains a set of Github Actions and pre-commit hooks used by the team across our private repos, mostly for use with MoTeC codebases.

## Github Actions

Github Actions can be used inside your repository's workflows to automate tasks, or automate checks on pull requests. Examples of how to use each action are provided below. For more information on how to set up and use Github Actions, please refer to the [Github Actions documentation](https://docs.github.com/en/actions).

#### `validate-m1prj`

Validates MoTeC `.m1prj` project files against the XSD schema. Additionally, it checks for any self-closing `<Help>` and `<Comment>` tags if the M1 build version is 1.4 or lower, as these will corrupt the project. By default, the action will search for any `Project.m1prj` files in the repository and validate them, but a specific path can also be provided.

```yaml
- name: Validate .m1prj
  uses: monashmotorsport/workflows/validate-m1prj@main
  with:
    path: "**/Project.m1prj" # Default value
```

#### `validate-m1cfg`

Validates MoTeC `.m1cfg` files against the XSD schema, and optionally compares the configuration against a corresponding .m1prj file. Configuration files contain the values of parameters, tables, IO resources, and calibrations used by the project. If a project path is provided, the action will check that all settings in the `.m1cfg` file are actually used in the project, and that all settings used in the project are defined in the config file. If no project path is provided, only schema validation will be performed.

```yaml
- name: Validate .m1cfg
  uses: monashmotorsport/workflows/validate-m1cfg@main
  with:
    cfg-path: path/to/Project.m1cfg
    prj-path: path/to/Parameters.m1prj # Optional
```

## Pre-commit Hooks

Hooks are installed and configured using the [pre-commit framework](https://pre-commit.com/). Examples of how to add each hook to your pre-commit config are provided below. For more information on how to set up and use pre-commit, please refer to the [pre-commit documentation](https://pre-commit.com/#install).

#### `convert-tabs-to-spaces`

Converts all tabs in specified files to spaces. By default, it will convert all tabs in all files. Can be configured to a specific set of files using the `files` option in the pre-commit config. Example usage:

```yaml
repos:
  - repo: https://github.com/monashmotorsport/workflows
    rev: v0.0.2
    hooks:
      - id: convert-tabs-to-spaces
        files: \.m1scr$
        args: [--spaces, 4] # Optional, defaults to 4 spaces
```

#### `verify-commit-author`

Checks that the author of a commit has an email address that matches the configured domain. By default, it will check for the `@monashmotorsport.com` domain, but this can be configured using the `domain` flag. Can also check whether the author's name matches the name in the email address. Example usage:

```yaml
repos:
  - repo: https://github.com/monashmotorsport/workflows
    rev: v0.0.2
    hooks:
      - id: verify-commit-author
        args: [--domain=monashmotorsport.com, --check-name]
```

#### `verify-branch-name`

Verifies that the branch name of a commit matches the `<category>/<description>` format, where the category is one of a predefined set of categories. A default set of categories is provided, as well as special branch names that are always allowed (e.g. `main`, `master`) but these can be configured using the `categories` and `allowed-branches` flags. Example usage:

```yaml
repos:
  - repo: https://github.com/monashmotorsport/workflows
    rev: v0.0.2
    hooks:
      - id: verify-branch-name
        args: [
            --categories=feature, bugfix, hotfix, config,
            --allowed-branches=main, dev
            ]
```
