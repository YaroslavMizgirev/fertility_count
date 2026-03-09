from fertility_count import compute_fertility
import json

text = '''Процедура ОбработкаПроведения(Отказ, РежимПроведения)
    Запрос = Новый Запрос;
    Запрос.Текст = "ВЫБРАТЬ Номенклатура ИЗ Документ.РасходнаяНакладная";
КонецПроцедуры'''

import pprint
pprint.pprint(compute_fertility(text))
