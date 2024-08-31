# Contributing

👍🎉 First off, thank you for taking the time to contribute! 🎉👍

This document describes our guidelines for contributing. They are guidelines, not rules. Use your best judgment and feel free to propose changes to this document in a pull request.

> This document can also be found in the AI Alliance [`community`](https://github.com/The-AI-Alliance/community/) repository.

## What Should I Know Before I Get Started?

We welcome contributions to Alliance projects, but contributors must accept certain agreements and conditions.

### The AI Alliance Code of Conduct

This project adheres to our [Code of Conduct](https://github.com/The-AI-Alliance/community/blob/main/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. If you observe unacceptable behavior, follow the instructions in the document to report it.

### Developer Certificate of Origin

The AI Alliance utilizes the Linux Foundation’s [Developer Certificate of Origin](https://developercertificate.org/) (DCO) on a per-commit basis to enable contributions to Core Projects. The DCO does not require the committer to give away ownership of the contribution - your IP remains yours and others' IP remains theirs.

Using DCO is discussed in more detail [below](#legal).

### AI Alliance Competition Law Guidelines

The AI Alliance and its members are committed to compliance with applicable antitrust and competition laws. See the [AI Alliance Competition Law Guidelines](https://ai-alliance.cdn.prismic.io/ai-alliance/ZnNNb5m069VX15Z1_AIAllianceCompetitionLawGuidelines.pdf) for details.

## The AI Alliance GitHub Organization and Repositories

The [`community`](https://github.com/The-AI-Alliance/community/) repository contains common files, like this one, that apply to all Alliance _core_ projects under the [`The-AI-Alliance`](https://github.com/The-AI-Alliance/) GitHub organization. Note that some Alliance members also collaborate on other _affiliate_ projects that are managed elsewhere and which were introduced to the Alliance by members seeking additional collaborators. The best way to find out about all the projects is to browse the [Alliance website](https://thealliance.ai/our-work).

In addition, some work is tracked at a high level in GitHub "projects" [here](https://github.com/orgs/The-AI-Alliance/projects) for projects that cut across different repos and GitHub organizations.

## The Contribution Process

We follow normal _GitOps_ practices. We ask that all work in a particular repo be contributed as a pull request where it will be, built automatically and tested (for code changes), reviewed by maintainers, and merged when accepted.

### Creating a Contribution

As an example, let's use the [`trust-safety-user-guide`](https://github.com/The-AI-Alliance/trust-safety-user-guide) repo.

Before you start working on a contribution to this guide review the [open issues](https://github.com/The-AI-Alliance/trust-safety-user-guide/issues) and [open pull requests](https://github.com/The-AI-Alliance/trust-safety-user-guide/pulls) to see if your contribution or enhancements are already proposed. You might instead be able to join forces with the people already working on these items. If you are unsure about how to contribute an idea, [open an issue](https://github.com/The-AI-Alliance/trust-safety-user-guide/issues) first to discuss your proposal idea with the maintainers.

> **Note:** Review the [Legal](#legal) section below before making any commits to a repo or fork of one.

To contribute to this repo, you'll use the *Fork and Pull* model common in many open source repositories. You can follow this process in a local terminal or in the GitHub web UI.

- For details on the local process, check out the [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) documentation from GitHub.
- For details on contributing using the GitHub webpage UI, see [Contributing using the GH UI](docs/contributing_via_GH_UI.md).

When your contribution is ready, you can create a pull request (PR). In general, we follow the standard [GitHub pull request](https://help.github.com/en/articles/about-pull-requests) process. Follow the template to provide details about your pull request to the maintainers. Before submitting pull requests, run any tests or formatting constraints locally that are defined for the repository, if any. For example, does the repo have a `make test` command for running the unit tests?

### Submitting Your Contribution

When submitting your PR, give it a title and description which are as clear and detailed as possible.

### Pull Request Review

After submitting a pull request, maintainers will review it and may make suggestions to fix before merging. It will be easier for your pull request to receive reviews if you consider the criteria the reviewers follow while working. Remember to:

- Run tests (if any) locally and ensure that they pass.
- Ensure your contribution is in the proper format, if defined, e.g., documentation conventions.
- Break large changes into a logical series of smaller patches, which are easy to understand individually and combine to solve a broader issue.
- Follow the project's coding and documentation conventions.

For a list of the maintainers, see the [MAINTAINERS.md](https://github.com/The-AI-Alliance/community/blob/main/MAINTAINERS.md) page.

## Submitting Bug Reports

To submit a new bug report, raise an issue in the appropriate repository before creating a pull request. This ensures that the issue is properly tracked. To fix an existing bug, assign yourself a bug from the issues page of the desired repository. Then, submit a pull request for review.

Bugs are tracked as GitHub issues in the corresponding repo.

## Legal

We have tried to make it as easy as possible to make contributions.
This applies to how we handle the legal aspects of contribution.

### "Developer Certificate of Origin"

We follow the [Developer's Certificate of Origin 1.1 (DCO)][DCO] to manage code contributions, which is the same approach that [the Linux Kernel community uses][Linux-DCO]. 

We ask that all developers include a sign-off statement in the commit message. Here is an example `Signed-off-by` line, which indicates that the submitter accepts the DCO:

```text
Signed-off-by: John Doe <john.doe@example.com>
```

This can be included automatically in a commit to a local Git repository using the following command:

```shell
git commit -s
```

> **Tip:** If a commit is created that did not include the `-s` option, the original commit message can be edited by using the `git commit -s --amend` command. A "force push" must be done afterward to add the amended commit to a PR.

Consider creating a git _alias_ that permanently adds the `-s` flag to all commits. For example, let's define a `cs` alias for this purpose:

```shell
git config --global alias.cs "commit -s"
...
git cs -m 'Some comment' changed_files
```

The alias will be added to your `~/.gitconfig` file.

If you don't want to make this a global alias, omit `--global` and run the command in each repo's root directory where you want to use it. The alias will be added to the `.git/config` file for your local repo clone.

### Licenses

Unless specifically stated, all Alliance projects are
distributed under a suitable "open" license. Use the following guidelines:

| Purpose | License | Website | SPDX License Identifier |
| :------ | :------ | :------ | :---------------------- |
| Code and Model Weights| [Apache License, Version 2.0](LICENSE.Apache-2.0) | [link](http://www.apache.org/licenses/LICENSE-2.0) | [link](https://spdx.org/licenses/Apache-2.0) |
| Documentation and other written materials | [The Creative Commons License, Version 4.0 - `CC BY 4.0`](LICENSE.CC-BY-4.0) | [link](https://chooser-beta.creativecommons.org/) | [link](https://spdx.org/licenses/CC-BY-4.0.html) |
| Data | [CDLA Permissive 2.0](LICENSE.CDLA-2.0) | [link](https://cdla.dev/permissive-2-0/) | [link](https://spdx.org/licenses/CDLA-Permissive-2.0.html) |

The AI Alliance leaves open the possibility of additional terms concerning safe and responsible use for certain elements in special core projects. For example, some model weights may be open for use, except for harmful purposes. Any decision to use any such additional terms for a core project must be made by the AI Alliance Steering Committee and will be clearly identified in the core project's repository.

[DCO]: https://developercertificate.org/
[Linux-DCO]: https://docs.kernel.org/process/submitting-patches.html#sign-your-work-the-developer-s-certificate-of-origin
