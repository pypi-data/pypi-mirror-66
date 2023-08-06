# Micro template

This template is for writing micro services which are based on [bgtasks][bgtasks]

#### Do this steps to prepare your template for work:
  - Enter **APP_NAME(SERVICE_NAME)** in settings file
  - Change **micro_template** keyword in deployment files
  - While adding django models, after `manage.py makemigration` register your model permissions adding python command into migration file.(You can use `register_perms(permissions:list)` function in `apps/shared/service/perm.py` file )

[bgtasks]: <https://pypi.org/project/bgtasks/>