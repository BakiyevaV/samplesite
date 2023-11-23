import uuid

from django.db import models

is_all_posts_passive = False

def is_active():
    return is_all_posts_passive


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название',unique=True) #unique for day,/unique for month
    #db_index индексация поиска, бинарные деревья

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']


class Bb(models.Model):
    class Kinds(models.TextChoices):
        BUY = 'b','Куплю'
        SELL= 's', 'Продам'
        RENT = 'r'
        __empty__ = 'Выберите тип объявления'
    '''KINDS = (
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('с', 'Обменяю')
    )'''
    '''KINDS = (
        ('Купля-продажа',(
         ('s', 'Продам'),
        ('b', 'Куплю'),
        )),
        ('Обмен',(
        ('с', 'Обменяю'),
        ))'''

    # KINDS = (
    #     (None, 'Выберите тип объявления')
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('с', 'Обменяю')
    # )



    #kind = models.CharField(max_length=1, choices=KINDS,default='s')
    # kind = models.CharField(max_length=1, choices=KINDS,blank=True)
    kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.SELL)
    rubric = models.ForeignKey("Rubric", null=True, on_delete=models.PROTECT, #наименование поля, которое отображается, related_name = '' замена objects во view
                               #"Rubric" в ковычках, позволяет обращаться в любом порядке, раньше или позже кода строки без ковычек, значик модель должна быть реализована выше
                               verbose_name='Рубрика') # +helptext = '' помощь/описание без настройки не отображается

    title = models.CharField(max_length=50, verbose_name="Товар")
    content = models.TextField(null=True, blank=True, verbose_name="Описание")
    price = models.DecimalField(verbose_name="Цена",default=0, max_digits=8, decimal_places=2)# +default= 0.0 дефолтное значение #
    is_active = models.BooleanField(default=is_all_posts_passive)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")#auto_now_add - заполнение поля текущим временем в момент создания не изменяется
    updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Опубликовано")#auto_now - заполнение поля текущим временем в момент создания обновляемое
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #editable=False вывод в форму)
    """типы полей:
    -charfield - текстовое поле (обязательно max_length)
    -textfield - текстовое поле (не обязательно max_length)
    -emailField (не обязательно max_length)
    -urlField 
    -SlugField (max_length = 50, allow_unicode = True)
    -NullBooleanField
    -IntegerField
    -PositiveIntegerField (Small, Big)
    -BinaryField()
    -AutoField - для id
    -UUIDField"
    -"""



    def __str__(self):
        return f'{self.title}'


    class Meta:
        # доп настройки модели
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published'] #можно несколько параметров
