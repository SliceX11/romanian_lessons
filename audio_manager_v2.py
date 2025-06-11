#!/usr/bin/env python3
"""
Утилиты для работы с аудиофайлами румынских уроков
"""

import os
import json
from pathlib import Path

AUDIO_DIR = "audio"

def load_lesson_data(lesson_file):
    """Загружает данные урока"""
    try:
        with open(lesson_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Ошибка при загрузке {lesson_file}: {e}")
        return None

def get_directory_size(path):
    """Возвращает размер папки в MB"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size / (1024 * 1024)

def show_stats():
    """Показать детальную статистику аудиофайлов"""
    print("\n📊 Статистика аудиофайлов:")
    print("=" * 50)
    
    audio_dir = Path(AUDIO_DIR)
    if not audio_dir.exists():
        print("❌ Папка audio не найдена")
        return
        
    audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3')]
    print(f"Всего аудиофайлов: {len(audio_files)}")
    print(f"Размер папки audio: {get_directory_size(AUDIO_DIR):.1f} MB")
    
    # Статистика по урокам
    lesson_files = [f for f in os.listdir('.') if f.startswith('lesson') and f.endswith('.json')]
    
    total_expected = 0
    total_existing = 0
    
    for lesson_file in sorted(lesson_files):
        lesson_num = lesson_file.replace('lesson', '').replace('.json', '')
        lesson_data = load_lesson_data(lesson_file)
        
        if lesson_data:
            words_count = len(lesson_data.get('words', []))
            dialogs_phrases = sum(len(dialog) for dialog in lesson_data.get('dialogs', []))
            expected = words_count + dialogs_phrases
            total_expected += expected
            
            # Подсчитываем существующие файлы для урока
            existing = 0
            for word in lesson_data.get('words', []):
                if os.path.exists(os.path.join(AUDIO_DIR, word['audio'])):
                    existing += 1
            
            for dialog in lesson_data.get('dialogs', []):
                for phrase in dialog:
                    if os.path.exists(os.path.join(AUDIO_DIR, phrase['audio'])):
                        existing += 1
            
            total_existing += existing
            completion = (existing / expected * 100) if expected > 0 else 0
            
            lesson_titles = {
                "1": "Приветствие", 
                "2": "Знакомство", 
                "3": "Числа и время"
            }
            lesson_title = lesson_titles.get(lesson_num, "Неизвестный урок")
            
            print(f"\nУрок {lesson_num}: {lesson_title}")
            print(f"  Слова: {words_count}")
            print(f"  Фразы диалогов: {dialogs_phrases}")
            print(f"  Аудио готово: {existing}/{expected} ({completion:.1f}%)")
            
            if completion < 100:
                print(f"  ⚠ Отсутствует {expected - existing} файлов")
    
    overall_completion = (total_existing / total_expected * 100) if total_expected > 0 else 0
    print(f"\n📈 Общая готовность: {total_existing}/{total_expected} ({overall_completion:.1f}%)")

def check_audio_files():
    """Проверяет, какие аудиофайлы отсутствуют"""
    
    print("🔍 Проверка аудиофайлов")
    print("=" * 40)
    
    audio_dir = Path(AUDIO_DIR)
    if not audio_dir.exists():
        print("❌ Папка audio не найдена")
        return
    
    # Получаем список существующих файлов
    existing_files = set(f.name for f in audio_dir.glob("*.mp3"))
    
    # Собираем список нужных файлов из всех уроков
    needed_files = set()
    lesson_files = sorted([f for f in os.listdir('.') if f.startswith('lesson') and f.endswith('.json')])
    
    for lesson_file in lesson_files:
        lesson_data = load_lesson_data(lesson_file)
        if lesson_data:
            # Файлы из слов
            if 'words' in lesson_data:
                for word in lesson_data['words']:
                    if 'audio' in word:
                        needed_files.add(word['audio'])
            
            # Файлы из диалогов
            if 'dialogs' in lesson_data:
                for dialog in lesson_data['dialogs']:
                    for phrase in dialog:
                        if 'audio' in phrase:
                            needed_files.add(phrase['audio'])
    
    missing_files = needed_files - existing_files
    extra_files = existing_files - needed_files
    
    print(f"📊 Статистика:")
    print(f"   Нужно файлов: {len(needed_files)}")
    print(f"   Есть файлов: {len(existing_files)}")
    print(f"   Отсутствует: {len(missing_files)}")
    print(f"   Лишних: {len(extra_files)}")
    
    if missing_files:
        print(f"\n❌ Отсутствующие файлы ({len(missing_files)}):")
        for file in sorted(missing_files)[:10]:  # Показываем только первые 10
            print(f"   - {file}")
        if len(missing_files) > 10:
            print(f"   ... и еще {len(missing_files) - 10} файлов")
    
    if extra_files:
        print(f"\n⚠ Лишние файлы ({len(extra_files)}):")
        for file in sorted(extra_files)[:10]:  # Показываем только первые 10
            print(f"   - {file}")
        if len(extra_files) > 10:
            print(f"   ... и еще {len(extra_files) - 10} файлов")
    
    if not missing_files and not extra_files:
        print(f"\n✅ Все аудиофайлы на месте!")

def list_audio_files():
    """Показывает список всех аудиофайлов"""
    
    audio_dir = Path(AUDIO_DIR)
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
    
    audio_dir = Path(AUDIO_DIR)
    if not audio_dir.exists():
        print("❌ Папка audio не найдена")
        return
    
    # Получаем список существующих файлов
    existing_files = {f.name: f for f in audio_dir.glob("*.mp3")}
    
    # Собираем список нужных файлов
    needed_files = set()
    lesson_files = sorted([f for f in os.listdir('.') if f.startswith('lesson') and f.endswith('.json')])
    
    for lesson_file in lesson_files:
        lesson_data = load_lesson_data(lesson_file)
        if lesson_data:
            if 'words' in lesson_data:
                for word in lesson_data['words']:
                    if 'audio' in word:
                        needed_files.add(word['audio'])
            
            if 'dialogs' in lesson_data:
                for dialog in lesson_data['dialogs']:
                    for phrase in dialog:
                        if 'audio' in phrase:
                            needed_files.add(phrase['audio'])
    
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

def generate_missing_audio():
    """Генерирует отсутствующие аудиофайлы"""
    print("🎵 Генерация отсутствующих аудиофайлов")
    print("Запускаем generate_audio.py...")
    
    import subprocess
    try:
        result = subprocess.run(['python', 'generate_audio.py'], check=True, capture_output=True, text=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при генерации: {e}")
        print(e.stderr)
    except FileNotFoundError:
        print("❌ Файл generate_audio.py не найден")

def main():
    """Главное меню"""
    
    print("🎵 Управление аудиофайлами румынских уроков")
    print("=" * 50)
    print("1. 📊 Показать статистику")
    print("2. 🔍 Проверить файлы")
    print("3. 📄 Показать список файлов") 
    print("4. 🗑 Очистить неиспользуемые")
    print("5. 🎵 Генерировать недостающие")
    print("6. 🚪 Выход")
    
    while True:
        choice = input("\nВыберите действие (1-6): ").strip()
        
        if choice == '1':
            show_stats()
        elif choice == '2':
            check_audio_files()
        elif choice == '3':
            list_audio_files()
        elif choice == '4':
            clean_unused_audio()
        elif choice == '5':
            generate_missing_audio()
        elif choice == '6':
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор, попробуйте еще раз")

if __name__ == "__main__":
    main()
