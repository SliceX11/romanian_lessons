#!/usr/bin/env python3
"""
Утилиты для работы с аудиофайлами
"""

import os
import json
from pathlib import Path

def check_audio_files():
    """Проверяет, какие аудиофайлы отсутствуют"""
    
    print("🔍 Проверка аудиофайлов")
    print("=" * 40)
    
    audio_dir = Path("audio")
    if not audio_dir.exists():
        print("❌ Папка audio не найдена")
        return
    
    # Получаем список существующих файлов
    existing_files = set(f.name for f in audio_dir.glob("*.mp3"))
    
    # Собираем список нужных файлов из всех уроков
    needed_files = set()
    lesson_files = sorted([f for f in os.listdir('.') if f.startswith('lesson') and f.endswith('.json')])
    
    for lesson_file in lesson_files:
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Файлы из слов
            if 'words' in data:
                for word in data['words']:
                    if 'audio' in word:
                        needed_files.add(word['audio'])
            
            # Файлы из диалогов
            if 'dialogs' in data:
                for dialog in data['dialogs']:
                    for phrase in dialog:
                        if 'audio' in phrase:
                            needed_files.add(phrase['audio'])
                            
        except Exception as e:
            print(f"❌ Ошибка при обработке {lesson_file}: {e}")
    
    missing_files = needed_files - existing_files
    extra_files = existing_files - needed_files
    
    print(f"📊 Статистика:")
    print(f"   Нужно файлов: {len(needed_files)}")
    print(f"   Есть файлов: {len(existing_files)}")
    print(f"   Отсутствует: {len(missing_files)}")
    print(f"   Лишних: {len(extra_files)}")
    
    if missing_files:
        print(f"\n❌ Отсутствующие файлы ({len(missing_files)}):")
        for file in sorted(missing_files):
            print(f"   - {file}")
    
    if extra_files:
        print(f"\n⚠ Лишние файлы ({len(extra_files)}):")
        for file in sorted(extra_files):
            print(f"   - {file}")
    
    if not missing_files and not extra_files:
        print(f"\n✅ Все аудиофайлы на месте!")

def list_audio_files():
    """Показывает список всех аудиофайлов"""
    
    audio_dir = Path("audio")
    if not audio_dir.exists():
        print("❌ Папка audio не найдена")
        return
    
    files = sorted(audio_dir.glob("*.mp3"))
    
    print(f"🎵 Аудиофайлы ({len(files)} шт.):")
    print("=" * 40)
    
    for file in files:
        size_kb = file.stat().st_size // 1024
        print(f"   {file.name} ({size_kb} KB)")

def clean_unused_audio():
    """Удаляет неиспользуемые аудиофайлы"""
    
    audio_dir = Path("audio")
    if not audio_dir.exists():
        print("❌ Папка audio не найдена")
        return
    
    # Получаем список существующих файлов
    existing_files = {f.name: f for f in audio_dir.glob("*.mp3")}
    
    # Собираем список нужных файлов
    needed_files = set()
    lesson_files = sorted([f for f in os.listdir('.') if f.startswith('lesson') and f.endswith('.json')])
    
    for lesson_file in lesson_files:
        try:
            with open(lesson_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'words' in data:
                for word in data['words']:
                    if 'audio' in word:
                        needed_files.add(word['audio'])
            
            if 'dialogs' in data:
                for dialog in data['dialogs']:
                    for phrase in dialog:
                        if 'audio' in phrase:
                            needed_files.add(phrase['audio'])
                            
        except Exception as e:
            print(f"❌ Ошибка при обработке {lesson_file}: {e}")
    
    # Находим лишние файлы
    extra_files = set(existing_files.keys()) - needed_files
    
    if not extra_files:
        print("✅ Лишних файлов не найдено")
        return
    
    print(f"🗑 Найдено лишних файлов: {len(extra_files)}")
    for filename in sorted(extra_files):
        print(f"   - {filename}")
    
    response = input("\nУдалить лишние файлы? (y/N): ")
    if response.lower() == 'y':
        for filename in extra_files:
            file_path = existing_files[filename]
            file_path.unlink()
            print(f"🗑 Удален: {filename}")
        print(f"✅ Удалено {len(extra_files)} файлов")
    else:
        print("❌ Отменено")

def main():
    """Главное меню"""
    
    print("🎵 Управление аудиофайлами")
    print("=" * 30)
    print("1. Проверить файлы")
    print("2. Показать список файлов") 
    print("3. Очистить неиспользуемые")
    print("4. Выход")
    
    while True:
        choice = input("\nВыберите действие (1-4): ").strip()
        
        if choice == '1':
            check_audio_files()
        elif choice == '2':
            list_audio_files()
        elif choice == '3':
            clean_unused_audio()
        elif choice == '4':
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор, попробуйте еще раз")

if __name__ == "__main__":
    main()
