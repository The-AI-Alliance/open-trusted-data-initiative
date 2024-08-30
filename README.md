# Open Trusted Data Initiative README

Welcome to the AI Alliance [Open Trusted Data Initiative](https://the-ai-alliance.github.io/open-trusted-data-initiative/)

The documentation for this repo is published using [GitHub Pages](https://pages.github.com/). We welcome contributions as PRs. See the AI Alliance [CONTRIBUTING](https://github.com/The-AI-Alliance/community/blob/main/CONTRIBUTING.md) instructions. Also, you'll need to agree with the AI Alliance [Code of Conduct](https://github.com/The-AI-Alliance/community/blob/main/CODE_OF_CONDUCT.md) and all contributions will be covered by the [LICENSE](https://github.com/The-AI-Alliance/community/blob/main/LICENSE) (which is also in [this repo](LICENSE)).

> [!NOTE]
> The documentation in this repo is licensed under Creative Commons Attribution 4.0 International. To view a copy of this license, see [LICENSE.CC-BY-4.0](LICENSE.CC-BY-4.0) or visit https://creativecommons.org/licenses/by/4.0/legalcode. All code uses the [Apache 2.0](LICENSE.Apache-2.0) license.

## Quick Setup

We use [GitHub Pages](https://pages.github.com/) so edits can be made in Markdown, updates can be managed using pull requests, and the results can be published automatically by GitHub.

In fact, each page has _Edit this page on GitHub_ links, making it easy to view a page, then go straight to the source to edit it and submit a PR! This is the best way to help us fix typos and make similar small edits.

However, this easy approach only supports correcting content on a single page. for more significant changes, like adding new pages, you'll want to edit and preview the changes locally.

Local previewing also helps you see how the changes will _really_ look when rendered. While GitHub renders Markdown well, there are extensions we use that are supported by Jekyll that won't be rendered correctly in GitHub's default file viewer. 

So, to view the website locally and to make more extensive changes, you'll need to have a recent version of [Ruby](https://www.ruby-lang.org/en/) installed, along with the [`gem`](https://docs.ruby-lang.org/en/master/Gem.html) and [`jekyll`](https://jekyllrb.com/) tools.

We discuss these steps in more depth [below](#setup-jekyll), but the following steps may _just work_ for you.

Install a recent version of Ruby 3. Note that on MacOS, the default Ruby installation is old, version 2.6.10. Installing Ruby will also install the `gem` dependency tool.

This project's `Makefile` will attempt to install the remaining dependencies, including `jekyll`, when you run `make all` or `make view-local`, as a prerequisite task.

So, try `make view-local` and see if Jekyll is installed successfully and website is rendered.

The command will finish with a message like this:

```
...
Server address: http://127.0.0.1:4000/
Server running... press ctrl-c to stop.
```

Open the URL in a browser. 

> **Tips:** 
> 1. On MacOS, use &#8984;-click on the URL to open it in a browser.
> 2. Run `make help` for a list of commands defined.

> **WARNING:** The automatic setup of `jekyll` in the `Makefile` has only been tested on MacOS. If you encounter problems on other platforms, please [post an issue](https://github.com/The-AI-Alliance/open-trusted-data-initiative/issues) to get help, or if you can fix the issue, a [pull request](https://github.com/The-AI-Alliance/open-trusted-data-initiative/pulls) (PR) is always welcome :nerd_face:. (More details on PRs below.)



## Contributing New or Improved Content

What gets displayed by GitHub Pages is the customized Markdown files in the `docs` directory. If you need to create a new page, copy an existing page to get the correct "header" information, then edit as needed.

Here are some things you should know.

### Using the Correct Branch

As for most Git projects, issue PRs to the `main` branch. However, the repo is actually configured to publish the docs from the `latest` branch, so we can accept PRs quickly, then decide when to publish a new version. (We will also tag `latest` for each release with a version number, for historical tracking.)

> **Note:** If you are curious, the details of how this publication branch is configured are discussed [below](#configuring-github-pages-in-the-repo-settings).

## Publishing a New Version

Because PRs go to the `main` branch, but the pages are published from the `latest` branch, PRs are not immediately published. When it is time to publish a new version of the website, change to the `main` git branch and run the script `./publish.sh`. It takes several options:

```
> publish.sh -h
publish.sh [-h|--help] [-n|--noop] [-v|--version V] [-t|--timestamp T]

Where the options are the following:
-h | --help            Print this message and exit
-n | --noop            Just print the commands but don't make changes.
-v | --version V       Use version string "V", which should be of the format
                       "X.Y.Z". Without this option the current value of
                       "last_version" in _config.yml is extracted (e.g., 1.0.1)
                       and the last digit is incremented.
-t | --timestamp "T"   Use this timestamp "T", which you'll need to quote on
                       the command line, because it must be of the form
                       "%Y-%m-%d %H:%M %z". Without this option, the current
                       system time is used.
```

With no arguments, the current version string's last digit will be incremented. For example, if the current version is `1.2.3`, the new version with be `1.2.4`. _Please use this `X.Y.Z` format if you specify a new version explicitly._ The script doesn't check the format.

The script _does_ check that a specified timestamp uses the correct format, but it should be rare that you would want to use any timestamp other than the current time, which is the default.

Both strings are printed at the bottom of each page, e.g.:

> Version: 1.0.1. Site last modified: Jun 5 2024 08:13 -0500.

## Editing Conventions and Tips

### Links

For internal cross-references, use the conventional `[title]({{site.baseurl}}/relative_URL)` Markdown syntax. 

> **WARNING:** the `{{site.baseurl}}/` prefix is _essential_, because this _prefix_ will be different for local execution vs. published serving.

For external links, add a `target` tag using the following syntax, which works for GitHub Markdown and GitHub Pages.

```
[title]({{site.baseurl}}/relative_URL){:target="_target"}
```

The `target` value is arbitrary; use whatever you want. While this is a little more tedious to type, it is usually better for users so they don't lose their place in the document. Also, [our stylesheet](https://github.com/The-AI-Alliance/open-trusted-data-initiative/blob/main/docs/_includes/css/custom.scss.liquid) is configured to put the little up-and-to-the-right arrows after every link that isn't relative, i.e., links that start with `http` or `https`. This provides a visual clue that a new tab will be opened.

### Emojis

In the pages, you can use emojis, e.g., `:+1:` yields :+1:, `:smirk:` yields :smirk:, `:nerd_face:` yields :nerd_face:, etc. The `jemoji` Ruby gem adds this capability. [Here is a list of available emojis](https://www.webfx.com/tools/emoji-cheat-sheet/).

## Previewing Your Work Locally

We provided a basic set of instructions above for setting up Jekyll locally. Here is a more detailed set of instructions, if you need them.

### Setup Jekyll

First, you'll need a reasonably recent version of Ruby installed. The one that comes with MacOS is _not new enough_. See [Use Homebrew to Install Ruby on MacOS](#use-homebrew-to-install-ruby-on-macos) to install [Homebrew](https://brew.sh) and then Ruby using the `brew` command.

Afterwards, the commands shown next should produce similar output that shown from Dean's machine, circa June 2024:

```shell
$ which ruby
/usr/local/Cellar/ruby/3.3.0/bin/ruby
$ ruby --version
ruby 3.3.0 (2023-12-25 revision 5124f9ac75) [x86_64-darwin23]
```

> **Warning:** In 2022, when we used these tools, building the website was not working with Ruby 3.2, you may still need to use 3.3 or 3.1.

For MacOS, make sure the `ruby` path shown is not `/usr/bin/ruby`, which is the old, built-in 2.6 version. Try `which -a ruby`, which will hopefully show the `Cellar` version second. If so, edit the `PATH` definition in your `~/.zshrc` file to put the newer `/usr/local/Cellar/ruby/3.X.Y/bin` directory before `/usr/bin/`.

Now, it _should_ be sufficient to run the following command:

```shell
make setup-jekyll
```

If this fails, then see the [Tips and Known Issues](#tips-and-known-issues) below.

### View the Pages Locally

Once Jekyll is set up, you can serve the pages locally for previewing and editing by running the following command, then open [localhost:4000](http://localhost:4000) in a browser.

```shell
make view-local   # Or use "make all" or just "make"!
```

If this throws an error, see the [Tips and Known Issues](#tips-and-known-issues) below.

> **Tip:** In MacOS terminal windows, you can &#8984;+click any URL printed to open it in a browser!

The `make` target runs the following command:

```shell
cd docs && bundle exec jekyll serve --baseurl '' --incremental
```

The `--baseurl` flag effectively supports the simple URL, `localhost:4000`. (Without it, the URL would be `localhost:4000/The-AI-Alliance/open-trusted-data-initiative/`.) The `--incremental` flag lets you edit the pages and refresh the browser tab to see the updates immediately. 

> **Note:** Well, more or less immediately. It can take several seconds for new pages to be generated and sometimes you'll get weird behaviors if you change URL paths, etc. So, occasionally it is useful to _control-c_ in the terminal and rerun `make view-local`.

> **Pro Tip:** `make view-pages` opens the _published_ GitHub Pages in a browser tab.

### Now Edit!

You can now edit the pages, save them, then refresh your browser to see the updates.

## Tips and Known Issues

### Use Homebrew to Install Ruby on MacOS (Recommended)

You really can't use the Ruby that comes with your Mac, because:
1. It's too old, 2.6.X, instead of 3.X, which we need.
2. You don't have permissions to install Gems into `/Library/...`

So, install [Homebrew](https://brew.sh), if you haven't already. Then use it to install a local, recent version of Ruby:

```shell
brew install ruby@3.3
which -a ruby
```

If the last command shows `/usr/bin/ruby` before a path like `/usr/local/Cellar/ruby/3.3.0/bin/ruby`, then you will have to edit your `~/.zshrc` file and make sure the `/usr/local/Cellar/ruby/...` path comes before `/usr/bin`. For example, the following line will just put this Ruby first. (this is a hack):

```shell
PATH="/usr/local/opt/ruby/3.3.0/bin:$PATH"
```

(Use the exact version number you have!)

Then in your terminal, either open a new window/tab or run the command `source ~/.zshrc` to load the changed `PATH`. Now `which ruby` should return a path in `/usr/local/Cellar/...` and `ruby --version` should return the correct 3.X version.

### The Jekyll Installation Instructions Failed

Suppose you run the following command and it fails:

```shell
make setup-jekyll
```

First, make sure you are using a valid version of `ruby`, as described in the previous section. A symptom you didn't do that? You'll see this error message:

```
You don't have write permissions for the /Library/Ruby/Gems/2.6.0 directory.
```

The commands run by `make setup-jekyll` discussed previously include the following (a few details omitted for simplification):

```shell
gem install jekyll bundler jemoji
bundle install
bundle update html-pipeline
```

Finally, if you are still stuck, please [post an issue](https://github.com/The-AI-Alliance/open-trusted-data-initiative/issues) to get help.

> **Help Needed:** If you find missing steps that `make setup-jekyll` should run but doesn't, or you find and fix problems that only occur on non-MacOS platforms, **please** submit a PR with fixes! Thank you. 

### The "make view-local" Command Fails

What if `make view-local` command fails with this error message?

```
jekyll 3.9.2 | Error: No such file or directory @ rb_check_realpath_internal
```

First, that's an old Jekyll version. It should be 4.3.3 or later. Try these commands:

```
gem uninstall jekyll
gem install jekyll
gem list | grep jekyll
```

### Configuring GitHub Pages in the Repo Settings

This section documents the one-time settings changes we did to [configure publication of our GitHub Pages](https://docs.github.com/en/enterprise-server@3.1/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site). We changed the desired branch to use, `latest`, rather than the default `main` branch, and we specified the directory for the website pages, `docs`. This only needs to be done if and when the branch or directory location is changed.

In the repo's _Settings > GitHub Pages_ section, set the branch to be `latest` and the folder to be `/docs`. The reason for using `latest` rather than `main`, is to allow small changes to be made without affecting what is published until we decide to publish an update.
