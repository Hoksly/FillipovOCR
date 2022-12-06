# Лабораторна робота №3

#### Made by Ryan Goslenko

## Завдання:
### Реалізувати програму, яка використовує зовнішні бібліотеки для реалізації частини функціональності. Студенти мають самостійно прочитати документацію бібліотеки і розібратись, як її використовувати. Програма може бути з графічним інтерфейсом (це кращий варіант) чи з інтерфейсом командного рядка. Можна використовувати одну чи декілька зовнішніх бібліотек/фреймворків.
## Keras and tensorflow
### Опис
- Tensorflow - один з найпопулярніших фреймворків для роботи з машинним навчанням на python, який розробляє компанія Google. Keras в свою чергу, своєрідна надбудована над tensorflow, яка допомагає ще швидше і зручніше створювати, тренувати й використовувати моделі машинного навчання.
### Звіт-ретроспектива

1. Які конкретні задачі планували вирішувати за допомогою цієї бібліотеки?
- Планувалося використовувати цю бібліотеку для завантаження натренованої моделі InceptionV3, попередньої обробки вхідних даних, її тренування на наших даних, збереження моделі.

2. Чому було обрано саме цю бібліотеку, а не аналоги?
- З tensorflow я знайомий вже досить давно, це один з найкращих фреймоворків для машинного навчання на цей час, якщо не найкращий. Він широко підтримується всюди, часто оновлюється і його комп'юніті неймовірно активне. Зазвичай, саме цей фреймворк більшість використовує для задач комп'ютерного зору, його аналоги типу PyTorch часто зручніші для задач типу Reinforcement learning.
3.	Наскільки просто та зрозуміло було отримати, встановити, налаштувати та почати використовувати цю бібліотеку?
- Все максимально просто pip install tensorflow; pip install keras і погнали писати код.
4. Наскільки зрозумілою та корисною була документація бібліотеки?
- Досить зрозуміла, вся документація й гайди є на сайті tensorflow ат keras
- https://keras.io/guides/
- https://www.tensorflow.org/api_docs/python/tf
5. Наскільки було зрозуміло, як саме використовувати бібліотеку, які класи/методи/функції використовувати для вирішення поставлених задач?
- Досить зрозуміло, а якщо не було спочатку не зрозуміло, то в інтернеті достатньо багато матеріалів, в яких можна було знайти потрібне. Потрібен відповідний бекґраунд та досвід роботи з подібними ресурсами.
6. Наскільки зручно було використовувати бібліотеку, чи не треба було писати багато надлишкового коду?
- у випадку з використанням keras - однозначно ні. Сама його ідея полягає в тому, щоб спростити роботу з таким потужним інструментом як tensorflow, щоб писати менше коду. Тут будь-яка задача вирішується в декілька рядків коду, якщо використовувати вже реалізовані засоби.
7. Наскільки зрозумілою була поведінка класів/методів/функцій з бібліотеки?
- Достатньо зрозуміла, якщо користувач знайомий з документацією.
8. Наскільки зрозумілою була взаємодія між різними класами/методами/функціями цієї бібліотеки, а також взаємодія між бібліотекою та власним кодом?
- Взаємодія між внутрішніми класами і функціями бібліотеки просто та зрозуміла, а взаємодія з власним кодом зазвичай відбувається із застосуванням інших бібліотек, наприклад numpy (у нашому випадку) або всім відома pandas.
9. Чи виникали якісь проблеми з використанням бібліотеки? Чи вдалось їх вирішити, як саме?
- Виникла проблема використання вже натренованої нейромережі, адже її архітектура приймає лише 3-х вимірні зображення, хоча для нашої задачі достатньо чорно-білих. Вирішили конвертувати 2-х вимірні зображення в трьохвимірні, перед тим, як їх використовувати.
10. Що хорошого можна сказати про цю бібліотеку, які були позитивні аспекти використання бібліотеки?
- Бібліотека дуже крута, дозволяє дуже швидко і зручно створювати й використовувати нейронні мережі
11. Що поганого можна сказати про цю бібліотеку, які були негативні аспекти використання бібліотеки?
- Із мінусів, як тільки оновлюєшся на якусь нову версію python або ж самої бібліотеки, то кожного разу починаються якісь проблеми, що зазвичай пов'язані із їх взаємодією
12. Якби довелось вирішувати аналогічну задачу, але вже враховуючи досвід використання в цій лабораторній роботі, що варто було б робити так само, а що змінити? Можливо, використати інші бібліотеки, чи використати інші можливості цієї бібліотеки, чи інакше організувати код, чи ще щось?
- Як б так само використовував tensorflow під keras, а змінив би процес організації роботи. 