# دليل النشر التفصيلي - مشروع ورشة

## الإعداد قبل النشر

### 1. تجميع الملفات الثابتة

```bash
python manage.py collectstatic --noinput
```

### 2. التأكد من الهجرات

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. اختبار المشروع محلياً

```bash
# تعطيل DEBUG
export DEBUG=False  # على Windows: set DEBUG=False

# تشغيل مع Gunicorn
gunicorn warsha_project.wsgi
```

## النشر على Render.com (موصى به - مجاني)

### الخطوات:

1. **إنشاء حساب GitHub ورفع المشروع**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **التسجيل في Render.com**
   - اذهب إلى https://render.com
   - سجل دخول باستخدام GitHub

3. **إنشاء PostgreSQL Database**
   - اضغط على "New +"
   - اختر "PostgreSQL"
   - اختر الخطة المجانية
   - احفظ `DATABASE_URL` من صفحة المعلومات

4. **إنشاء Web Service**
   - اضغط على "New +"
   - اختر "Web Service"
   - اربط مستودع GitHub الخاص بك
   - الإعدادات:
     - **Name**: warsha-app (أو أي اسم تريده)
     - **Region**: اختر الأقرب لك
     - **Branch**: main
     - **Runtime**: Python 3
     - **Build Command**:
       ```bash
       pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
       ```
     - **Start Command**:
       ```bash
       gunicorn warsha_project.wsgi
       ```

5. **إضافة متغيرات البيئة**
   في قسم "Environment":
   ```
   SECRET_KEY=<generate-a-strong-secret-key>
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.onrender.com
   DATABASE_URL=<paste-from-postgresql-database>
   ```

   لتوليد SECRET_KEY:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **النشر**
   - اضغط "Create Web Service"
   - انتظر حتى يكتمل النشر (5-10 دقائق)

7. **إنشاء مستخدم إداري**
   بعد النشر، في قسم "Shell":
   ```bash
   python manage.py createsuperuser
   ```

8. **الوصول للموقع**
   - الموقع: https://your-app-name.onrender.com
   - لوحة التحكم: https://your-app-name.onrender.com/admin

---

## النشر على Railway.app

### الخطوات:

1. **التسجيل في Railway**
   - اذهب إلى https://railway.app
   - سجل دخول باستخدام GitHub

2. **إنشاء مشروع جديد**
   - اضغط "New Project"
   - اختر "Deploy from GitHub repo"
   - اختر مستودعك

3. **إضافة قاعدة بيانات**
   - اضغط "+ New"
   - اختر "Database"
   - اختر "PostgreSQL"

4. **إعداد المتغيرات**
   في Web Service:
   - اضغط على "Variables"
   - أضف:
     ```
     SECRET_KEY=<your-secret-key>
     DEBUG=False
     ALLOWED_HOSTS=${{RAILWAY_PUBLIC_DOMAIN}}
     DATABASE_URL=${{Postgres.DATABASE_URL}}
     ```

5. **إعداد أوامر البناء**
   في Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn warsha_project.wsgi`

6. **النشر**
   - سيتم النشر تلقائياً
   - احصل على الرابط من "Settings" > "Domains"

---

## النشر على PythonAnywhere

### الخطوات:

1. **إنشاء حساب**
   - اذهب إلى https://www.pythonanywhere.com
   - سجل حساب مجاني

2. **رفع الملفات**
   ```bash
   # في Bash console على PythonAnywhere
   git clone <your-github-repo-url>
   cd Warsha-django-project
   ```

3. **إنشاء بيئة افتراضية**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 warsha-env
   pip install -r requirements.txt
   ```

4. **إعداد Web App**
   - اذهب إلى "Web" tab
   - اضغط "Add a new web app"
   - اختر "Manual configuration"
   - اختر Python 3.11

5. **تكوين WSGI**
   في ملف WSGI:
   ```python
   import os
   import sys
   
   path = '/home/yourusername/Warsha-django-project'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'warsha_project.settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

6. **إعداد Static Files**
   في "Web" tab:
   - URL: `/static/`
   - Directory: `/home/yourusername/Warsha-django-project/staticfiles`

7. **تطبيق الهجرات**
   ```bash
   python manage.py migrate
   python manage.py collectstatic
   python manage.py createsuperuser
   ```

8. **إعادة تحميل التطبيق**
   - اضغط "Reload" في "Web" tab

---

## النشر على Heroku

### الخطوات:

1. **تثبيت Heroku CLI**
   ```bash
   # Windows
   # قم بتحميل المثبت من: https://devcenter.heroku.com/articles/heroku-cli
   
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **تسجيل الدخول**
   ```bash
   heroku login
   ```

3. **إنشاء تطبيق**
   ```bash
   heroku create warsha-app
   ```

4. **إضافة PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:essential-0
   ```

5. **إعداد المتغيرات**
   ```bash
   heroku config:set SECRET_KEY="<your-secret-key>"
   heroku config:set DEBUG=False
   heroku config:set ALLOWED_HOSTS=warsha-app.herokuapp.com
   ```

6. **النشر**
   ```bash
   git push heroku main
   ```

7. **تطبيق الهجرات**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

8. **فتح التطبيق**
   ```bash
   heroku open
   ```

---

## نصائح مهمة

### الأمان

1. **لا تشارك SECRET_KEY أبداً**
2. **تأكد من DEBUG=False في الإنتاج**
3. **استخدم HTTPS دائماً**
4. **قم بتحديث ALLOWED_HOSTS**

### الأداء

1. **استخدم قاعدة بيانات PostgreSQL للإنتاج**
2. **فعّل WhiteNoise لخدمة الملفات الثابتة**
3. **استخدم CDN للصور والملفات الكبيرة**

### النسخ الاحتياطي

1. **قم بعمل نسخة احتياطية من قاعدة البيانات بانتظام**
   ```bash
   # Render
   pg_dump $DATABASE_URL > backup.sql
   
   # Heroku
   heroku pg:backups:capture
   heroku pg:backups:download
   ```

### المراقبة

1. **راقب السجلات (Logs)**
   ```bash
   # Render: في لوحة التحكم
   # Railway: في لوحة التحكم
   # Heroku:
   heroku logs --tail
   ```

2. **راقب الأداء والأخطاء**

---

## استكشاف الأخطاء

### خطأ: Static files not found

```bash
python manage.py collectstatic --noinput
```

### خطأ: Database connection

تأكد من:
- DATABASE_URL صحيح
- قاعدة البيانات تعمل
- الهجرات مطبقة

### خطأ: 500 Internal Server Error

1. تحقق من السجلات
2. تأكد من DEBUG=False
3. تأكد من ALLOWED_HOSTS صحيح

---

## الدعم

للمساعدة:
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Render Documentation](https://render.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Heroku Django Guide](https://devcenter.heroku.com/articles/django-app-configuration)
