# Анализ использования транслитерации английских слов в русскоязычных онлайн-пространствах
В интернет пространствах можно заметить повсеместное использование транслитерцаии. Она может быть использована в ожидаемых контекстах, например, при указании англоязычных терминов или названий. Однако часто транслитерированные выражения используются в качестве вводных слов, имея при этом распространенные аналоги на русском языке. К тому же, можно выделить набор транслитерированных выражений, которые являются заимствованиями из англоязычной интернет-культуры. Целью данной работы является исследование фразеологичности транслитерированных выражений, а также их расположения в контексте фраз.

Гипотезы:
1. Транслитерированные выражения фразеологичны, то есть есть транслитерированные выражения, которые повторяются в онлайн-пространствах чаще, чем можно считать случайным.
2. Русские слова часто подводят к транслитерированным выражениям, которые играют кульминационную роль во фразах. То есть, транслитерированные выражения статистически значимо чаще появляются в конце фразы.
3. Многословные транслитерированные выражения одинаково часто появляются в начале фраз и после существительных.  

**Описание исходных данных**
Данные были собраны из крупных публичных чатов различной направленности в Telegram. В том числе были рассмотрены IT-чат, чат русскоязычного сообщества англоязычных дебатов и чат фанатов Бродвея для повседневного общения. Демографию этих чатов состоавляют молодые люди 18-35 лет с хорошим знанием английского языка. Так как специфика каждого чата требует постоянного взаимодействия с англоязычными ресурсами, их участники часто включают английские выражения в свою речь.

С импользованием морфологического анализатора PyMorphy были выявлены транслитерированные выражения и части речи слов до и после них.

*result.json* - Пример сырых данных. По факту использовался больший объем данных.
