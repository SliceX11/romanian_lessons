#!/usr/bin/env python3
"""
Скрипт для генерации аудиофайлов из JSON файлов уроков
используя Google Text-to-Speech API
"""

import json
import os
import sys
from pathlib import Path

try:
    from gtts import gTTS
except ImportError:
    print("Ошибка: Необходимо установить gtts")
    print("Выполните: pip install gtts")
    sys.exit(1)

def create_audio_directory():
    """Создает папку audio если её нет"""
    audio_dir = Path("audio")
    audio_dir.mkdir(exist_ok=True)
    return audio_dir

def generate_audio_for_text(text, filename, audio_dir, lang='ro', slow=False):
    """
    Генерирует аудиофайл для текста
    
    Args:
        text (str): Текст для озвучки
        filename (str): Имя файла
        audio_dir (Path): Путь к папке audio
        lang (str): Язык (по умолчанию румынский)
        slow (bool): Медленная речь
    """
    try:
        # Создаем объект gTTS
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Сохраняем файл
        filepath = audio_dir / filename
        tts.save(str(filepath))
        
        print(f"✓ Создан: {filename}")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка при создании {filename}: {e}")
        return False

def process_lesson_file(lesson_file):
    """Обрабатывает файл урока и генерирует аудио"""
    
    if not os.path.exists(lesson_file):
        print(f"Файл {lesson_file} не найден")
        return False
    
    # Создаем папку audio
    audio_dir = create_audio_directory()
    
    try:
        with open(lesson_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Ошибка при чтении {lesson_file}: {e}")
        return False
    
    print(f"\n📁 Обрабатываем файл: {lesson_file}")
    
    success_count = 0
    total_count = 0
    
    # Обрабатываем слова
    if 'words' in data and data['words']:
        print(f"\n🎯 Генерируем аудио для слов ({len(data['words'])} шт.):")
        
        for word in data['words']:
            if 'ro' in word and 'audio' in word:
                total_count += 1
                
                # Проверяем, существует ли уже файл
                audio_path = audio_dir / word['audio']
                if audio_path.exists():
                    print(f"⚠ Файл {word['audio']} уже существует, пропускаем")
                    success_count += 1
                    continue
                
                if generate_audio_for_text(word['ro'], word['audio'], audio_dir):
                    success_count += 1
    
    # Обрабатываем диалоги
    if 'dialogs' in data and data['dialogs']:
        dialog_count = sum(len(dialog) for dialog in data['dialogs'])
        print(f"\n💬 Генерируем аудио для диалогов ({dialog_count} фраз):")
        
        for dialog in data['dialogs']:
            for phrase in dialog:
                if 'ro' in phrase and 'audio' in phrase:
                    total_count += 1
                    
                    # Проверяем, существует ли уже файл
                    audio_path = audio_dir / phrase['audio']
                    if audio_path.exists():
                        print(f"⚠ Файл {phrase['audio']} уже существует, пропускаем")
                        success_count += 1
                        continue
                    
                    if generate_audio_for_text(phrase['ro'], phrase['audio'], audio_dir):
                        success_count += 1
    
    print(f"\n📊 Результат: {success_count}/{total_count} файлов создано успешно")
    return success_count == total_count

def main():
    """Основная функция"""
    
    print("🎵 Генератор аудиофайлов для румынских уроков")
    print("=" * 50)
    
    # Ищем все файлы lesson*.json
    lesson_files = sorted([f for f in os.listdir('.') if f.startswith('lesson') and f.endswith('.json')])
    
    if not lesson_files:
        print("❌ Файлы уроков (lesson*.json) не найдены")
        return
    
    print(f"📚 Найдено файлов уроков: {len(lesson_files)}")
    
    # Проверяем подключение к интернету
    print("\n🌐 Проверяем подключение к Google TTS...")
    try:
        test_tts = gTTS(text="test", lang='ro')
        print("✓ Подключение к Google TTS успешно")
    except Exception as e:
        print(f"❌ Ошибка подключения к Google TTS: {e}")
        print("Проверьте подключение к интернету")
        return
    
    # Обрабатываем каждый файл
    total_success = True
    for lesson_file in lesson_files:
        success = process_lesson_file(lesson_file)
        total_success = total_success and success
    
    print("\n" + "=" * 50)
    if total_success:
        print("🎉 Все аудиофайлы созданы успешно!")
    else:
        print("⚠ Некоторые файлы не удалось создать")
    
    print(f"\n📁 Аудиофайлы сохранены в папку: ./audio/")

if __name__ == "__main__":
    main()
