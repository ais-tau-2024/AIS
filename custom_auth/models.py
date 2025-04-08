from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.hashers import make_password, check_password
import uuid


def generate_unique_token():
    """
    Генерирует уникальный токен на основе UUID4.
    Убеждается в уникальности токена в таблице TeacherAuthTokenModel.
    """
    while True:
        token = str(uuid.uuid4())
        if not TeacherAuthTokenModel.objects.filter(token=token).exists():
            return token

# GROUP

class GroupModel(models.Model):
    """
    ## Модель группы студентов
    - name - название группы
    - faculty - связь с факультетом
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'group' 


# STUDENT

class StudentModel(models.Model):
    """
    ## Модель студента
    first_name - имя
    last_name - фамилия
    patronymic - отчество
    group - группа
    birth_date - дата рождения
    gender - пол
    nationality - национальность
    marital_status - семейное положение
    citizenship - гражданство
    country_of_origin - страна, откуда прибыл
    place_of_birth - место рождения
    was_born_in_another_country - родился ли в другой стране
    locality_of_registration - населенный пункт прописки
    registration_address - адрес прописки
    place_of_residence - место проживания
    residential_address - адрес проживания
    """
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Не замужем/Не женат'),
        ('married', 'Замужем/Женат'),
        ('divorced', 'Разведен/Разведена'),
    ]

    iin = models.CharField(
        max_length=12,
        validators=[
            MinLengthValidator(12),
            RegexValidator(
                regex=r'^\d{12}$',
                message='IIN must be exactly 12 digits.',
                code='invalid_iin'
            )
        ]
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, null=True, blank=True)
    group = models.ForeignKey(GroupModel, on_delete=models.SET_NULL, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    marital_status = models.CharField(
        max_length=30, 
        choices=MARITAL_STATUS_CHOICES, 
        null=True, 
        blank=True
    )
    citizenship = models.CharField(max_length=30, null=True, blank=True)
    country_of_origin = models.CharField(max_length=30, null=True, blank=True)
    place_of_birth = models.CharField(max_length=50, null=True, blank=True)
    was_born_in_another_country = models.BooleanField(default=False)
    locality_of_registration = models.CharField(max_length=50, null=True, blank=True)
    registration_address = models.CharField(max_length=50, null=True, blank=True)
    place_of_residence = models.CharField(max_length=50, null=True, blank=True)
    residential_address = models.CharField(max_length=50, null=True, blank=True)
    date_of_enrollment = models.DateField(null=True, blank=True)
    form_of_payment = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.iin})"

    class Meta:
        db_table = 'student'


# TEACHER

# Основная модель преподавателя
class TeacherModel(models.Model):
    """
    ## Модель преподавателя
    Добавлено поле profile_photo для фото профиля.
    admission_date - Дата поступления на работу
    """
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Не замужем/Не женат'),
        ('married', 'Замужем/Женат'),
        ('divorced', 'Разведен/Разведена'),
    ]

    iin = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{12}$',
                message='IIN must be exactly 12 digits.',
                code='invalid_iin'
            )
        ]
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    citizenship = models.CharField(max_length=50, null=True, blank=True)
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, null=True, blank=True)
    document_series = models.CharField(max_length=255, null=True, blank=True)
    document_type = models.CharField(max_length=100, null=True, blank=True)
    document_number = models.CharField(max_length=50, null=True, blank=True)
    document_issue_date = models.DateField(null=True, blank=True)
    document_expiry_date = models.DateField(null=True, blank=True)
    issuing_authority = models.CharField(max_length=255, null=True, blank=True)
    registration_address = models.TextField(null=True, blank=True)
    residential_address = models.TextField(null=True, blank=True)
    home_phone = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    teaching_language = models.CharField(max_length=50, null=True, blank=True)
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True
    )
    admission_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.iin})"

    @classmethod
    def authenticate(cls, iin, password):
        """
        Аутентифицирует преподавателя по ИИН и паролю.
        """
        teacher = cls.objects.filter(iin=iin).first()
        if teacher and TeacherAuthModel.verify_password(teacher, password):
            token = TeacherAuthTokenModel.create_token(teacher)
            return token.token
        return None

    @classmethod
    def logout(cls, token_str):
        """
        Выход из системы. Удаляет токен.
        """
        token = TeacherAuthTokenModel.objects.filter(token=token_str).first()
        if token:
            token.delete()
            return True
        return False

    @classmethod
    def create_teacher(cls, iin, first_name, last_name, **kwargs):
        """
        Создаёт нового преподавателя и сохраняет его в базе.
        - iin: ИИН
        - first_name: Имя
        - last_name: Фамилия
        - kwargs: Дополнительные поля для заполнения
        """
        teacher = cls(
            iin=iin,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        teacher.save()
        return teacher

    class Meta:
        db_table = 'teacher'


# Авторизация преподавателя
class TeacherAuthModel(models.Model):
    """
    ## Модель авторизации преподавателя (создается запись при первом входе преподавателя в системе, это нужно для создания пароля пользователя)
    - teacher: Преподаватель (ссылка на модель TeacherModel)
    - password: Пароль (хэшированный)
    """
    teacher = models.OneToOneField('TeacherModel', on_delete=models.CASCADE, related_name='auth')
    password = models.CharField(max_length=255)

    @classmethod
    def create_auth(cls, teacher, raw_password):
        """
        Создает запись авторизации с хэшированным паролем.
        - teacher: Преподаватель (TeacherModel)
        - raw_password: Пароль в открытом виде
        """
        hashed_password = make_password(raw_password)
        return cls.objects.create(teacher=teacher, password=hashed_password)

    @classmethod
    def verify_password(cls, teacher, raw_password):
        """
        Проверяет соответствие пароля.
        - teacher: Преподаватель (TeacherModel)
        - raw_password: Пароль в открытом виде
        """
        try:
            auth = cls.objects.get(teacher=teacher)
            return check_password(raw_password, auth.password)
        except cls.DoesNotExist:
            return False

    class Meta:
        db_table = 'teacher_auth'

# Токены для аутентификации
class TeacherAuthTokenModel(models.Model):
    """
    ## Модель токенов преподавателя (модель для хранения токенов авторизации)
    - teacher: Преподаватель (TeacherModel)
    - token: Уникальный токен
    """
    teacher = models.ForeignKey(
        'TeacherModel',
        on_delete=models.CASCADE,
        related_name='auth_tokens'
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_token(cls, teacher):
        """
        Создает уникальный токен для преподавателя.
        - teacher: Преподаватель (TeacherModel)
        """
        return cls.objects.create(teacher=teacher, token=generate_unique_token()).token

    class Meta:
        db_table = 'teacher_auth_token'

# TEACHER ADDITIONAL MODELS

class TeacherAchievementModel(models.Model):
    """
    ## Модель достижений преподавателя (Сведения об обучении -> общая информация -> Достижения)
    - teacher: Преподаватель
    - title: Название достижения
    - description: Описание достижения
    """
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'teacher_achievement'

class TeacherScienceFieldModel(models.Model):
    """
    ## Модель отрасли науки преподавателя (Сведения об обучении)
    - teacher: Преподаватель
    - field: Отрасль науки
    - academic_degree: Ученая степень
    - academic_status: Академический статус
    """
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, related_name='science_fields')
    field = models.CharField(max_length=255)
    academic_degree = models.CharField(max_length=100)
    academic_status = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = 'teacher_science_field'
        
class TeacherForeignLanguageModel(models.Model):
    """
    ## Модель владения иностранным языком
    - teacher: Преподаватель
    - language: Язык
    - proficiency_level: Уровень владения (по шкале CEFR)
    """
    LANGUAGE_LEVEL_CHOICES = [
        ('A1', 'A1 - Начальный'),
        ('A2', 'A2 - Элементарный'),
        ('B1', 'B1 - Средний'),
        ('B2', 'B2 - Выше среднего'),
        ('C1', 'C1 - Продвинутый'),
        ('C2', 'C2 - Владение'),
    ]

    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, related_name='foreign_languages')
    language = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=2, choices=LANGUAGE_LEVEL_CHOICES)

    class Meta:
        db_table = 'teacher_foreign_language'
        

class TeacherEducationRecordModel(models.Model):
    """
    ## Модель записи об образовании преподавателя
    - teacher: Преподаватель
    - institution_name: Название учебного заведения
    - document_details: Сведения о документе об образовании
    - graduation_year: Год окончания
    - qualification: Квалификация по документу об образовании
    - specialization: Специальность по документу об образовании
    - foreign_institution: Было ли это зарубежное учебное заведение
    """
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, related_name='education_records')
    institution_name = models.CharField(max_length=255)
    document_details = models.TextField()
    graduation_year = models.PositiveIntegerField()
    qualification = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    foreign_institution = models.BooleanField(default=False)
    scan_copy = models.FileField(upload_to='education_scans/', null=True, blank=True)

    class Meta:
        db_table = 'teacher_education_record'
        

class TeacherCategoryModel(models.Model):
    """
    ## Модель категории преподавателя
    - teacher: Преподаватель
    - category: Категория преподавателя
    - order_number: Номер приказа
    - order_date: Дата приказа
    - confirmation_document: Подтверждающий документ
    """
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, related_name='categories')
    category = models.CharField(max_length=100)
    order_number = models.CharField(max_length=50)
    order_date = models.DateField()
    confirmation_document = models.FileField(upload_to='confirmation_documents/', null=True, blank=True)

    class Meta:
        db_table = 'teacher_category'


class TeacherGroupModel(models.Model):
    """
    ## Модель групп преподавателей
    - teacher: Преподаватель
    - group: Группа
    """
    teacher = models.ForeignKey(TeacherModel, on_delete=models.CASCADE, related_name='teacher_groups')
    group = models.ForeignKey(GroupModel, on_delete=models.CASCADE, related_name='group_teachers')

    class Meta:
        db_table = 'teacher_group'
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'group'], name='unique_teacher_group')
        ]