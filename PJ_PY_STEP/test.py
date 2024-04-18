def format_text(text: str):
    new_pizza_description_words = text.split()
    new_pizza_formatted_description = ""
    line_len = 0
    
    for word in new_pizza_description_words:
        if line_len + len(word) <= 80:
            new_pizza_formatted_description += word + ' '
            line_len += len(word) + 1
        else:
            new_pizza_formatted_description += '\n' + word + ' '
            line_len = len(word) + 1 
    
    return new_pizza_formatted_description.strip()

# Пример использования:
input_text = "Это пример текста, который нужно отформатировать. Мы добавим перенос строки после каждых 12 слов. Это будет полезно для улучшения читаемости текста."
formatted_text = format_text(input_text)
print(formatted_text)