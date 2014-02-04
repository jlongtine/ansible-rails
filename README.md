# ansible-rails

Ansible library to work with bundler and rails related commands.

## example: rake command

**available options**

    - executable:
      description:
        - Bundler executable
      required: no
      default: $GEM_HOME/bin/bundle
    - path:
      description:
        - path which should cd'd into to run commands
      required: yes
    - current:
      description:
        - path of current version. used to decide if migrations and precompilations are necessary
      required: no
    - rails_env:
      description:
        - RAILS_ENV used by commands
      required: no
    - bundled:
      description:
        - use `bundle exec rake` or `bundle exec rails` instead of `rake` and `rails`
      required: no
      default: no
    - migrate:
      description:
        - migrate the database
      required: no
    - assets:
      description:
        - precompile the assets
      required: no
    - force:
      description:
        - force migration or asset compilation
      required: no
      default: false
    - command:
      description:
        - run any rake command, really
      required: no
      default: false

**examples**


    # run rake db:migrate
    rake: path=/path rails_env=staging current=/current migrate=yes

    # run bundle exec rake db:migrate
    rake: path=/path rails_env=staging current=/current migrate=yes bundled=yes

    # run bundle exec rake assets:precompile
    rake: path=/path rails_env=staging current=/current assets=yes bundled=yes

    # run bundle exec rake my:custom:command
    rake: path=/path rails_env=staging current=/current bundled=yes command="my:custom:command"

### Tests

To execute tests for the `rake` command run the following in the project directory:

    PYTHONPATH=$PWD/library python test/rake_test.py

## example: bundle command

**available options**

    - executable:
      description:
        - Bundler executable
      required: no
      default: $GEM_HOME/bin/bundle
    - deployment:
      description:
        - Run for deployment
      required: false
      default: yes
    - binstubs:
      description:
        - generate binstubs
      required: false
      default: no
    - gemfile:
      description:
        - Path of Gemfile to run against
      required: false
      default: yes
    - path:
      description:
        - Path to install dependencies into
      required: false

**examples**

    # install a specific Gemfile to `shared/vendor`
    bundle: path=shared/vendor gemfile=/path/to/gemfile

    # install with option --deployment
    bundle: path=shared/vendor deployment=yes

    # use a specific bundler binary
    bundle: path=shared/vendor executable=$HOME/.rvm/wrappers/bundle


### Tests

To execute tests for the `bundle` command run the following in the project directory:

    PYTHONPATH=$PWD/library python test/bundle_test.py