# ansible-rails

Ansible extensions to work with bundler and rails related commands
as well as a role which deploys just like capistrano/ mina does.

## example: deploy role

    ---
    - hosts: server
      user: app
      gather_facts: False
      vars:
        user: app
        home_directory: "/home/{{ user }}"
        rails_env: "staging"

      roles:
        -
          role: nicolai86.ansible-rails

          repo: git@example.com:app
          branch: develop

          deploy_to: "{{ home_directory }}"
          build_path: "{{ deploy_to }}/releases/{{ timestamp.stdout }}"
          shared_path: "{{ deploy_to }}/shared"
          current_path: "{{ deploy_to }}/current"
          migrate: yes
          compile_assets: yes

          symlinks:
            - { src: "{{ shared_path }}/vendor/bundle", dest: "{{ build_path }}/vendor/bundle" }
            - { src: "{{ shared_path }}/public/assets", dest: "{{ build_path }}/public/assets" }
            - { src: "{{ shared_path }}/log", dest: "{{ build_path }}/log" }
            - { src: "{{ shared_path }}/.env", dest: "{{ build_path }}/.env" }
            - { src: "{{ shared_path }}/config/database.yml", dest: "{{ build_path }}/config/database.yml" }

          directories:
            - "{{ shared_path }}/config"

          templates:
            - { src: "templates/env.js", dest: "{{ shared_path }}/.env" }


#### requirements

  - all gem binaries (e.g. bundle, rake, rails) need to be locateable using the $PATH. Make sure to setup properly

#### important features:

  - it can be reused multiple times inside a single playbook for separate deployments.
  - works with rvm, rbenv or system ruby installations.
  - it's using a bare copy of the repository to deploy.
  - migration and asset compilation can be de-activated as needed.
  - only keeps 5 most recent deployments per default

#### limitations

  - does not support rollbacks because ansible does not support error handling (yet)
  - does not contain any restart logic (will change in the future)

## example: rails command

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

**examples**


    # run rake db:migrate
    rails: path=/path rails_env=staging current=/current migrate=yes

    # run bundle exec rake db:migrate
    rails: path=/path rails_env=staging current=/current migrate=yes bundled=yes

    # run bundle exec rake assets:precompile
    rails: path=/path rails_env=staging current=/current assets=yes bundled=yes


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
