# coding: UTF-8
'''
Adaptar essa lógica para gerar um ID único para minhas tabelas no PostgreSQL.
Essa alternativa parece boa porque evita o uso de UUID / GUID
(que tem como drawback chars como primary keys):
    http://instagram-engineering.tumblr.com/post/10853187575/sharding-ids-at-instagram

Como fazer isso no SQLAlchemy:
    http://stackoverflow.com/questions/1038126/auto-incrementing-attribute-with-custom-logic-in-sqlalchemy
'''


