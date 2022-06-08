from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    
    """ Utilisant un model d'utilisateur personnalisé, cette class sert à redefinir la façon doit un utilisateurs va etre créé en tenant compte de ma configuration.
    """

    def create_user(self, first_name, last_name, username, email, password=None):
        
        """ Redefinition de la fonction servant à créer un utilisateur.

        Raises:
            ValueError: Genere une erreur en cas d'adresse email manquante.
            ValueError: Genere une erreur en cas dde nom d'utilisateur manquant.

        Returns:
            _type_: L'utilisateur venant d'etre créé
        """
        if not email:
            raise ValueError('Adresse email incorrect')

        if not username:
            raise ValueError('Username incorrect')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )
        
        user.set_password(password)

        user.save(using=self._db)
        return user


    def create_superuser(self, first_name, last_name, username, email, password):
        
        """ Redefinition de la fonction servant à créer un super-utilisateur.
        """

        user = self.create_user(
            first_name= first_name,
            last_name = last_name, 
            username = username,
            email = email,
            password = password
            )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)


class Account(AbstractBaseUser):
    
    """ Model de base donnée represantant un utilisateur du site.
        Ce model se base sur le model User de base (AbstractBaseUser) proposé par Django.
    """
    
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique = True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)

    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_superadmin   = models.BooleanField(default=False)
    
    # Redefinition du champs servant de username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True