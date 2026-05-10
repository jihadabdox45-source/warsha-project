# مشروع ورشة - منصة الحرف اليدوية السعودية

منصة إلكترونية لعرض وتوثيق الحرف اليدوية التقليدية في مختلف مناطق المملكة العربية السعودية.

## المميزات

- 🎨 عرض الحرف اليدوية من مختلف مناطق المملكة
- 🌍 دعم اللغتين العربية والإنجليزية
- ⭐ نظام تقييم وتعليقات للحرف
- ❤️ إضافة الحرف المفضلة
- 👤 نظام تسجيل المستخدمين
- 📱 تصميم متجاوب
- 🎥 دعم الفيديوهات التعريفية

## المناطق المدعومة

- الرياض
- مكة المكرمة
- المدينة المنورة
- عسير
- القصيم
- تبوك
- المنطقة الشرقية

## التقنيات المستخدمة

- **Backend**: Django 5.0
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Frontend**: HTML, CSS, JavaScript
- **Internationalization**: django-modeltranslation
- **Deployment**: Gunicorn, WhiteNoise

## التثبيت المحلي

### المتطلبات

- Python 3.11+
- pip

### خطوات التثبيت

1. استنساخ المشروع:
```bash
git clone <repository-url>
cd Warsha-django-project
```

2. إنشاء بيئة افتراضية:
```bash
python -m venv .venv
source .venv/bin/activate  # على Windows: .venv\Scripts\activate
```

3. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

4. إنشاء ملف البيئة:
```bash
cp .env.example .env
```

5. تطبيق الهجرات:
```bash
python manage.py migrate
```

6. إنشاء مستخدم إداري:
```bash
python manage.py createsuperuser
```

7. تشغيل السيرفر:
```bash
python manage.py runserver
```

8. فتح المتصفح على: http://localhost:8000

## النشر على الإنترنت

### الخيار 1: Render.com (مجاني)

1. إنشاء حساب على [Render.com](https://render.com)
2. إنشاء Web Service جديد
3. ربط مستودع GitHub
4. إعدادات النشر:
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn warsha_project.wsgi`
   - **Environment Variables**:
     - `SECRET_KEY`: مفتاح سري قوي
     - `DEBUG`: False
     - `ALLOWED_HOSTS`: your-app.onrender.com
     - `DATABASE_URL`: (سيتم إنشاؤه تلقائياً)

### الخيار 2: Railway.app (مجاني)

1. إنشاء حساب على [Railway.app](https://railway.app)
2. إنشاء مشروع جديد من GitHub
3. إضافة PostgreSQL Database
4. إضافة متغيرات البيئة المطلوبة

### الخيار 3: PythonAnywhere (مجاني)

1. إنشاء حساب على [PythonAnywhere](https://www.pythonanywhere.com)
2. رفع الملفات
3. إعداد Web App
4. تكوين WSGI

### الخيار 4: Heroku

1. إنشاء حساب على [Heroku](https://heroku.com)
2. تثبيت Heroku CLI
3. تنفيذ الأوامر:
```bash
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## متغيرات البيئة المطلوبة

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DATABASE_URL=postgres://user:password@host:5432/dbname
```

## البنية

```
warsha_project/
├── core/                 # التطبيق الأساسي
│   ├── templates/       # قوالب HTML
│   ├── static/          # ملفات CSS/JS
│   └── views.py         # العروض
├── crafts/              # تطبيق الحرف
│   ├── models.py        # نماذج البيانات
│   ├── views.py         # العروض
│   └── templates/       # قوالب الحرف
├── warsha_project/      # إعدادات المشروع
│   ├── settings.py      # الإعدادات
│   └── urls.py          # المسارات
└── manage.py            # أداة إدارة Django
```

## لوحة التحكم

الوصول إلى لوحة التحكم: `/admin`

## الترخيص

هذا المشروع مفتوح المصدر.

## المساهمة

المساهمات مرحب بها! يرجى فتح Issue أو Pull Request.

## الدعم

للأسئلة والدعم، يرجى فتح Issue في المستودع.
