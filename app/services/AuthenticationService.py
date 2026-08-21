class AuthenticationService():
    def login(form):
        print(f"O usuario {form.username.data} fez o login, lembrar={form.remember_me.data}")
        return True