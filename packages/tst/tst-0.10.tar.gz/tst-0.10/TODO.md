# To do

- refactor site.get() and site.get_directory()
- make login command print in colors; make login perform a
  version command immediately after login (perhaps in a thread,
  so that it is done, while the user logs into the web and
  creates the token)


# Bugs

1. Quando se tenta fazer login em um site sem url de login,
   e se fornece o código na linha de comando, o tst quebra.
