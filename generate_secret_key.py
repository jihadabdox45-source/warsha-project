#!/usr/bin/env python
"""
سكريبت لتوليد SECRET_KEY جديد لـ Django
"""
from django.core.management.utils import get_random_secret_key

if __name__ == '__main__':
    secret_key = get_random_secret_key()
    print("\n" + "="*60)
    print("SECRET_KEY الجديد:")
    print("="*60)
    print(secret_key)
    print("="*60)
    print("\nانسخ هذا المفتاح وضعه في ملف .env أو في متغيرات البيئة")
    print("="*60 + "\n")
