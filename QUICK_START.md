# البدء السريع - نشر مشروع ورشة

## ✅ الملفات الجاهزة

تم إنشاء الملفات التالية للنشر:

- ✅ `requirements.txt` - المكتبات المطلوبة
- ✅ `Procfile` - ملف تشغيل Heroku
- ✅ `runtime.txt` - إصدار Python
- ✅ `.env.example` - مثال لمتغيرات البيئة
- ✅ `.gitignore` - ملفات يتم تجاهلها في Git
- ✅ `README.md` - توثيق المشروع
- ✅ `DEPLOYMENT.md` - دليل النشر التفصيلي
- ✅ `generate_secret_key.py` - توليد مفتاح سري

## 🚀 خطوات النشر السريع (Render.com - مجاني)

### 1. رفع المشروع على GitHub

```bash
# إذا لم تكن قد أنشأت مستودع Git بعد
git init
git add .
git commit -m "Ready for deployment"

# إنشاء مستودع على GitHub ثم:
git remote add origin https://github.com/username/warsha-project.git
git branch -M main
git push -u origin main
```

### 2. التسجيل في Render.com

1. اذهب إلى: https://render.com
2. سجل دخول باستخدام حساب GitHub

### 3. إنشاء قاعدة بيانات PostgreSQL

1. اضغط "New +" → "PostgreSQL"
2. اختر الخطة المجانية (Free)
3. اضغط "Create Database"
4. **احفظ** `Internal Database URL` من صفحة المعلومات

### 4. إنشاء Web Service

1. اضغط "New +" → "Web Service"
2. اختر مستودع GitHub الخاص بك
3. املأ الإعدادات:

**Basic Settings:**
- Name: `warsha-app` (أو أي اسم)
- Region: اختر الأقرب لك
- Branch: `main`
- Runtime: `Python 3`

**Build & Deploy:**
- Build Command:
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- Start Command:
  ```bash
  gunicorn warsha_project.wsgi
  ```

**Environment Variables:**
اضغط "Add Environment Variable" وأضف:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | [استخدم `python generate_secret_key.py`] |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
| `DATABASE_URL` | [الصق من PostgreSQL Database] |

### 5. النشر

1. اضغط "Create Web Service"
2. انتظر 5-10 دقائق حتى يكتمل النشر
3. سترى "Live" عندما يكون جاهزاً

### 6. إنشاء مستخدم إداري

1. في صفحة Web Service، اذهب إلى "Shell"
2. نفذ:
   ```bash
   python manage.py createsuperuser
   ```
3. أدخل اسم المستخدم والبريد وكلمة المرور

### 7. الوصول للموقع

- **الموقع**: https://your-app-name.onrender.com
- **لوحة التحكم**: https://your-app-name.onrender.com/admin

---

## 🎯 البدائل الأخرى

### Railway.app (سهل جداً)
1. https://railway.app
2. "New Project" → "Deploy from GitHub"
3. أضف PostgreSQL
4. أضف متغيرات البيئة
5. انتهى!

### PythonAnywhere (تقليدي)
- مناسب للمبتدئين
- واجهة بسيطة
- دليل كامل في `DEPLOYMENT.md`

### Heroku (احترافي)
- يتطلب Heroku CLI
- دليل كامل في `DEPLOYMENT.md`

---

## 📝 ملاحظات مهمة

### توليد SECRET_KEY جديد
```bash
python generate_secret_key.py
```

### تحديث المشروع بعد التعديلات
```bash
git add .
git commit -m "Update project"
git push origin main
```
سيتم النشر تلقائياً على Render/Railway

### مشاهدة السجلات (Logs)
- **Render**: في لوحة التحكم → Logs
- **Railway**: في لوحة التحكم → Deployments
- **Heroku**: `heroku logs --tail`

### النسخ الاحتياطي
قم بعمل نسخة احتياطية من قاعدة البيانات بانتظام من لوحة تحكم الخدمة.

---

## ❓ استكشاف الأخطاء

### الموقع لا يعمل (500 Error)
1. تحقق من السجلات (Logs)
2. تأكد من `ALLOWED_HOSTS` صحيح
3. تأكد من `DATABASE_URL` صحيح

### الصور والـ CSS لا تظهر
```bash
python manage.py collectstatic --noinput
```

### خطأ في قاعدة البيانات
```bash
python manage.py migrate
```

---

## 📞 الدعم

- راجع `DEPLOYMENT.md` للتفاصيل الكاملة
- راجع `README.md` للتوثيق الشامل
- افتح Issue على GitHub للمساعدة

---

## ✨ نصيحة

**Render.com** هو الخيار الأفضل للبداية:
- ✅ مجاني تماماً
- ✅ سهل الاستخدام
- ✅ نشر تلقائي من GitHub
- ✅ SSL مجاني
- ✅ قاعدة بيانات PostgreSQL مجانية

**ابدأ الآن!** 🚀
