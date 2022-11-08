# Contributing Guide

<div align="center">

[![This Project Uses Conventional Commits](https://img.shields.io/badge/Commit%20Style-Conventional-e10079)](https://www.conventionalcommits.org/)
[![Maintained](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://graphicartquest.com/author/scott-lassiter/)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](#how-can-i-contribute)

**Thank you for contributing to Blender Scripting Assistant!**

</div>

Before contributing, please take a moment to read through this document. This guide documents the project source code organization, tooling, standards, and processes that go into the CI/CD pipeline.

<details open="open">
    <summary><b>Table of Contents</b></summary>

-   [Code of Conduct](#code-of-conduct)
-   [How can I Contribute?](#how-can-i-contribute)
    -   [Submit Issues](#submit-issues)
    -   [Propose New Features](#propose-new-features)
    -   [Submit a Pull Request](#submit-a-pull-request)
-   [Development](#development)
    -   [Local Installation](#local-installation)
    -   [Running Tests](#running-tests)
    -   [Building](#building)
    -   [Project Structure](#project-structure)
    -   [Documentation](#documentation)
-   [Adding New Features](#adding-new-features)
    -   [Checklist](#checklist)
    -   [Creating New Tests](#creating-new-tests)
-   [Commits](#commits)
    -   [Commit Header Format](#commit-header-format)
    -   [Commit Body Format](#commit-body-format)
    -   [Commit Footer Format](#commit-footer-format)
-   [Versioning Triggers](#versioning-triggers)
    -   [Example Patch Version Change](#example-patch-version-change)
    -   [Example Minor Version Change](#example-minor-version-change)
    -   [Example Major Version Change](#example-major-version-change)
    -   [Examples That Cause No Change](#examples-that-cause-no-change)

</details>

## Code of Conduct

Please help keep this project open and inclusive. Refer to the [Code of Conduct](CODE_OF_CONDUCT.md) before your first contribution.

## How can I Contribute?

### Submit Issues

**Bug Reports**: Be as detailed as possible, and fill out all information requested in the [bug report template][choose issue].

*For security related issues, see the [security policy][security policy].*

**Documentation Requests**: Is something unclear in the documentation or the API? Submit a [documentation change request][choose issue]! Be as detailed as possible. If you have the question, chances are someone else will also who isn't as willing to speak up as you are. If you want to do it yourself, see the [documentation guidelines](#documentation) for instructions.

### Propose New Features

Feature requests are welcome! Before submitting:

-   Take a moment to make sure your feature idea fits within the scope and aims of this project. **Blender Scripting Assistant** aims to make it easier for developers to write Blender scripts and create add-ons. All contributions must meet [Blender's community add-on requirements][blender addon reqs].
-   Search the issues for [enhancements][enhancements requested] to make sure this isn't already in the works.
-   Be as detailed as possible, and fill out a [new matcher request][choose issue]. It is up to you to make your case of why the feature should get included.

**Please ask** before embarking on any significant undertaking (e.g. implementing a new matcher, major code refactoring), otherwise you risk wasting time on something that might not fit well with the project. Do this by opening an issue for the proposal.

### Submit a Pull Request

Good pull requests are outstanding help. They should remain focused in scope and avoid unrelated commits.

To submit a pull request,

1. Fork and clone the repository
1. Create a branch for your edits
1. Make sure your work follows the [commits](#commits) guidance

## Development

### Local Installation

```bash
git clone https://github.com/GraphicArtQuest/Blender-Scripting-Assistant.git
cd Blender-Scripting-Assistant
mkdir dist # The build script will fail if this folder does not exist
```

After installing, you should [run the test script](#running-tests) and [build a local distributable](#building) to verify everything works without runtime errors before you start making changes.

### Running Tests

This project provides high working confidence to developers by uses Jest itself for unit testing. Test locally using one of the following scripts:

```bash
python test.py
```

Additionally, there is a manual testing script to verify if the `debugpy` server is working and code editors such as VS Code can connect to it:

```bash
python testdebugpy.py
```

### Building

Before submitting changes, run the build script locally, then commit:

```bash
python build.py 
```

### Project Structure

```
├── dist
├── src
│   ├── console_messages
|   │   └── <individual output scripts>
│   ├── operators
|   │   └── <individual operators>
│   ├── bundler.py
|   ├── debug_server.py
|   ├── directory_monitor.py
|   ├── hot_swap.py
|   ├── preferences.py
|   └── ui.js
├── tests
│   ├── test_bundler.py
|   └── test_directory_monitor.py
```

-   `dist`: output directory for the bundled add-on. This will exist locally only as the `.gitignore` excludes the directory to prevent committing binaries. Official distributables are hosted in [releases][releases].
-   `src`: contains all distribution files.
    -   `console_messages`: Contains individual Python scripts for individual modules that consolidates and prints color enhanced formatted console messages.
    -   `operators`: Contains indivudal Python scripts that extend Blender's `bpy.types.Operator` class. Limit each script to a single operator.
    -   `bundler.py`: Bundles source files into into the format Blender requires to install add-ons.
    -   `debug_server.py`: Starts and runs the `debugpy` debug server for remote debugging .
    -   `directory_monitor.py`: Monitors a specified file or folder for any changes. Has a subscribable function to run registered scripts when it detects changes.
    -   `hot_swap.py`: Reloads a specified add-on back into Blender by disabling, reinstalling, and enabling it again. 
    -   `preferences.py`: Stores the user preferences and variables that persist between Blender sessions by extending the `bpy.types.AddonPreferences` class.
    -   `ui.py`: Creates all the user interfaces by extending Blender's `bpy.types.Panel` class.
-   `tests`: the individual `unittest` scripts used to verify the functionality works as designed

### Documentation

API Documentation is manually generated.

## Adding New Features

### Checklist

Before pushing to Github and opening a pull request:

-   [ ] Open an issue with detailed description of the purpose and required behavior
-   [ ] Document the functionality within the code
-   [ ] Update the `README.md`
-   [ ] Create a unit test under `tests/`
-   [ ] Verify `test.py` passes locally
-   [ ] Run the `build.py` script locally and verify it installs and works on Blender

Explain any omissions or exceptions to this checklist in your pull request.

### Creating New Tests

**Blender Scripting Assistant** uses the built-in Python [unittest][unittest] library for testing. Tests [reside separately][tests] from the source code and do not get distributed with each release.

Unfortunately, `unittest` does not easily display the percent test coverage. Still, aim for 100% test coverage when creating new functions. Use the issue you opened to fully describe and document how this function should work. This provides a persistent reference point for the logic that drives the tests.

Refer to any of the [test files][tests] for examples.

## Commits

All commits must follow this guidance. *This specification is inspired by and supersedes the [Angular Commit Message](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit).*

If possible, make [atomic commits](https://en.wikipedia.org/wiki/Atomic_commit), which means:

-   a commit should contain exactly one self-contained functional change
-   a functional change should be contained in exactly one commit
-   a commit should not create an inconsistent state (such as test errors, linting errors, partial fix, feature with documentation etc...)

A complex feature can be broken down into multiple commits as long as each one maintains a consistent state and consists of a self-contained change.

This project uses very precise rules over how Git commit messages must be formatted. This leads to **easier to read commit history**.

Each commit message consists of a **header**, a **body**, and a **footer**.

```bash
<header>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

The `header` is mandatory and must conform to the [Commit Message Header](#commit-header-format) format.

The `body` is mandatory for all commits except for those of type "docs".
When the body is present it must be at least 20 characters long and must conform to the [Commit Message Body](#commit-body-format) format.

The `footer` is optional unless resolving issues. The [Commit Message Footer](#commit-footer-format) format describes what the footer is used for and the structure it must have.

### Commit Header Format

The header contains succinct description of the change:

-   use the imperative, present tense: "change" not "changed" nor "changes"
-   don't capitalize first letter
-   no dot (.) at the end
-   if the commit is of type `revert`, include `reverts commit <hash>`, where the hash is the SHA of the commit being reverted

```
<type>(<scope>): <short summary>
│      │         │
│      │         └─⫸ Summary in present tense. Not capitalized. No period at the end.
│      │
│      └─⫸ Commit Scope: <custom>|api|contributing|license|readme|security
│
└─⫸ Commit Type: build|ci|docs|feat|fix|perf|refactor|revert|test
```

**Types**

Required. Must be one of the following:

-   `build`: Changes that affect the build system configuration, package scripts, or dev dependencies (i.e. adds/remove/modify/update)
-   `ci`: Changes to CI configuration files and scripts (e.g. release configs, YAML scripts, GitHub templates)
-   `docs`: Documentation only changes including both markdown documentation and API comments within code
-   `feat`: Adding new or enhancing existing functionality
-   `fix`: Fixes a bug in an existing feature
-   `perf`: A code change that improves performance
-   `refactor`: A code change that neither fixes a bug nor adds a feature
-   `revert`: Revert to a commit
-   `test`: Add missing tests or correct existing tests

**Scopes**

Optional. If used, must be one of the following supported scopes:

-   `console_messages`: Changes to any of the console message scripts
-   `contributing`: Contributions to this guidance or the [Code of Conduct](CODE_OF_CONDUCT.md)
-   `license`: Changes to terms or copyright status within the [license](LICENSE).
    -   _Any change in license type MUST include a BREAKING CHANGE_
-   `operators`: Changes to any operator function
-   `readme`: Contributions to the main [README.md](README.md)
-   `security`: Changes that address code related security issues or security policies
-   Changes to one of the add-on modules. Use one of the following:
    - `bundler`
    - `debug_server`
    - `directory_monitor`
    - `hot_swap`
    - `preferences`
    - `ui`

### Commit Body Format

Provide a plain text description of *why* you made this change. This is the place for you to explain your thought process, developer to developer. If helpful, include a comparison of the previous behavior with the new behavior to illustrate the change's impact.

If there are breaking changes, start the body with `BREAKING CHANGE: <breaking change summary>.`

### Commit Footer Format

The footer identifies which issues this commit fixes. If none, leave it blank. Otherwise, use the format `Resolves #<issue number>`. If more than one issue is resolved, separate them with a comma.

## Versioning Triggers

This project uses [Semantic Versioning](https://semver.org/) and releases updates based on specific types used in the commit messages.

-   Patch
    -   `fix`
    -   `perf`
-   Version
    -   `feat`
-   Major
    -   `BREAKING CHANGE`

### Example Patch Version Change

```
fix(directory_monitor): address bug that caused...

This corrects a bug that caused... by doing...

Resolves: #1
```

### Example Minor Version Change

```
feat(ui): add button to do...

This function adds a button to the UI that executes the... This works by...

Resolves: #2, #3
```

### Example Major Version Change

```
feat(index): add function `foobar`

BREAKING CHANGE: This function does some new useful things. Due to refactoring in the `foo` function, it no longer...

Resolves: #4
```

### Examples That Cause No Change

```
docs(readme): update readme to document new changes to `foo`

Resolves: #5
```

```
refactor(preferences): change `foo` implementation to faster xyz algorithm
```


[security policy]: https://github.com/GraphicArtQuest/Blender-Scripting-Assistant/blob/master/.github/SECURITY.md
[choose issue]: https://github.com/GraphicArtQuest/Blender-Scripting-Assistant/issues/new/choose
[enhancements requested]: https://github.com/M-Scott-Lassiter/jest-geojson/labels/enhancement
[blender addon reqs]: https://wiki.blender.org/wiki/Process/Addons
[tests]: https://github.com/GraphicArtQuest/Blender-Scripting-Assistant/tree/master/tests
[unittest]: https://docs.python.org/3/library/unittest.html
[releases]: https://github.com/GraphicArtQuest/Blender-Scripting-Assistant/releases