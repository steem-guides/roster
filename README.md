### Introduction

`roster` is a list of the users in CN community and their nicknames.

![The Avengers](https://upload.wikimedia.org/wikipedia/en/f/f9/TheAvengers2012Poster.jpg)
<br/>
Image Source: [Wikipedia - The Avengers](https://en.wikipedia.org/wiki/The_Avengers_(2012_film))


### Features

1. Generate the roster from the community posts
1. Help team members to know / memorize each other's nickname easily


### How to Build the Roster

We collect the (name, nickname) pair from the posts in the community.

The current data sources includes below ones:
1. @teamcn-shop 's daily reports: https://steemit.com/@teamcn-shop
1. @teamcn-shop 's comments on users' posts
1. @teamcn 's ceremony post: https://steemit.com/steempress/@team-cn/egxwc0ewsi



### Commands

The commands / tasks in this project is manged with `invoke` package.

By running `pipenv run invoke -l`, you're able to see the available tasks in the bot.

```
Available tasks:

  roster.generate    generate the roster from the specified sources
  steem.list-posts   list the post by account, tag, keyword, etc.
```

To see the introduction of a command, run `pipenv run invoke -h <command>`.


### Reference

- The interaction with Steem blockchain is built with [beem](https://github.com/holgern/beem) project.


### License

The project is open sourced under MIT license.
