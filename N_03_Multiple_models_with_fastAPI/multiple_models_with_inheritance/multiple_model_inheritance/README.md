# Multiple Models with Inheritance:

In the previous code, we had lot of duplicated data and if we decide to rename one field (column) it won't be easy. So to avoid duplication we use another approach called Multiple Models with Inheritance.

In the previous step, Hero, HeroCreate and HeroRead share some base fields:

- name, required
- secret_name, required
- age, optional

So we will create a base model HeroBase that the other can inherit from and it is not a sqlAlchemy model (no table attribute here)

# Rules to inherit Models:

- Only inherit from data models, don't inherit from table models
- It will help you avoid confusion, and there won't be any reason for you to need to inherit from a table model.
- If you feel like you need to inherit from a table model, then instead create a base class that is only a data model and has all those fields, like HeroBase. And then inherit from that base class that is only a data model for any other data model and for the table model.

## Note:

Inheritance, the same as SQLModel, and anything else, are just tools to help you be more productive, that's one of their main objectives. If something is not helping with that (e.g. too much duplication, too much complexity), then change it.
