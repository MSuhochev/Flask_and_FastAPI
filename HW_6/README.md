# Задание №6

### Необходимо создать базу данных для интернет-магазина. 

#### База данных должна состоять из трех таблиц: 
   - товары,
   - заказы,
   - пользователи.

1. Таблица товары должна:
   - содержать информацию 
     * о доступных товарах, 
     * их описаниях 
     * и ценах.
   - содержать следующие поля: 
     * id (PRIMARY KEY), 
     * название, 
     * описание 
     * и цена.

2. Таблица пользователи должна:
   - содержать информацию о зарегистрированных пользователях магазина.
   - содержать следующие поля: 
     * id (PRIMARY KEY),
     * имя,
     * фамилия, 
     * адрес электронной почты, 
     * пароль.

3. Таблица заказы должна:
   - содержать информацию о заказах, сделанных пользователями.
   - содержать следующие поля: 
     * id (PRIMARY KEY), 
     * id пользователя (FOREIGN KEY), 
     * id товара (FOREIGN KEY), 
     * дата заказа 
     * и статус заказа.

4. Создайте модели pydantic для получения новых данных и
возврата существующих в БД для каждой из трёх таблиц
(итого шесть моделей).

5. Реализуйте CRUD операции для каждой из таблиц через
создание маршрутов, REST API (итого 15 маршрутов).
    * Чтение всех
    * Чтение одного
    * Запись
    * Изменение
    * Удаление