import random
import uuid
from datetime import datetime, timedelta
import os
from faker import Faker

class BookmateDataGenerator:
    def __init__(self):
        self.data_file = "data.sql"
        
        # Configurar Faker con locales en español
        self.fake = Faker(['es_ES', 'es_MX', 'es_AR'])
        
        # Listas específicas que mantenemos para el contexto literario
        self.generos_literarios = [
            'Ficción', 'No ficción', 'Misterio', 'Romance', 'Ciencia ficción', 
            'Fantasía', 'Biografía', 'Historia', 'Terror', 'Aventura',
            'Drama', 'Comedia', 'Ensayo', 'Poesía', 'Thriller'
        ]
        
        self.editoriales_famosas = [
            "Editorial Planeta", "Penguin Random House", "Alfaguara", "Anagrama",
            "Seix Barral", "Tusquets", "Cátedra", "Espasa", "Crítica", "Destino",
            "Salamandra", "Minotauro", "Acantilado", "Berenice", "Impedimenta"
        ]
        
        self.idiomas = ["Español", "Inglés", "Francés", "Portugués", "Italiano", "Alemán", "Catalán"]
        
        # Plantillas para generar contenido más realista
        self.tipos_biografia = [
            "Escritor y periodista reconocido por su estilo narrativo único",
            "Novelista contemporáneo con múltiples premios internacionales",
            "Autor de obras que han marcado la literatura hispanoamericana",
            "Poeta y ensayista cuya obra trasciende generaciones",
            "Dramaturgo y novelista de gran influencia en la literatura mundial",
            "Escritor cuya obra explora temas sociales y políticos profundos",
            "Autor de cuentos y novelas que han sido traducidos a múltiples idiomas"
        ]
        
        self.tipos_sinopsis = [
            "Una historia fascinante que explora los límites del tiempo y el espacio",
            "Un relato conmovedor sobre el amor y la pérdida en tiempos difíciles",
            "Una obra que combina realismo mágico con crítica social profunda",
            "Un viaje literario a través de la memoria y la identidad",
            "Una novela que desafía las convenciones narrativas tradicionales",
            "Un texto que reflexiona sobre la condición humana en el mundo moderno",
            "Una historia épica que abarca generaciones de una familia extraordinaria"
        ]
        
        self.tipos_notificaciones = [
            "Nuevo libro disponible en tu género favorito",
            "Recordatorio: continúa leyendo tu libro actual",
            "Oferta especial disponible por tiempo limitado",
            "Te recomendamos este libro basado en tus lecturas",
            "Actualización disponible para la aplicación",
            "Tienes un nuevo seguidor en tu perfil",
            "Alguien comentó en tu reseña reciente",
            "Tu lista de lectura ha sido actualizada"
        ]

    def generar_uuid(self):
        """Genera un UUID aleatorio"""
        return str(uuid.uuid4())

    def generar_fecha_aleatoria(self, dias_atras=365):
        """Genera una fecha aleatoria dentro de los últimos días especificados"""
        fecha_base = datetime.now()
        fecha_aleatoria = fecha_base - timedelta(days=random.randint(0, dias_atras))
        return fecha_aleatoria.strftime('%Y-%m-%d %H:%M:%S')

    def generar_isbn(self):
        """Genera un ISBN-13 aleatorio"""
        return f"978-{random.randint(10,99)}-{random.randint(100,999)}-{random.randint(1000,9999)}-{random.randint(0,9)}"

    def generar_usuario(self):
        """Genera un usuario aleatorio usando Faker"""
        user_id = self.generar_uuid()
        nombre = self.fake.name()
        password = self.fake.password(length=12)
        is_premium = self.fake.boolean()
        user_type = random.randint(1, 3)
        
        sql = f"""
-- Usuario generado aleatoriamente
INSERT INTO "user" ("user_id", "password", "name", "is_premium", "user_type") 
VALUES ('{user_id}', '{password}', '{nombre}', {is_premium}, {user_type});
"""
        return sql, user_id

    def generar_autor(self):
        """Genera un autor aleatorio usando Faker"""
        author_id = self.generar_uuid()
        nombre = self.fake.name()
        # Generar biografía más realista
        biografia = f"{random.choice(self.tipos_biografia)}. {self.fake.text(max_nb_chars=200)}"
        nacionalidad = random.randint(1, 200)  # Asumiendo que hay países del 1 al 200
        
        sql = f"""
-- Autor generado aleatoriamente
INSERT INTO "author" ("author_id", "name", "biography", "nationality") 
VALUES ('{author_id}', '{nombre}', '{biografia}', {nacionalidad});
"""
        return sql, author_id

    def generar_editorial(self):
        """Genera una editorial aleatoria usando Faker"""
        publisher_id = self.generar_uuid()
        nombre = random.choice(self.editoriales_famosas)
        country_id = random.randint(1, 200)
        founded_year = self.fake.year()
        website = self.fake.url()
        descripcion = f"Editorial {nombre} fundada en {founded_year}. {self.fake.company_suffix()}"
        
        sql = f"""
-- Editorial generada aleatoriamente
INSERT INTO "publisher" ("publisher_id", "name", "country_id", "founded_year", "website", "description") 
VALUES ('{publisher_id}', '{nombre}', {country_id}, {founded_year}, '{website}', '{descripcion}');
"""
        return sql, publisher_id

    def generar_libro(self, author_id, user_id, publisher_id):
        """Genera un libro aleatorio usando Faker"""
        book_id = self.generar_uuid()
        # Generar título más realista
        titulo = self.fake.catch_phrase()
        sinopsis = f"{random.choice(self.tipos_sinopsis)}. {self.fake.text(max_nb_chars=300)}"
        idioma = random.choice(self.idiomas)
        is_audiobook = self.fake.boolean()
        file_url = self.fake.url()
        published_year = f"{self.fake.year()}-01-01"
        isbn = self.generar_isbn()
        
        sql = f"""
-- Libro generado aleatoriamente
INSERT INTO "book" ("book_id", "title", "author", "synopsis", "language", "is_audiobook", "file_url", "uploaded_by", "publisher_id", "published_year", "isbn") 
VALUES ('{book_id}', '{titulo}', '{author_id}', '{sinopsis}', '{idioma}', {is_audiobook}, '{file_url}', '{user_id}', '{publisher_id}', '{published_year}', '{isbn}');
"""
        return sql, book_id, is_audiobook

    def generar_audiobook(self, book_id):
        """Genera datos de audiobook usando Faker"""
        duration = random.randint(300, 1200)  # 5 a 20 horas en minutos
        narrator = self.fake.name()
        audio_file_url = self.fake.url()
        
        sql = f"""
-- Audiobook generado aleatoriamente
INSERT INTO "audiobook" ("book_id", "duration", "narrator", "audio_file_url") 
VALUES ('{book_id}', {duration}, '{narrator}', '{audio_file_url}');
"""
        return sql

    def generar_metricas_libro(self, book_id):
        """Genera métricas para un libro usando Faker"""
        total_reads = self.fake.random_int(min=50, max=2000)
        total_listens = self.fake.random_int(min=0, max=1000)
        total_favorites = self.fake.random_int(min=10, max=500)
        total_reviews = self.fake.random_int(min=5, max=300)
        average_rating = round(random.uniform(3.0, 5.0), 1)
        last_read_at = self.fake.date_time_between(start_date='-30d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        
        sql = f"""
-- Métricas de libro generadas aleatoriamente
INSERT INTO "book_metrics" ("book_id", "total_reads", "total_listens", "total_favorites", "total_reviews", "average_rating", "last_read_at") 
VALUES ('{book_id}', {total_reads}, {total_listens}, {total_favorites}, {total_reviews}, {average_rating}, '{last_read_at}');
"""
        return sql

    def generar_review(self, user_id, book_id):
        """Genera una reseña aleatoria usando Faker"""
        review_id = self.generar_uuid()
        rating = self.fake.random_int(min=1, max=5)
        comentario = self.fake.sentence(nb_words=8)
        
        sql = f"""
-- Reseña generada aleatoriamente
INSERT INTO "review" ("review_id", "rating", "comment", "user_id", "book_id") 
VALUES ('{review_id}', {rating}, '{comentario}', '{user_id}', '{book_id}');
"""
        return sql

    def generar_favorito(self, user_id, book_id):
        """Genera un favorito aleatorio"""
        favorite_id = self.generar_uuid()
        
        sql = f"""
-- Favorito generado aleatoriamente
INSERT INTO "favorite" ("favorite_id", "user_id", "book_id") 
VALUES ('{favorite_id}', '{user_id}', '{book_id}');
"""
        return sql

    def generar_progreso_lectura(self, user_id, book_id):
        """Genera progreso de lectura usando Faker"""
        pages_read = self.fake.random_int(min=0, max=500)
        minutes_listened = self.fake.random_int(min=0, max=300)
        last_accessed = self.fake.date_time_between(start_date='-7d', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        
        sql = f"""
-- Progreso de lectura generado aleatoriamente
INSERT INTO "user_book" ("user_id", "book_id", "pages_read", "minutes_listened", "last_accessed") 
VALUES ('{user_id}', '{book_id}', {pages_read}, {minutes_listened}, '{last_accessed}');
"""
        return sql

    def generar_lista_lectura(self, user_id):
        """Genera una lista de lectura usando Faker"""
        list_id = self.generar_uuid()
        nombre = f"{self.fake.word().title()} {random.choice(self.generos_literarios)}"
        descripcion = self.fake.sentence(nb_words=10)
        is_public = self.fake.boolean()
        
        sql = f"""
-- Lista de lectura generada aleatoriamente
INSERT INTO "reading_list" ("list_id", "name", "description", "created_by", "is_public") 
VALUES ('{list_id}', '{nombre}', '{descripcion}', '{user_id}', {is_public});
"""
        return sql, list_id

    def generar_item_lista(self, list_id, book_id):
        """Genera un item para una lista de lectura"""
        sql = f"""
-- Item de lista generado aleatoriamente
INSERT INTO "reading_list_item" ("list_id", "book_id") 
VALUES ('{list_id}', '{book_id}');
"""
        return sql

    def generar_notificacion(self, user_id):
        """Genera una notificación usando Faker"""
        notification_id = self.generar_uuid()
        mensaje = random.choice(self.tipos_notificaciones)
        is_read = self.fake.boolean()
        notification_type = random.randint(1, 4)
        
        sql = f"""
-- Notificación generada aleatoriamente
INSERT INTO "notification" ("notification_id", "message", "is_read", "user_id", "notification_type") 
VALUES ('{notification_id}', '{mensaje}', {is_read}, '{user_id}', {notification_type});
"""
        return sql

    def generar_datos_completos(self):
        """Genera un conjunto completo de datos relacionados"""
        datos_sql = []
        
        # Generar usuario
        sql_usuario, user_id = self.generar_usuario()
        datos_sql.append(sql_usuario)
        
        # Generar autor
        sql_autor, author_id = self.generar_autor()
        datos_sql.append(sql_autor)
        
        # Generar editorial
        sql_editorial, publisher_id = self.generar_editorial()
        datos_sql.append(sql_editorial)
        
        # Generar libro
        sql_libro, book_id, is_audiobook = self.generar_libro(author_id, user_id, publisher_id)
        datos_sql.append(sql_libro)
        
        # Si es audiobook, generar datos de audiobook
        if is_audiobook:
            sql_audiobook = self.generar_audiobook(book_id)
            datos_sql.append(sql_audiobook)
        
        # Generar métricas del libro
        sql_metricas = self.generar_metricas_libro(book_id)
        datos_sql.append(sql_metricas)
        
        # Generar géneros para el libro (1-3 géneros aleatorios)
        num_generos = random.randint(1, 3)
        generos_usados = []
        for _ in range(num_generos):
            genero = random.randint(1, 8)
            if genero not in generos_usados:
                generos_usados.append(genero)
                sql_genero = f"""
-- Género de libro generado aleatoriamente
INSERT INTO "genre_book" ("book_id", "genre_type_id") 
VALUES ('{book_id}', {genero});
"""
                datos_sql.append(sql_genero)
        
        # Generar tags para el libro (1-2 tags aleatorios)
        num_tags = random.randint(1, 2)
        tags_usados = []
        for _ in range(num_tags):
            tag = random.randint(1, 6)
            if tag not in tags_usados:
                tags_usados.append(tag)
                sql_tag = f"""
-- Tag de libro generado aleatoriamente
INSERT INTO "book_tag" ("book_id", "tag_id") 
VALUES ('{book_id}', {tag});
"""
                datos_sql.append(sql_tag)
        
        # Generar reseña
        sql_review = self.generar_review(user_id, book_id)
        datos_sql.append(sql_review)
        
        # Generar favorito (50% de probabilidad)
        if random.choice([True, False]):
            sql_favorito = self.generar_favorito(user_id, book_id)
            datos_sql.append(sql_favorito)
        
        # Generar progreso de lectura
        sql_progreso = self.generar_progreso_lectura(user_id, book_id)
        datos_sql.append(sql_progreso)
        
        # Generar lista de lectura
        sql_lista, list_id = self.generar_lista_lectura(user_id)
        datos_sql.append(sql_lista)
        
        # Agregar libro a la lista
        sql_item_lista = self.generar_item_lista(list_id, book_id)
        datos_sql.append(sql_item_lista)
        
        # Generar notificación
        sql_notificacion = self.generar_notificacion(user_id)
        datos_sql.append(sql_notificacion)
        
        return datos_sql

    def guardar_datos(self, datos_sql):
        """Guarda los datos generados en el archivo data.sql"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        with open(self.data_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n-- Datos generados aleatoriamente el {timestamp}\n")
            for sql in datos_sql:
                f.write(sql)
        
        print(f"Datos generados y guardados en {self.data_file}")

    def ejecutar(self):
        """Ejecuta el generador de datos"""
        # Verificar e instalar Faker si es necesario
        try:
            from faker import Faker
        except ImportError:
            print("Faker no está instalado. Instalando...")
            import subprocess
            import sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "faker"])
            print("Faker instalado exitosamente.")
            from faker import Faker
        
        print("Generando datos aleatorios para la base de datos Bookmate...")
        
        # Verificar si el archivo existe
        if not os.path.exists(self.data_file):
            print(f"Archivo {self.data_file} no encontrado. Creando nuevo archivo...")
            with open(self.data_file, 'w', encoding='utf-8') as f:
                f.write("-- Archivo de datos para Bookmate\n")
        
        # Generar datos
        datos_sql = self.generar_datos_completos()
        
        # Guardar datos
        self.guardar_datos(datos_sql)
        
        print("¡Generación completada exitosamente!")
        print(f"Se generaron {len(datos_sql)} consultas SQL nuevas.")

    def generar_multiples_registros(self, cantidad=1):
        """Genera múltiples conjuntos de datos aleatorios"""
        print(f"Generando {cantidad} conjunto(s) de datos aleatorios...")
        
        for i in range(cantidad):
            print(f"Generando conjunto {i+1}/{cantidad}...")
            datos_sql = self.generar_datos_completos()
            self.guardar_datos(datos_sql)
            
        print(f"¡Generación completada! Se generaron {cantidad} conjuntos de datos.")

    def mostrar_estadisticas(self):
        """Muestra estadísticas del archivo de datos"""
        if not os.path.exists(self.data_file):
            print("El archivo de datos no existe.")
            return
            
        with open(self.data_file, 'r', encoding='utf-8') as f:
            contenido = f.read()
            
        # Contar diferentes tipos de INSERT
        tipos_inserts = {
            'usuarios': contenido.count('INSERT INTO "user"'),
            'autores': contenido.count('INSERT INTO "author"'),
            'editoriales': contenido.count('INSERT INTO "publisher"'),
            'libros': contenido.count('INSERT INTO "book"'),
            'audiobooks': contenido.count('INSERT INTO "audiobook"'),
            'reseñas': contenido.count('INSERT INTO "review"'),
            'favoritos': contenido.count('INSERT INTO "favorite"'),
            'listas': contenido.count('INSERT INTO "reading_list"'),
            'notificaciones': contenido.count('INSERT INTO "notification"')
        }
        
        print("\n=== ESTADÍSTICAS DEL ARCHIVO DE DATOS ===")
        for tipo, cantidad in tipos_inserts.items():
            print(f"{tipo.capitalize()}: {cantidad}")
        print(f"Total de líneas: {len(contenido.splitlines())}")
        print(f"Tamaño del archivo: {len(contenido)} caracteres")

    def menu_interactivo(self):
        """Menú interactivo para el generador"""
        while True:
            print("\n" + "="*50)
            print("🎯 GENERADOR DE DATOS BOOKMATE")
            print("="*50)
            print("1. Generar 1 conjunto de datos aleatorios")
            print("2. Generar múltiples conjuntos de datos")
            print("3. Mostrar estadísticas del archivo")
            print("4. Salir")
            print("="*50)
            
            opcion = input("Selecciona una opción (1-4): ").strip()
            
            if opcion == '1':
                self.ejecutar()
            elif opcion == '2':
                try:
                    cantidad = int(input("¿Cuántos conjuntos de datos quieres generar? "))
                    if cantidad > 0:
                        self.generar_multiples_registros(cantidad)
                    else:
                        print("❌ La cantidad debe ser mayor que 0")
                except ValueError:
                    print("❌ Por favor ingresa un número válido")
            elif opcion == '3':
                self.mostrar_estadisticas()
            elif opcion == '4':
                print("¡Hasta luego! 👋")
                break
            else:
                print("❌ Opción no válida. Por favor selecciona 1, 2, 3 o 4.")

# Ejecutar el generador
if __name__ == "__main__":
    generador = BookmateDataGenerator()
    # Preguntar al usuario si quiere usar el menú interactivo
    usar_menu = input("¿Quieres usar el menú interactivo? (s/n): ").strip().lower()
    
    if usar_menu in ['s', 'si', 'sí', 'y', 'yes']:
        generador.menu_interactivo()
    else:
        generador.ejecutar()