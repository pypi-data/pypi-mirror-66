# dotconfig

A single configuration file for `.bash_profile` and `.gitconfig`.

    $ pipx install nr.dotconfig
    $ dotconfig dotconfig.yaml -u
    Writing /home/me/.bash_profile
    Writing /home/me/.gitconfig

## Example

My own dotconfig can be found [here](https://git.niklasrosenstein.com/NiklasRosenstein/dotconfig-files/raw/branch/master/dotconfig.yaml).
An further example below shows how another config file can be taken as a basis for another (eg. to add work related settings on top
of a personal configuration).

```yml
base: https://git.niklasrosenstein.com/NiklasRosenstein/dotconfig-files/raw/branch/master/dotconfig.yaml
profile:
  blocks:
    work-functions: |
      function do-all-my-work() {
        # it's a secret
      }
gitconfig:
  user:
    email: my-work-mail@work.com
    signingkey: WORKSIGNINKEYID
  Profile.user: '{{base.gitconfig.user}}'
```

---

<p align="center">Copyright 2020 &copy; Niklas Rosenstein</p>
